import base64
import csv
import html
import json
import logging
import re
import smtplib
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

# ============================================================
# EagleView Estates | Private Yard Allocation Portal
# Complete master code
# ============================================================

APP_TITLE = "EagleView Estates | Private Yard Allocation Portal"
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "Private Yard Allocation Portal • CentrePort Canada • Winnipeg"

BACKGROUND_IMAGE = Path("site_photo.jpg")
SITE_LAYOUT_OVERVIEW = Path("site_layout.jpg")
LAYOUT_DIRECTORY = Path("layouts")
DATA_DIRECTORY = Path("data")
GENERATED_DIRECTORY = Path("generated")
LEAD_CSV_FILE = DATA_DIRECTORY / "eagleview_leads.csv"

DEFAULT_SENDER_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_ADMIN_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_BOOKING_LINK = ""
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon=APP_ICON)


@dataclass(frozen=True)
class PricingDeal:
    daily: str
    weekly: str
    monthly: str
    yearly: str
    multi_year: str
    details: str


@dataclass
class EmailSendResult:
    client_sent: bool = False
    admin_sent: bool = False
    client_error: str = ""
    admin_error: str = ""
    smtp_username: str = ""
    sender_email: str = ""
    admin_email: str = ""
    client_email: str = ""


@dataclass(frozen=True)
class AttachmentStatus:
    overview_attached: bool = False
    overview_status: str = ""
    size_layout_attached: bool = False
    size_layout_status: str = ""
    leasing_pdf_attached: bool = False
    leasing_pdf_status: str = ""


PRICING_DEALS: Dict[str, PricingDeal] = {
    "💎 Anchor Tenant: 5-Acre Parcel": PricingDeal(
        "$1,000 - $1,500/day", "$4,500 - $6,500/week", "$9,500 - $14,500/month",
        "$110k - $155k/annum", "Custom institutional quote",
        "Full 5-acre integrated site with exclusive controlled gate access.",
    ),
    "Dedicated Pad: 1,000 - 5,000 sq ft": PricingDeal(
        "$150 - $350/day", "$900 - $1,500/week", "$2,250 - $4,500/month",
        "$28k - $45k/annum", "$25k - $38k/annum, 3+ year term",
        "Engineered gravel pad with dedicated lighting and surveillance coverage.",
    ),
    "Flex Staging / Short-Term Laydown": PricingDeal(
        "$350 - $550/day", "$1,800 - $2,800/week", "$5,000 - $7,500/month",
        "Available by quote", "Available by quote",
        "Rapid-access staging for project material laydown, fleet positioning, and short-term contractor use.",
    ),
    "Winter Equipment Storage": PricingDeal(
        "N/A", "N/A", "$1,200 - $2,100/month",
        "$12,500 - $18,000 seasonal, October-May", "Fleet-volume discounts available",
        "Seasonal storage for equipment, trailers, attachments, and contractor assets.",
    ),
}

CLIENT_TYPES = [
    "General Contractor", "Civil / Earthworks Contractor", "Utility / Infrastructure Contractor",
    "Transportation / Logistics", "Energy / Industrial Services", "Government / Institutional",
    "Developer / Construction Manager", "Other Commercial User",
]
SPACE_REQUIREMENTS = [
    "Under 1,000 sq ft", "1,000 - 5,000 sq ft", "5,000 - 10,000 sq ft",
    "10,000 - 25,000 sq ft", "25,000 - 50,000 sq ft", "Full Site / Anchor Requirement",
]
LEASE_TERMS = [
    "Short-Term: Daily / Weekly", "Monthly Rolling", "Seasonal: 3-8 Months",
    "Annual Lease", "Multi-Year: 2-5 Years", "Anchor / Exclusive Site Allocation",
]
AMENITIES = [
    "Controlled Gate Access", "LED Yard Lighting", "CCTV Surveillance", "Engineered Gravel Surface",
    "Wide Drive Aisles", "Maintenance Support", "Long-Term Lease Options",
    "Exclusive / Dedicated Yard Area", "After-Hours Access", "Snow Clearing / Winter Operations",
    "Power Availability",
]
VALUE_OPTIONS = ["Low", "Neutral", "Important", "Strategic", "Critical"]
DEPLOYMENT_WINDOWS = ["June 1 - Immediate Requirement", "Summer 2026", "Fall/Winter 2026", "Flexible / Planning Ahead"]

LAYOUT_FILES = {
    "Under 1,000 sq ft": LAYOUT_DIRECTORY / "layout_under_1000.pdf",
    "1,000 - 5,000 sq ft": LAYOUT_DIRECTORY / "layout_1000_5000.pdf",
    "5,000 - 10,000 sq ft": LAYOUT_DIRECTORY / "layout_5000_10000.pdf",
    "10,000 - 25,000 sq ft": LAYOUT_DIRECTORY / "layout_10000_25000.pdf",
    "25,000 - 50,000 sq ft": LAYOUT_DIRECTORY / "layout_25000_50000.pdf",
    "Full Site / Anchor Requirement": LAYOUT_DIRECTORY / "layout_anchor_site.pdf",
}


