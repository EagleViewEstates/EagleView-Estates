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
# Enterprise-grade Streamlit master code
# ============================================================

APP_TITLE = "EagleView Estates | Private Yard Allocation Portal"
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "Private Yard Allocation Portal • CentrePort Canada • Winnipeg"

BACKGROUND_IMAGE = Path("site_photo.jpg")
SITE_LAYOUT_OVERVIEW = Path("site_layout.jpg")
LAYOUT_DIRECTORY = Path("layouts")
DATA_DIRECTORY = Path("data")
LEAD_CSV_FILE = DATA_DIRECTORY / "eagleview_leads.csv"
GENERATED_DIRECTORY = Path("generated")

DEFAULT_SENDER_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_ADMIN_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_BOOKING_LINK = ""

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon=APP_ICON)


# ============================================================
# Data models
# ============================================================

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
    overview_attached: bool
    overview_status: str
    size_layout_attached: bool
    size_layout_status: str
    leasing_pdf_attached: bool
    leasing_pdf_status: str


# ============================================================
# Pricing / options
# ============================================================

PRICING_DEALS: Dict[str, PricingDeal] = {
    "💎 Anchor Tenant: 5-Acre Parcel": PricingDeal(
        daily="$1,000 - $1,500/day",
        weekly="$4,500 - $6,500/week",
        monthly="$9,500 - $14,500/month",
        yearly="$110k - $155k/annum",
        multi_year="Custom institutional quote",
        details="Full 5-acre integrated site with exclusive controlled gate access.",
    ),
    "Dedicated Pad: 1,000 - 5,000 sq ft": PricingDeal(
        daily="$150 - $350/day",
        weekly="$900 - $1,500/week",
        monthly="$2,250 - $4,500/month",
        yearly="$28k - $45k/annum",
        multi_year="$25k - $38k/annum, 3+ year term",
        details="Engineered gravel pad with dedicated lighting and surveillance coverage.",
    ),
    "Flex Staging / Short-Term Laydown": PricingDeal(
        daily="$350 - $550/day",
        weekly="$1,800 - $2,800/week",
        monthly="$5,000 - $7,500/month",
        yearly="Available by quote",
        multi_year="Available by quote",
        details="Rapid-access staging for project material laydown, fleet positioning, and short-term contractor use.",
    ),
    "Winter Equipment Storage": PricingDeal(
        daily="N/A",
        weekly="N/A",
        monthly="$1,200 - $2,100/month",
        yearly="$12,500 - $18,000 seasonal, October-May",
        multi_year="Fleet-volume discounts available",
        details="Seasonal storage for equipment, trailers, attachments, and contractor assets.",
    ),
}

AMENITIES = [
    "Controlled Gate Access",
    "LED Yard Lighting",
    "CCTV Surveillance",
    "Engineered Gravel Surface",
    "Wide Drive Aisles",
    "Maintenance Support",
    "Long-Term Lease Options",
    "Exclusive / Dedicated Yard Area",
    "After-Hours Access",
    "Snow Clearing / Winter Operations",
    "Power Availability",
]

LEASE_TERMS = [
    "Short-Term: Daily / Weekly",
    "Monthly Rolling",
    "Seasonal: 3-8 Months",
    "Annual Lease",
    "Multi-Year: 2-5 Years",
    "Anchor / Exclusive Site Allocation",
]

SPACE_REQUIREMENTS = [
    "Under 1,000 sq ft",
    "1,000 - 5,000 sq ft",
    "5,000 - 10,000 sq ft",
    "10,000 - 25,000 sq ft",
    "25,000 - 50,000 sq ft",
    "Full Site / Anchor Requirement",
]

CLIENT_TYPES = [
    "General Contractor",
    "Civil / Earthworks Contractor",
    "Utility / Infrastructure Contractor",
    "Transportation / Logistics",
    "Energy / Industrial Services",
    "Government / Institutional",
    "Developer / Construction Manager",
    "Other Commercial User",
]

VALUE_OPTIONS = ["Low", "Neutral", "Important", "Strategic", "Critical"]

DEPLOYMENT_WINDOWS = [
    "June 1 - Immediate Requirement",
    "Summer 2026",
    "Fall/Winter 2026",
    "Flexible / Planning Ahead",
]

LAYOUT_FILES = {
    "Under 1,000 sq ft": LAYOUT_DIRECTORY / "layout_under_1000.pdf",
    "1,000 - 5,000 sq ft": LAYOUT_DIRECTORY / "layout_1000_5000.pdf",
    "5,000 - 10,000 sq ft": LAYOUT_DIRECTORY / "layout_5000_10000.pdf",
    "10,000 - 25,000 sq ft": LAYOUT_DIRECTORY / "layout_10000_25000.pdf",
    "25,000 - 50,000 sq ft": LAYOUT_DIRECTORY / "layout_25000_50000.pdf",
    "Full Site / Anchor Requirement": LAYOUT_DIRECTORY / "layout_anchor_site.pdf",
}


# ============================================================
# Secrets / config helpers
# ============================================================

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


# ============================================================
# General helpers
# ============================================================

def encode_file_base64(path: Path) -> Optional[str]:
    try:
        if not path.exists():
            return None
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except OSError as exc:
        logger.warning("Unable to read background image %s: %s", path, exc)
        return None


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip()))


def clean_text(value: str) -> str:
    return html.escape(value.strip())


def initialize_state() -> None:
    st.session_state.setdefault("page", "assessment")
    st.session_state.setdefault("user_data", {})
    st.session_state.setdefault("email_result", None)


def reset_portal() -> None:
    st.session_state.page = "assessment"
    st.session_state.user_data = {}
    st.session_state.email_result = None
    st.rerun()


def ensure_runtime_directories() -> None:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    GENERATED_DIRECTORY.mkdir(parents=True, exist_ok=True)


# ============================================================
# Styling
# ============================================================

def apply_global_styles() -> None:
    bg_image = encode_file_base64(BACKGROUND_IMAGE)

    if bg_image:
        background_css = f"""
        .stApp {{
            background-imag
