import base64
import html
import logging
import re
import smtplib
import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

APP_TITLE = "EagleView Estates | EOI Portal"
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "CentrePort Canada • Winnipeg"
BACKGROUND_IMAGE = Path("site_photo.jpg")

DEFAULT_SENDER_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_ADMIN_EMAIL = "info@eagleviewearthworks.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


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
]

DEPLOYMENT_WINDOWS = [
    "June 1 - Immediate Requirement",
    "Summer 2026",
    "Fall/Winter 2026",
    "Flexible / Planning Ahead",
]

VALUE_OPTIONS = ["Low", "Neutral", "Important", "Strategic", "Critical"]


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


st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon=APP_ICON)


def encode_file_base64(path: Path) -> Optional[str]:
    try:
        if not path.exists():
            return None
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except OSError as exc:
        logger.warning("Unable to read background image %s: %s", path, exc)
        return None


def apply_global_styles() -> None:
    bg_image = encode_file_base64(BACKGROUND_IMAGE)

    if bg_image:
        background_css = f"""
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.82)), url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    else:
        background_css = ".stApp { background-color: #050505; }"

    st.markdown(
        f"""
        <style>
        {background_css}

        .brand-title {{
            text-align: center;
            font-family: Georgia, 'Times New Roman', serif;
            font-size: clamp(2.2rem, 7vw, 4rem);
            font-weight: 300;
            letter-spacing: 0.22em;
            margin: 2rem 0 0.25rem 0;
            background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
        }}

        .sub-brand {{
            text-align: center;
            color: #d4af37;
            letter-spacing: 0.28em;
            font-size: 0.82rem;
            text-transform: uppercase;
            margin-bottom: 2rem;
        }}

        .gold-text {{ color: #d4af37; font-weight: 700; }}

        [data-testid="stForm"] {{
            background-color: rgba(0, 0, 0, 0.78) !important;
            border: 1px solid #d4af37 !important;
            padding: 2rem !important;
            border-radius: 0.75rem;
            box-shadow: 0 0 40px rgba(212, 175, 55, 0.12);
        }}

        .eoi-document {{
            background-color: rgba(0, 0, 0, 0.90);
            color: #ffffff;
            padding: clamp(1.5rem, 4vw, 3rem);
            border: 1px solid #d4af37;
            border-radius: 0.75rem;
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.55;
            margin-bottom: 1.8rem;
            box-shadow: 0 0 40px rgba(212, 175, 55, 0.2);
        }}

        .notice-card {{
            background: linear-gradient(145deg, rgba(26,26,26,0.95), rgba(0,0,0,0.95));
            border: 2px solid #d4af37;
            padding: 1.8rem;
            border-radius: 1rem;
            text-align: center;
            max-width: 680px;
            margin: 1.5rem auto;
            color: #ffffff;
        }}

        .diagnostic-card {{
            background-color: rgba(0, 0, 0, 0.76);
            border: 1px solid rgba(212, 175, 55, 0.65);
            padding: 1rem;
            border-radius: 0.75rem;
            margin-top: 1rem;
            color: #ffffff;
            font-size: 0.9rem;
        }}

        .stButton > button, .stFormSubmitButton > button {{
            background-color: #d4af37 !important;
            color: #000000 !important;
            font-weight: 800;
            border-radius: 0.35rem;
            min-height: 3.4rem;
            width: 100%;
            border: none;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            background-color: #ffffff !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.8);
        }}

        label, .stMarkdown, .stRadio, .stSelectbox, .stMultiSelect, .stTextInput, .stCheckbox {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(f"<div class='brand-title'>{BRAND_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-brand'>{LOCATION_LINE}</div>", unsafe_allow_html=True)


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


def format_single_pricing_block(scope: str, pricing: PricingDeal) -> str:
    return f"""
{scope}
- Daily: {
