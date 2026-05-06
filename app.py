import base64
import html
import logging
import re
import smtplib
import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

APP_TITLE = "EagleView Estates | Private Yard Allocation Portal"
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "Private Yard Allocation Portal • CentrePort Canada • Winnipeg"
BACKGROUND_IMAGE = Path("site_photo.jpg")
LAYOUT_DIRECTORY = Path("layouts")
SITE_LAYOUT_OVERVIEW = Path("site_layout.jpg")

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

LAYOUT_FILES = {
    "Under 1,000 sq ft": LAYOUT_DIRECTORY / "layout_under_1000.pdf",
    "1,000 - 5,000 sq ft": LAYOUT_DIRECTORY / "layout_1000_5000.pdf",
    "5,000 - 10,000 sq ft": LAYOUT_DIRECTORY / "layout_5000_10000.pdf",
    "10,000 - 25,000 sq ft": LAYOUT_DIRECTORY / "layout_10000_25000.pdf",
    "25,000 - 50,000 sq ft": LAYOUT_DIRECTORY / "layout_25000_50000.pdf",
    "Full Site / Anchor Requirement": LAYOUT_DIRECTORY / "layout_anchor_site.pdf",
}

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
- Daily: {pricing.daily}
- Weekly: {pricing.weekly}
- Monthly: {pricing.monthly}
- Yearly: {pricing.yearly}
- Multi-Year: {pricing.multi_year}
- Details: {pricing.details}
""".strip()


def format_full_pricing_schedule() -> str:
    return "\n\n".join(
        format_single_pricing_block(scope, pricing)
        for scope, pricing in PRICING_DEALS.items()
    )


def requested_pricing_block(data: dict) -> str:
    if data.get("send_full_pricing", True):
        return format_full_pricing_schedule()

    scope = data.get("scope")
    if scope in PRICING_DEALS:
        return format_single_pricing_block(scope, PRICING_DEALS[scope])

    return format_full_pricing_schedule()


def calculate_lead_score(data: dict) -> Tuple[str, int, str, str]:
    """Return lead tier, numeric score, follow-up urgency, and pricing strategy."""
    score = 0

    scope = data.get("scope", "")
    space = data.get("space_requirement", "")
    lease_term = data.get("lease_term", "")
    strategic_value = data.get("strategic_value", "")
    deployment = data.get("deployment_window", "")
    amenities = data.get("amenities", [])
    client_type = data.get("client_type", "")

    if "Anchor" in scope or "5-Acre" in scope:
        score += 35
    elif "Dedicated Pad" in scope:
        score += 22
    elif "Flex" in scope:
        score += 15
    else:
        score += 10

    if "Full Site" in space:
        score += 30
    elif "25,000 - 50,000" in space:
        score += 24
    elif "10,000 - 25,000" in space:
        score += 18
    elif "5,000 - 10,000" in space:
        score += 12
    elif "1,000 - 5,000" in space:
        score += 8

    if "Anchor" in lease_term or "Multi-Year" in lease_term:
        score += 24
    elif "Annual" in lease_term:
        score += 16
    elif "Seasonal" in lease_term:
        score += 10
    elif "Monthly" in lease_term:
        score += 6

    if strategic_value == "Critical":
        score += 16
    elif strategic_value == "Strategic":
        score += 12
    elif strategic_value == "Important":
        score += 8

    if "Immediate" in deployment:
        score += 10
    elif "Summer" in deployment:
        score += 7

    if "Exclusive / Dedicated Yard Area" in amenities:
        score += 8
    if "After-Hours Access" in amenities:
        score += 4
    if "Power Availability" in amenities:
        score += 4

    if client_type in {"Government / Institutional", "Energy / Industrial Services", "Utility / Infrastructure Contractor"}:
        score += 8

    if score >= 95:
        return "Tier A+ / Anchor Prospect", score, "Same-day executive follow-up recommended", "Do not rely on standard schedule only. Offer custom allocation review and term pricing."
    if score >= 75:
        return "Tier A / High-Value Commercial Prospect", score, "Follow up within 24 hours", "Quote preliminary framework, then move toward custom lease structure."
    if score >= 50:
        return "Tier B / Qualified Commercial Prospect", score, "Follow up within 48 hours", "Use standard schedule with opportunity to adjust for size and term."
    return "Tier C / General Inquiry", score, "Follow up as capacity allows", "Use standard pricing schedule and qualify further before reserving space."


def estimate_monthly_value(data: dict) -> str:
    scope = data.get("scope", "")
    space = data.get("space_requirement", "")

    if "Full Site" in space or "5-Acre" in scope:
        return "$9,500 - $14,500+/month before custom terms"
    if "25,000 - 50,000" in space:
        return "$8,500 - $30,000+/month depending on rate structure and exclusivity"
    if "10,000 - 25,000" in space:
        return "$5,000 - $18,000/month depending on access, surface, and term"
    if "5,000 - 10,000" in space:
        return "$3,500 - $9,500/month depending on use case"
    if "1,000 - 5,000" in space:
        return "$2,250 - $4,500/month typical dedicated pad range"
    return "To be confirmed after site allocation review"


def get_layout_file(data: dict) -> Optional[Path]:
    """Return the matching preliminary layout exhibit for the requested size band."""
    return LAYOUT_FILES.get(data.get("space_requirement", ""))


def make_safe_attachment_name(data: dict) -> str:
    """Create a clean, professional attachment filename for size-specific PDF exhibits."""
    space = data.get("space_requirement", "allocation").lower()
    safe_space = re.sub(r"[^a-z0-9]+", "_", space).strip("_")
    return f"EagleView_Preliminary_Yard_Allocation_Exhibit_{safe_space}.pdf"


def attach_file(
    message: MIMEMultipart,
    file_path: Path,
    display_name: str,
    mime_subtype: str = "octet-stream",
) -> Tuple[bool, str]:
    """Attach a local file to an email without failing the submission if unavailable."""
    if not file_path.exists():
        return False, f"File missing: {file_path}"

    try:
        with file_path.open("rb") as file:
            part = MIMEApplication(file.read(), _subtype=mime_subtype, Name=display_name)

        part["Content-Disposition"] = f'attachment; filename="{display_name}"'
        message.attach(part)
        return True, f"Attached: {file_path}"
    except Exception as exc:
        logger.exception("Failed to attach file")
        return False, f"Attachment error for {file_path}: {type(exc).__name__}: {exc}"


def attach_layout_exhibit(message: MIMEMultipart, data: dict) -> Tuple[bool, str]:
    """Attach the matching size-specific layout PDF if the file exists."""
    layout_file = get_layout_file(data)

    if not layout_file:
        return False, "No layout template mapped for selected space requirement."

    return attach_file(
        message=message,
        file_path=layout_file,
        display_name=make_safe_attachment_name(data),
        mime_subtype="pdf",
    )


def attach_site_layout_overview(message: MIMEMultipart) -> Tuple[bool, str]:
    """Attach the universal EagleView site layout overview image to every client email."""
    return attach_file(
        message=message,
        file_path=SITE_LAYOUT_OVERVIEW,
        display_name="EagleView_Site_Layout_Overview.jpg",
        mime_subtype="octet-stream",
    )


def build_admin_email(data: dict, sender_email: str, admin_email: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = f"EagleView Portal <{sender_email}>"
    msg["To"] = admin_email
    msg["Subject"] = f"New EOI Submission: {data['name']}"

    amenities = ", ".join(data.get("amenities", [])) or "None selected"

    body = f"""