def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def get_email_config() -> Tuple[str, str, str, Optional[str]]:
    sender_email = get_secret("SENDER_EMAIL", DEFAULT_SENDER_EMAIL)
    admin_email = get_secret("ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL)
    smtp_username = get_secret("SMTP_USERNAME", sender_email)
    password = get_secret("EMAIL_PASSWORD")
    return sender_email, admin_email, smtp_username, password


def get_booking_link() -> str:
    return get_secret("BOOKING_LINK", DEFAULT_BOOKING_LINK) or ""


def ensure_dirs() -> None:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    GENERATED_DIRECTORY.mkdir(parents=True, exist_ok=True)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip()))


def encode_file_base64(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    try:
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        return None


def apply_global_styles() -> None:
    bg = encode_file_base64(BACKGROUND_IMAGE)
    background_css = (
        f'.stApp {{ background-image: linear-gradient(rgba(0,0,0,.84), rgba(0,0,0,.84)), url("data:image/jpg;base64,{bg}"); background-size: cover; background-position: center; background-attachment: fixed; }}'
        if bg else ".stApp { background-color: #050505; }"
    )
    st.markdown(f"""
    <style>
    {background_css}
    .brand-title {{ text-align:center; font-family:Georgia,serif; font-size:clamp(2.2rem,7vw,4rem); font-weight:300; letter-spacing:.22em; margin:2rem 0 .25rem; background:linear-gradient(to right,#bf953f,#fcf6ba,#b38728,#fbf5b7,#aa771c); -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-transform:uppercase; }}
    .sub-brand {{ text-align:center; color:#d4af37; letter-spacing:.18em; font-size:.82rem; text-transform:uppercase; margin-bottom:2rem; }}
    .gold-text {{ color:#d4af37; font-weight:700; }}
    [data-testid="stForm"] {{ background-color:rgba(0,0,0,.80)!important; border:1px solid #d4af37!important; padding:2rem!important; border-radius:.75rem; box-shadow:0 0 40px rgba(212,175,55,.12); }}
    .eoi-document {{ background-color:rgba(0,0,0,.92); color:#fff; padding:clamp(1.5rem,4vw,3rem); border:1px solid #d4af37; border-radius:.75rem; font-family:Georgia,serif; line-height:1.55; margin-bottom:1.8rem; box-shadow:0 0 40px rgba(212,175,55,.2); }}
    .notice-card {{ background:linear-gradient(145deg,rgba(26,26,26,.95),rgba(0,0,0,.95)); border:2px solid #d4af37; padding:1.8rem; border-radius:1rem; text-align:center; max-width:760px; margin:1.5rem auto; color:#fff; }}
    .diagnostic-card {{ background:rgba(0,0,0,.76); border:1px solid rgba(212,175,55,.65); padding:1rem; border-radius:.75rem; margin-top:1rem; color:#fff; font-size:.9rem; }}
    .privacy-note {{ font-size:.85rem; color:#ccc; border-left:3px solid #d4af37; padding-left:.9rem; margin-top:.75rem; }}
    .stButton>button, .stFormSubmitButton>button {{ background-color:#d4af37!important; color:#000!important; font-weight:800; border-radius:.35rem; min-height:3.4rem; width:100%; border:none; letter-spacing:.12em; text-transform:uppercase; }}
    .stButton>button:hover, .stFormSubmitButton>button:hover {{ background-color:#fff!important; box-shadow:0 0 20px rgba(212,175,55,.8); }}
    label, .stMarkdown, .stRadio, .stSelectbox, .stMultiSelect, .stTextInput, .stCheckbox, .stTextArea {{ color:#fff!important; }}
    </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(f"<div class='brand-title'>{BRAND_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-brand'>{LOCATION_LINE}</div>", unsafe_allow_html=True)


def init_state() -> None:
    st.session_state.setdefault("page", "assessment")
    st.session_state.setdefault("user_data", {})
    st.session_state.setdefault("email_result", None)


def reset_portal() -> None:
    st.session_state.page = "assessment"
    st.session_state.user_data = {}
    st.session_state.email_result = None
    st.rerun()


def format_single_pricing_block(scope: str, pricing: PricingDeal) -> str:
    return f"""{scope}
- Daily: {pricing.daily}
- Weekly: {pricing.weekly}
- Monthly: {pricing.monthly}
- Yearly: {pricing.yearly}
- Multi-Year: {pricing.multi_year}
- Details: {pricing.details}"""


def format_full_pricing_schedule() -> str:
    return "\n\n".join(format_single_pricing_block(scope, pricing) for scope, pricing in PRICING_DEALS.items())


def requested_pricing_block(data: dict) -> str:
    if data.get("send_full_pricing", True):
        return format_full_pricing_schedule()
    scope = data.get("scope")
    return format_single_pricing_block(scope, PRICING_DEALS[scope]) if scope in PRICING_DEALS else format_full_pricing_schedule()


def calculate_lead_score(data: dict) -> Tuple[str, int, str, str]:
    score = 0
    scope = data.get("scope", "")
    space = data.get("space_requirement", "")
    term = data.get("lease_term", "")
    value = data.get("strategic_value", "")
    deployment = da
