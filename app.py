import base64
import html
import logging
import os
import re
import smtplib
import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional

import streamlit as st

# ============================================================
# EagleView Estates | Expression of Interest Portal
# Upgraded Streamlit single-file app
# ============================================================

APP_TITLE = "EagleView Estates | EOI Portal"
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "CentrePort Canada • Winnipeg"
BACKGROUND_IMAGE = Path("site_photo.jpg")

SENDER_EMAIL = "info@eagleviewearthworks.com"
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


FULL_PRICING_REQUEST_LABEL = "📄 Send Full Pricing Schedule"

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


# -----------------------------
# Page setup and styling
# -----------------------------

st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon=APP_ICON)


def encode_file_base64(path: Path) -> Optional[str]:
    """Return a base64 string for a local file, or None if unavailable."""
    try:
        if not path.exists():
            return None
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except OSError as exc:
        logger.warning("Unable to read background image %s: %s", path, exc)
        return None


def apply_global_styles() -> None:
    """Apply the branded page background and CSS."""
    bg_image = encode_file_base64(BACKGROUND_IMAGE)

    if bg_image:
        background_css = f'''
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.82)), url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        '''
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

        label, .stMarkdown, .stRadio, .stSelectbox, .stMultiSelect, .stTextInput {{
            color: #ffffff !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(f"<div class='brand-title'>{BRAND_NAME}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-brand'>{LOCATION_LINE}</div>", unsafe_allow_html=True)


# -----------------------------
# Validation and state helpers
# -----------------------------


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip()))


def clean_text(value: str) -> str:
    """Trim user input and keep it safe for HTML rendering."""
    return html.escape(value.strip())


def initialize_state() -> None:
    st.session_state.setdefault("page", "assessment")
    st.session_state.setdefault("user_data", {})
    st.session_state.setdefault("email_sent", False)


def reset_portal() -> None:
    st.session_state.page = "assessment"
    st.session_state.user_data = {}
    st.session_state.email_sent = False
    st.rerun()


# -----------------------------
# Email handling
# -----------------------------


def get_email_password() -> Optional[str]:
    """Read the email password from Streamlit secrets."""
    try:
        return st.secrets.get("EMAIL_PASSWORD")
    except Exception:
        return None


def format_single_pricing_block(scope: str, pricing: PricingDeal) -> str:
    return f"""
{scope}
- Daily: {pricing.daily}
- Weekly: {pricing.weekly}
- Monthly: {pricing.monthly}
- Yearly: {pricing.yearly}
- Multi-Year: {pricing.multi_year}
- Details: {pricing.details}
""".strip()


def format_full_pricing_schedule() -> str:
    blocks = [format_single_pricing_block(scope, pricing) for scope, pricing in PRICING_DEALS.items()]
    return "\n\n".join(blocks)


def is_full_pricing_request(data: dict) -> bool:
    return data.get("scope") == FULL_PRI


def build_client_email(data: dict, pricing: PricingDeal) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = f"EagleView Estates <{SENDER_EMAIL}>"
    msg["To"] = data["email"]
    msg["Subject"] = "EagleView Estates: Priority Pricing & Site Interest Confirmation"

    body = f"""
Hello {data['name']},

Thank you for submitting your Statement of Interest for EagleView Estates.

Selected site requirement:
{data['scope']}

Current pricing indication:
- Daily: {pricing.daily}
- Weekly: {pricing.weekly}
- Monthly: {pricing.monthly}
- Yearly: {pricing.yearly}
- Multi-Year: {pricing.multi_year}

Site notes:
{pricing.details}

Important disclaimer:
This submission confirms interest only. Pricing is indicative and subject to availability, final site configuration, operating requirements, lease terms, and market conditions. No lease, reservation, or binding commitment is created until a formal agreement is reviewed and executed by both parties.

Best regards,
The EagleView Estates Team
""".strip()

    msg.attach(MIMEText(body, "plain"))
    return msg


def send_emails(data: dict) -> bool:
    """Send admin notification and client confirmation email."""
    pricing = PRICING_DEALS.get(data.get("scope"))
    password = get_email_password()

    if not pricing:
        st.error("Pricing package could not be found. Please restart the form and try again.")
        return False

    if not password:
        st.error("Email is not configured. Add EMAIL_PASSWORD to Streamlit secrets.")
        return False

    try:
        admin_msg = build_admin_email(data, pricing)
        client_msg = build_client_email(data, pricing)

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SENDER_EMAIL, password)
            server.send_message(admin_msg)
            server.send_message(client_msg)

        logger.info("EOI emails sent successfully for %s", data["email"])
        return True

    except smtplib.SMTPAuthenticationError:
        logger.exception("SMTP authentication failed")
        st.error("Email authentication failed. Check the sender account and Streamlit secret.")
        return False
    except smtplib.SMTPException as exc:
        logger.exception("SMTP error: %s", exc)
        st.error("The submission was received, but the email could not be sent. Please contact EagleView directly.")
        return False
    except Exception as exc:
        logger.exception("Unexpected email error: %s", exc)
        st.error("An unexpected error occurred while sending the email.")
        return False