New Expression of Interest received.

Company / Representative: {data['name']}
Email: {data['email']}
Client Type: {data.get('client_type', 'N/A')}
Operational Scope: {data['scope']}
Space Requirement: {data.get('space_requirement', 'N/A')}
Preferred Lease Term: {data.get('lease_term', 'N/A')}
Full Pricing Schedule Requested: {'Yes' if data.get('send_full_pricing', True) else 'No'}
Strategic Value: {data['strategic_value']}
Target Deployment: {data['deployment_window']}
Amenities: {amenities}
Project / Use Notes: {data.get('project_notes', 'N/A')}
Digital Signature: {data.get('signature', 'N/A')}

Preliminary Layout Exhibits:
Universal Overview Exhibit: {SITE_LAYOUT_OVERVIEW}
Universal Overview Expected: Yes
Requested Size-Specific Exhibit File: {get_layout_file(data) or 'No mapped layout file'}
Size-Specific Attachment Expected: {'Yes' if get_layout_file(data) else 'No'}

Internal Lead Review:
Lead Tier: {calculate_lead_score(data)[0]}
Lead Score: {calculate_lead_score(data)[1]}/125
Follow-Up Urgency: {calculate_lead_score(data)[2]}
Recommended Pricing Strategy: {calculate_lead_score(data)[3]}
Estimated Monthly Value: {estimate_monthly_value(data)}

Pricing Sent To Prospect:
{requested_pricing_block(data)}

Notes:
This is an expression of interest only. No lease has been executed through the portal.
""".strip()

    msg.attach(MIMEText(body, "plain"))
    return msg


def build_client_email(data: dict, sender_email: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = f"EagleView Estates <{sender_email}>"
    msg["To"] = data["email"]
    msg["Subject"] = "EagleView Estates: Preliminary Yard Leasing Framework"

    pricing_intro = (
        "Complete current pricing schedule:"
        if data.get("send_full_pricing", True)
        else f"Current pricing indication for {data['scope']}:"
    )

    body = f"""
Hello {data['name']},

Thank you for submitting your private yard allocation request for EagleView Estates.

Our team has received the following preliminary requirement:
- Client Type: {data.get('client_type', 'To be confirmed')}
- Operational Scope: {data['scope']}
- Approximate Space Requirement: {data.get('space_requirement', 'To be confirmed')}
- Preferred Lease Term: {data.get('lease_term', 'To be confirmed')}
- Target Deployment Window: {data.get('deployment_window', 'To be confirmed')}

{pricing_intro}
{requested_pricing_block(data)}

Attached Exhibits:
A preliminary EagleView site layout overview has been attached for every request. Where available, a size-specific yard allocation exhibit may also be included. These visuals are conceptual only and are intended to support preliminary leasing review.

Commercial Notes:
The above is a preliminary leasing framework only. Larger allocations, exclusive-use areas, infrastructure users, project-based staging requirements, and multi-year commitments may be reviewed under a custom site allocation and term-pricing structure.

Important Disclaimer:
This submission confirms interest only. Pricing is indicative and subject to site availability, final yard configuration, access requirements, operating intensity, lease term, insurance requirements, security requirements, municipal approvals where applicable, and final lease documentation. No lease, reservation, or binding commitment is created until a formal agreement is reviewed and executed by both parties.

Next Step:
For larger or time-sensitive requirements, EagleView may complete a private site allocation review and confirm whether the requested yard area can be accommodated.