# -----------------------------
# Pages
# -----------------------------


def assessment_page() -> None:
    render_header()

    with st.form("assessment_form", clear_on_submit=False):
        st.markdown("### <span class='gold-text'>Strategic Site Assessment</span>", unsafe_allow_html=True)

        scope = st.selectbox("1. Operational Scope", list(PRICING_DEALS.keys()))
        strategic_value = st.select_slider("2. Strategic Value of Location", options=VALUE_OPTIONS)
        deployment_window = st.radio("3. Target Deployment Date", DEPLOYMENT_WINDOWS)
        amenities = st.multiselect("4. Critical Site Amenities", AMENITIES)

        name = st.text_input("Company / Representative Name", placeholder="Example: ABC Contracting Ltd.")
        email = st.text_input("Direct Email", placeholder="name@company.com")

        submitted = st.form_submit_button("Validate & Continue")

    if submitted:
        name_clean = name.strip()
        email_clean = email.strip().lower()

        if not name_clean:
            st.warning("Please enter a company or representative name.")
            return

        if not is_valid_email(email_clean):
            st.warning("Please enter a valid email address.")
            return

        st.session_state.user_data = {
            "name": name_clean,
            "email": email_clean,
            "scope": scope,
            "strategic_value": strategic_value,
            "deployment_window": deployment_window,
            "amenities": amenities,
        }
        st.session_state.page = "eoi"
        st.rerun()


def eoi_page() -> None:
    data = st.session_state.get("user_data", {})
    if not data:
        reset_portal()
        return

    render_header()

    name_safe = clean_text(data.get("name", ""))
    scope_safe = clean_text(data.get("scope", ""))
    deployment_safe = clean_text(data.get("deployment_window", ""))
    amenities_safe = html.escape(", ".join(data.get("amenities", [])) or "To be confirmed")

    st.markdown(
        f"""
        <div class='eoi-document'>
            <h2 style='text-align:center; color:#d4af37; text-transform:uppercase;'>Statement of Interest</h2>
            <p><span class='gold-text'>Prospective Tenant:</span> {name_safe}</p>
            <hr style='border: 0.5px solid #d4af37;'>
            <p><b>1. Scope:</b> Requirement identified for <span class='gold-text'>{scope_safe}</span>.</p>
            <p><b>2. Target Window:</b> {deployment_safe}</p>
            <p><b>3. Requested Amenities:</b> {amenities_safe}</p>
            <p><b>4. Pricing:</b> Indicative pricing will be emailed after submission.</p>
            <p><b>5. Non-Binding Acknowledgement:</b> This Statement of Interest is not a lease, reservation, or binding commitment. Final terms remain subject to availability, formal lease documentation, site readiness, and mutual approval.</p>
            <p style='font-size:0.9rem; color:#bbbbbb; margin-top:1.5rem;'><i>By signing below, you confirm interest in receiving formal leasing information based on current site availability.</i></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    signature = st.text_input("Digital Signature", placeholder="Full name and title")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.page = "assessment"
            st.rerun()

    with col2:
        if st.button("Execute & Unlock Pricing"):
            if not signature.strip():
                st.warning("Please enter your full name and title as a digital signature.")
                return

            st.session_state.user_data["signature"] = signature.strip()
            success = send_emails(st.session_state.user_data)
            st.session_state.email_sent = success
            st.session_state.page = "thankyou"
            st.rerun()


def thankyou_page() -> None:
    render_header()

    if st.session_state.get("email_sent"):
        st.markdown("<div style='text-align:center; margin-top:2rem; font-size:4rem;'>✔️</div>", unsafe_allow_html=True)
        status = "EOI Verified"
        message = "Your pricing package has been sent to the email provided."
    else:
        st.markdown("<div style='text-align:center; margin-top:2rem; font-size:4rem;'>⚠️</div>", unsafe_allow_html=True)
        status = "EOI Recorded"
        message = "Your information was captured, but the email confirmation may not have been delivered."

    st.markdown(
        f"""
        <div style='color:#d4af37; font-size:1.8rem; text-align:center; letter-spacing:0.22em; margin-bottom:1rem; text-transform:uppercase;'>
            {status}
        </div>
        <div class='notice-card'>
            <h4 style='color:#d4af37; margin-top:0; text-transform:uppercase; letter-spacing:0.12em;'>Next Step</h4>
            <p>{message}</p>
            <p>If your pricing package does not arrive shortly, check your <b style='color:#d4af37;'>Junk/Spam folder</b>.</p>
            <p>Mark the email as <b style='color:#d4af37;'>Not Junk</b> so future lease documents and site updates are delivered properly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Submit Another EOI"):
        reset_portal()


# -----------------------------
# App router
# -----------------------------


def main() -> None:
    initialize_state()
    apply_global_styles()

    page = st.session_state.get("page", "assessment")

    if page == "assessment":
        assessment_page()
    elif page == "eoi":
        eoi_page()
    elif page == "thankyou":
        thankyou_page()
    else:
        reset_portal()


if __name__ == "__main__":
    main()