Best regards,
The EagleView Estates Team
""".strip()

    msg.attach(MIMEText(body, "plain"))

    overview_attached, overview_status = attach_site_layout_overview(msg)
    size_attached, size_status = attach_layout_exhibit(msg, data)

    msg["X-EagleView-Site-Overview"] = "attached" if overview_attached else "not-attached"
    msg["X-EagleView-Site-Overview-Status"] = overview_status[:900]
    msg["X-EagleView-Size-Layout-Exhibit"] = "attached" if size_attached else "not-attached"
    msg["X-EagleView-Size-Layout-Status"] = size_status[:900]

    return msg


def send_one_message(
    server: smtplib.SMTP,
    message: MIMEMultipart,
    from_addr: str,
    to_addrs: List[str],
) -> Tuple[bool, str]:
    try:
        refused = server.sendmail(from_addr, to_addrs, message.as_string())
        if refused:
            return False, f"Recipient refused by SMTP server: {refused}"
        return True, ""
    except Exception as exc:
        logger.exception("Email send failed")
        return False, f"{type(exc).__name__}: {exc}"


def send_emails_with_diagnostics(data: dict) -> EmailSendResult:
    sender_email, admin_email, smtp_username, password = get_email_config()

    result = EmailSendResult(
        smtp_username=smtp_username or "",
        sender_email=sender_email or "",
        admin_email=admin_email or "",
        client_email=data.get("email", ""),
    )

    if not password:
        msg = "Missing EMAIL_PASSWORD in Streamlit secrets."
        result.client_error = msg
        result.admin_error = msg
        return result

    if not sender_email or not admin_email or not smtp_username:
        msg = "Missing SENDER_EMAIL, ADMIN_EMAIL, or SMTP_USERNAME."
        result.client_error = msg
        result.admin_error = msg
        return result

    if data.get("scope") not in PRICING_DEALS:
        msg = "Selected operational scope does not exist in PRICING_DEALS."
        result.client_error = msg
        result.admin_error = msg
        return result

    client_msg = build_client_email(data, sender_email)
    admin_msg = build_admin_email(data, sender_email, admin_email)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(smtp_username, password)

            client_recipients = [data["email"], admin_email]
            result.client_sent, result.client_error = send_one_message(
                server=server,
                message=client_msg,
                from_addr=sender_email,
                to_addrs=client_recipients,
            )

            result.admin_sent, result.admin_error = send_one_message(
                server=server,
                message=admin_msg,
                from_addr=sender_email,
                to_addrs=[admin_email],
            )

    except smtplib.SMTPAuthenticationError as exc:
        error = f"SMTPAuthenticationError: {exc}. Check Gmail app password / SMTP_USERNAME."
        result.client_error = error
        result.admin_error = error
        logger.exception("SMTP authentication failed")
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        result.client_error = error
        result.admin_error = error
        logger.exception("SMTP connection/login failed")

    return result


def render_email_diagnostics(result: EmailSendResult) -> None:
    st.markdown(
        f"""
        <div class='diagnostic-card'>
            <b>Email Diagnostic</b><br>
            SMTP Username: {html.escape(result.smtp_username)}<br>
            Sender Email: {html.escape(result.sender_email)}<br>
            Client Email: {html.escape(result.client_email)}<br>
            Admin / Verification Copy: {html.escape(result.admin_email)}<br>
            Client Confirmation Accepted by SMTP: {'YES' if result.client_sent else 'NO'}<br>
            Admin EOI Accepted by SMTP: {'YES' if result.admin_sent else 'NO'}<br>
            Client Error: {html.escape(result.client_error or 'None')}<br>
            Admin Error: {html.escape(result.admin_error or 'None')}
        </div>
        """,
        unsafe_allow_html=True,
    )


def assessment_page() -> None:
    render_header()

    with st.form("assessment_form", clear_on_submit=False):
        st.markdown("### <span class='gold-text'>Private Yard Allocation Request</span>", unsafe_allow_html=True)
        st.caption("For contractors, infrastructure operators, fleet users, and commercial tenants seeking secured yard space.")

        client_type = st.selectbox("1. Client / Organization Type", CLIENT_TYPES)
        scope = st.selectbox("2. Operational Scope", list(PRICING_DEALS.keys()))
        space_requirement = st.selectbox("3. Approximate Space Requirement", SPACE_REQUIREMENTS)
        lease_term = st.selectbox("4. Preferred Lease Structure", LEASE_TERMS)

        send_full_pricing = st.checkbox(
            "Send me the complete pricing schedule for all storage options",
            value=True,
            help="Recommended. The confirmation email will include the full EagleView Estates pricing schedule.",
        )

        strategic_value = st.select_slider("5. Strategic Value of Location", options=VALUE_OPTIONS)
        deployment_window = st.radio("6. Target Deployment Date", DEPLOYMENT_WINDOWS)
        amenities = st.multiselect("7. Critical Site Requirements", AMENITIES)
        project_notes = st.text_area(
            "8. Project / Fleet Requirement Notes",
            placeholder="Example: equipment type, number of units, access frequency, desired yard configuration, security requirements, or project timeline.",
            height=120,
        )

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
            "client_type": client_type,
            "scope": scope,
            "space_requirement": space_requirement,
            "lease_term": lease_term,
            "send_full_pricing": send_full_pricing,
            "strategic_value": strategic_value,
            "deployment_window": deployment_window,
            "amenities": amenities,
            "project_notes": project_notes.strip(),
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
    pricing_mode = "Complete pricing schedule" if data.get("send_full_pricing", True) else "Selected scope pricing only"

    st.markdown(
        f"""
        <div class='eoi-document'>
            <h2 style='text-align:center; color:#d4af37; text-transform:uppercase;'>Private Yard Allocation Request</h2>
            <p><span class='gold-text'>Prospective Tenant:</span> {name_safe}</p>
            <hr style='border: 0.5px solid #d4af37;'>
            <p><b>1. Client Type:</b> {html.escape(data.get('client_type', 'To be confirmed'))}</p>
            <p><b>2. Scope:</b> Requirement identified for <span class='gold-text'>{scope_safe}</span>.</p>
            <p><b>3. Space Requirement:</b> {html.escape(data.get('space_requirement', 'To be confirmed'))}</p>
            <p><b>4. Lease Structure:</b> {html.escape(data.get('lease_term', 'To be confirmed'))}</p>
            <p><b>5. Target Window:</b> {deployment_safe}</p>
            <p><b>6. Critical Requirements:</b> {amenities_safe}</p>
            <p><b>7. Pricing Email:</b> {html.escape(pricing_mode)}</p>
            <p><b>8. Non-Binding Acknowledgement:</b> This request is not a lease, reservation, or binding commitment. Final terms remain subject to availability, formal lease documentation, site readiness, municipal requirements where applicable, and mutual approval.</p>
            <p style='font-size:0.9rem; color:#bbbbbb; margin-top:1.5rem;'><i>By signing below, you confirm interest in receiving preliminary leasing information and, where applicable, a private site allocation review based on current availability.</i></p>
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
        if st.button("Submit Allocation Request"):
            if not signature.strip():
                st.warning("Please enter your full name and title as a digital signature.")
                return

            st.session_state.user_data["signature"] = signature.strip()
            result = send_emails_with_diagnostics(st.session_state.user_data)
            st.session_state.email_result = result

            if result.client_sent and result.admin_sent:
                st.session_state.page = "thankyou"
                st.rerun()

            st.error("Email delivery failed or partially failed. Diagnostic details are below.")
            render_email_diagnostics(result)


def thankyou_page() -> None:
    render_header()
    result: Optional[EmailSendResult] = st.session_state.get("email_result")

    st.markdown("<div style='text-align:center; margin-top:2rem; font-size:4rem;'>✔️</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='color:#d4af37; font-size:1.8rem; text-align:center; letter-spacing:0.22em; margin-bottom:1rem; text-transform:uppercase;'>
            EOI Verified
        </div>
        <div class='notice-card'>
            <h4 style='color:#d4af37; margin-top:0; text-transform:uppercase; letter-spacing:0.12em;'>Allocation Request Received</h4>
            <p>Your preliminary leasing framework has been accepted by the mail server.</p>
            <p>A verification copy was also sent to EagleView for internal review and follow-up.</p>
            <p>If the confirmation package does not arrive shortly, check your <b style='color:#d4af37;'>Junk/Spam folder</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Submit Another Allocation Request"):
        reset_portal()


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
