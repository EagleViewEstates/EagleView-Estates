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
# EagleView Estates | Expression of Interest Portal
# Final master code with tagline
# ============================================================

APP_TITLE = "EagleView Estates | Storage. Done your way."
APP_ICON = "🦅"
BRAND_NAME = "EagleView Estates"
LOCATION_LINE = "Storage. Done your way. • Expression of Interest Portal • CentrePort Canada • Winnipeg"

BACKGROUND_IMAGE = Path("site_photo.jpg")
SITE_LAYOUT_OVERVIEW = Path("site_layout.pdf")
LEASING_AGREEMENT_PDF = Path("EagleView_Preliminary_Leasing_Agreement.pdf")
LAYOUT_DIRECTORY = Path("layouts")
DATA_DIRECTORY = Path("data")
LEAD_CSV_FILE = DATA_DIRECTORY / "eagleview_leads.csv"

DEFAULT_SENDER_EMAIL = "info@eagleviewearthworks.com"
DEFAULT_ADMIN_EMAIL = "info@eagleviewearthworks.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
MAX_ATTACHMENT_MB = 10
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
class AttachmentStatus:
    overview_attached: bool = False
    overview_status: str = ""
    leasing_agreement_attached: bool = False
    leasing_agreement_status: str = ""
    size_layout_attached: bool = False
    size_layout_status: str = ""


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
        "$1,000 - $1,500/day",
        "$4,500 - $6,500/week",
        "$9,500 - $14,500/month",
        "$110k - $155k/annum",
        "Custom institutional quote",
        "Full 5-acre integrated site with exclusive controlled gate access.",
    ),
    "Dedicated Pad: 1,000 - 5,000 sq ft": PricingDeal(
        "$150 - $350/day",
        "$900 - $1,500/week",
        "$2,250 - $4,500/month",
        "$28k - $45k/annum",
        "$25k - $38k/annum, 3+ year term",
        "Engineered gravel pad with dedicated lighting and surveillance coverage.",
    ),
    "Flex Staging / Short-Term Laydown": PricingDeal(
        "$350 - $550/day",
        "$1,800 - $2,800/week",
        "$5,000 - $7,500/month",
        "Available by quote",
        "Available by quote",
        "Rapid-access staging for project material laydown, fleet positioning, and short-term contractor use.",
    ),
    "Winter Equipment Storage": PricingDeal(
        "N/A",
        "N/A",
        "$1,200 - $2,100/month",
        "$12,500 - $18,000 seasonal, October-May",
        "Fleet-volume discounts available",
        "Seasonal storage for equipment, trailers, attachments, and contractor assets.",
    ),
}

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

SPACE_REQUIREMENTS = [
    "Under 1,000 sq ft",
    "1,000 - 5,000 sq ft",
    "5,000 - 10,000 sq ft",
    "10,000 - 25,000 sq ft",
    "25,000 - 50,000 sq ft",
    "Full Site / Anchor Requirement",
]

LEASE_TERMS = [
    "Short-Term: Daily / Weekly",
    "Monthly Rolling",
    "Seasonal: 3-8 Months",
    "Annual Lease",
    "Multi-Year: 2-5 Years",
    "Anchor / Exclusive Site Allocation",
]

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


def safe_secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, default)
        return str(value) if value is not None else default
    except Exception:
        return default


def get_email_config() -> Tuple[str, str, str, str]:
    sender_email = safe_secret("SENDER_EMAIL", DEFAULT_SENDER_EMAIL)
    admin_email = safe_secret("ADMIN_EMAIL", DEFAULT_ADMIN_EMAIL)
    smtp_username = safe_secret("SMTP_USERNAME", sender_email)
    password = safe_secret("EMAIL_PASSWORD", "")
    return sender_email, admin_email, smtp_username, password


def get_booking_link() -> str:
    return safe_secret("BOOKING_LINK", "")


def ensure_directories() -> None:
    for directory in [DATA_DIRECTORY, LAYOUT_DIRECTORY]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.warning("Could not create directory %s: %s", directory, exc)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email.strip()))


def safe_html_text(value: object) -> str:
    return html.escape(str(value or ""))


def safe_filename(value: object) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", str(value or "file")).strip("_")
    return cleaned or "file"


def encode_file_base64(path: Path) -> Optional[str]:
    try:
        if path.exists():
            return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception as exc:
        logger.warning("Could not encode file %s: %s", path, exc)
    return None


def apply_global_styles() -> None:
    background_image = encode_file_base64(BACKGROUND_IMAGE)
    if background_image:
        background_css = f'''
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,.84), rgba(0,0,0,.84)), url("data:image/jpg;base64,{background_image}");
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
            text-align:center;
            font-family:Georgia,serif;
            font-size:clamp(2.2rem,7vw,4rem);
            font-weight:300;
            letter-spacing:.22em;
            margin:2rem 0 .25rem;
            background:linear-gradient(to right,#bf953f,#fcf6ba,#b38728,#fbf5b7,#aa771c);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            text-transform:uppercase;
        }}
        .sub-brand {{
            text-align:center;
            color:#d4af37;
            letter-spacing:.18em;
            font-size:.82rem;
            text-transform:uppercase;
            margin-bottom:2rem;
        }}
        .gold-text {{ color:#d4af37; font-weight:700; }}
        [data-testid="stForm"] {{
            background-color:rgba(0,0,0,.80)!important;
            border:1px solid #d4af37!important;
            padding:2rem!important;
            border-radius:.75rem;
            box-shadow:0 0 40px rgba(212,175,55,.12);
        }}
        .eoi-document {{
            background-color:rgba(0,0,0,.92);
            color:#fff;
            padding:clamp(1.5rem,4vw,3rem);
            border:1px solid #d4af37;
            border-radius:.75rem;
            font-family:Georgia,serif;
            line-height:1.55;
            margin-bottom:1.8rem;
            box-shadow:0 0 40px rgba(212,175,55,.2);
        }}
        .notice-card {{
            background:linear-gradient(145deg,rgba(26,26,26,.95),rgba(0,0,0,.95));
            border:2px solid #d4af37;
            padding:1.8rem;
            border-radius:1rem;
            text-align:center;
            max-width:760px;
            margin:1.5rem auto;
            color:#fff;
        }}
        .diagnostic-card {{
            background:rgba(0,0,0,.76);
            border:1px solid rgba(212,175,55,.65);
            padding:1rem;
            border-radius:.75rem;
            margin-top:1rem;
            color:#fff;
            font-size:.9rem;
        }}
        .privacy-note {{
            font-size:.85rem;
            color:#ccc;
            border-left:3px solid #d4af37;
            padding-left:.9rem;
            margin-top:.75rem;
        }}
        .stButton>button, .stFormSubmitButton>button {{
            background-color:#d4af37!important;
            color:#000!important;
            font-weight:800;
            border-radius:.35rem;
            min-height:3.4rem;
            width:100%;
            border:none;
            letter-spacing:.12em;
            text-transform:uppercase;
        }}
        .stButton>button:hover, .stFormSubmitButton>button:hover {{
            background-color:#fff!important;
            box-shadow:0 0 20px rgba(212,175,55,.8);
        }}
        label, .stMarkdown, .stRadio, .stSelectbox, .stMultiSelect, .stTextInput, .stCheckbox, .stTextArea {{
            color:#fff!important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    scope = data.get("scope", "")
    if data.get("send_full_pricing", False) or scope not in PRICING_DEALS:
        return format_full_pricing_schedule()
    return format_single_pricing_block(scope, PRICING_DEALS[scope])


def calculate_lead_score(data: dict) -> Tuple[str, int, str, str]:
    score = 0
    scope = data.get("scope", "")
    space = data.get("space_requirement", "")
    term = data.get("lease_term", "")
    value = data.get("strategic_value", "")
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

    if "Anchor" in term or "Multi-Year" in term:
        score += 24
    elif "Annual" in term:
        score += 16
    elif "Seasonal" in term:
        score += 10
    elif "Monthly" in term:
        score += 6

    if value == "Critical":
        score += 16
    elif value == "Strategic":
        score += 12
    elif value == "Important":
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
        return "Tier A+ / Anchor Prospect", score, "Same-day executive follow-up recommended", "DO NOT SEND STANDARD QUOTE ONLY. Complete custom allocation review and term pricing."
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


def is_high_value_lead(data: dict) -> bool:
    _, score, _, _ = calculate_lead_score(data)
    return score >= 75 or "Full Site" in data.get("space_requirement", "")


def get_layout_file(data: dict) -> Optional[Path]:
    return LAYOUT_FILES.get(data.get("space_requirement", ""))


def attach_file(message: MIMEMultipart, file_path: Optional[Path], display_name: str, subtype: str = "octet-stream") -> Tuple[bool, str]:
    if file_path is None:
        return False, "No file mapped."
    if not file_path.exists():
        return False, f"File missing: {file_path}"

    try:
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_ATTACHMENT_MB:
            return False, f"File too large: {file_path} is {file_size_mb:.1f} MB. Limit is {MAX_ATTACHMENT_MB} MB."
    except Exception as exc:
        return False, f"Could not inspect file size for {file_path}: {type(exc).__name__}: {exc}"

    try:
        with file_path.open("rb") as file:
            part = MIMEApplication(file.read(), _subtype=subtype, Name=display_name)
        part["Content-Disposition"] = f'attachment; filename="{display_name}"'
        message.attach(part)
        return True, f"Attached: {file_path}"
    except Exception as exc:
        logger.exception("Attachment failed")
        return False, f"Attachment error for {file_path}: {type(exc).__name__}: {exc}"


def attach_all_client_files(message: MIMEMultipart, data: dict) -> AttachmentStatus:
    overview_ok, overview_status = attach_file(message, SITE_LAYOUT_OVERVIEW, "EagleView_Site_Layout_Overview.pdf", "pdf")
    leasing_ok, leasing_status = attach_file(message, LEASING_AGREEMENT_PDF, "EagleView_Preliminary_Leasing_Agreement.pdf", "pdf")
    size_ok, size_status = attach_file(
        message,
        get_layout_file(data),
        f"EagleView_Yard_Allocation_{safe_filename(data.get('space_requirement'))}.pdf",
        "pdf",
    )
    return AttachmentStatus(
        overview_attached=overview_ok,
        overview_status=overview_status,
        leasing_agreement_attached=leasing_ok,
        leasing_agreement_status=leasing_status,
        size_layout_attached=size_ok,
        size_layout_status=size_status,
    )


def format_attachment_report(status: Optional[AttachmentStatus]) -> str:
    if status is None:
        return "Attachment status unavailable."
    return f"""Universal Site Layout Overview PDF: {'Attached' if status.overview_attached else 'NOT ATTACHED'}
Overview Status: {status.overview_status}
Preliminary Leasing Agreement PDF: {'Attached' if status.leasing_agreement_attached else 'NOT ATTACHED'}
Leasing Agreement Status: {status.leasing_agreement_status}
Size-Specific Layout: {'Attached' if status.size_layout_attached else 'NOT ATTACHED'}
Size-Specific Status: {status.size_layout_status}"""


def save_lead(data: dict, result: EmailSendResult, status: AttachmentStatus) -> str:
    try:
        ensure_directories()
        tier, score, follow_up, strategy = calculate_lead_score(data)
        submission_status = "email_sent" if result.client_sent and result.admin_sent else "email_failed_or_partial"
        row = {
            "submitted_at_utc": datetime.now(timezone.utc).isoformat(),
            "submission_status": submission_status,
            "company_or_rep": data.get("name", ""),
            "email": data.get("email", ""),
            "client_type": data.get("client_type", ""),
            "scope": data.get("scope", ""),
            "space_requirement": data.get("space_requirement", ""),
            "lease_term": data.get("lease_term", ""),
            "send_full_pricing": data.get("send_full_pricing", False),
            "strategic_value": data.get("strategic_value", ""),
            "deployment_window": data.get("deployment_window", ""),
            "amenities": json.dumps(data.get("amenities", [])),
            "project_notes": data.get("project_notes", ""),
            "signature": data.get("signature", ""),
            "terms_acknowledged": data.get("terms_acknowledged", False),
            "privacy_acknowledged": data.get("privacy_acknowledged", False),
            "lead_tier": tier,
            "lead_score": score,
            "follow_up": follow_up,
            "pricing_strategy": strategy,
            "estimated_monthly_value": estimate_monthly_value(data),
            "client_email_sent": result.client_sent,
            "admin_email_sent": result.admin_sent,
            "client_error": result.client_error,
            "admin_error": result.admin_error,
            "overview_attached": status.overview_attached,
            "overview_status": status.overview_status,
            "leasing_agreement_attached": status.leasing_agreement_attached,
            "leasing_agreement_status": status.leasing_agreement_status,
            "size_layout_attached": status.size_layout_attached,
            "size_layout_status": status.size_layout_status,
        }
        file_exists = LEAD_CSV_FILE.exists()
        with LEAD_CSV_FILE.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(row.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
        return f"Lead saved to {LEAD_CSV_FILE}"
    except Exception as exc:
        logger.exception("Lead backup failed")
        return f"Lead backup failed: {type(exc).__name__}: {exc}"


def build_client_email(data: dict, sender_email: str) -> Tuple[MIMEMultipart, AttachmentStatus]:
    message = MIMEMultipart()
    message["From"] = f"EagleView Estates <{sender_email}>"
    message["To"] = data["email"]
    message["Subject"] = "EagleView Estates: Expression of Interest Confirmation"

    pricing_intro = "Complete preliminary pricing schedule:" if data.get("send_full_pricing", False) else f"Preliminary pricing indication for {data.get('scope')}:"
    booking_link = get_booking_link()
    booking_text = f"\nSchedule Private Site Allocation Review:\n{booking_link}\n" if booking_link else "\nNext Step:\nEagleView may complete a private site allocation review before confirming availability.\n"

    body = f"""Hello {data.get('name')},

Thank you for submitting your Expression of Interest Request for EagleView Estates.

Preliminary requirement received:
- Client Type: {data.get('client_type')}
- Operational Scope: {data.get('scope')}
- Approximate Space Requirement: {data.get('space_requirement')}
- Preferred Lease Term: {data.get('lease_term')}
- Target Deployment Window: {data.get('deployment_window')}

{pricing_intro}
{requested_pricing_block(data)}

Attached Package:
- EagleView Site Layout Overview PDF
- Preliminary Leasing Agreement PDF for review and acceptance
- Size-specific yard allocation exhibit, when available

Important Disclaimer:
This submission confirms interest only. Pricing is indicative and subject to availability, final yard configuration, access requirements, operating intensity, lease term, insurance requirements, security requirements, municipal approvals where applicable, and final lease documentation. No lease, reservation, exclusivity, or binding commitment is created until a formal agreement is executed by both parties.

Privacy / Commercial Confidentiality:
Information submitted through the EagleView portal will be used to evaluate preliminary yard leasing requirements, site allocation suitability, pricing structure, and follow-up priority.
{booking_text}
Best regards,
The EagleView Estates Team"""
    message.attach(MIMEText(body, "plain"))
    attachment_status = attach_all_client_files(message, data)
    message["X-EagleView-Attachments"] = (
        f"overview={attachment_status.overview_attached}; "
        f"leasing_agreement={attachment_status.leasing_agreement_attached}; "
        f"size={attachment_status.size_layout_attached}"
    )
    return message, attachment_status


def build_admin_email(data: dict, sender_email: str, admin_email: str, attachment_status: AttachmentStatus, result: EmailSendResult, lead_status: str) -> MIMEMultipart:
    tier, score, follow_up, strategy = calculate_lead_score(data)
    high_value_warning = "\n*** HIGH-VALUE LEAD: DO NOT SEND STANDARD QUOTE ONLY — CUSTOM ALLOCATION REVIEW REQUIRED ***\n" if is_high_value_lead(data) else ""
    subject_prefix = "HIGH-VALUE LEAD - " if is_high_value_lead(data) else ""

    message = MIMEMultipart()
    message["From"] = f"EagleView Portal <{sender_email}>"
    message["To"] = admin_email
    message["Subject"] = f"{subject_prefix}New EOI Request: {data.get('name')}"

    body = f"""New Expression of Interest Request received.
{high_value_warning}
Company / Representative: {data.get('name')}
Email: {data.get('email')}
Client Type: {data.get('client_type')}
Operational Scope: {data.get('scope')}
Space Requirement: {data.get('space_requirement')}
Preferred Lease Term: {data.get('lease_term')}
Strategic Value: {data.get('strategic_value')}
Target Deployment: {data.get('deployment_window')}
Amenities: {', '.join(data.get('amenities', [])) or 'None selected'}
Project / Use Notes: {data.get('project_notes') or 'N/A'}
Digital Signature: {data.get('signature')}
Terms Acknowledged: {'Yes' if data.get('terms_acknowledged') else 'No'}
Privacy Acknowledged: {'Yes' if data.get('privacy_acknowledged') else 'No'}

Internal Lead Review:
Lead Tier: {tier}
Lead Score: {score}/125
Follow-Up Urgency: {follow_up}
Recommended Pricing Strategy: {strategy}
Estimated Monthly Value: {estimate_monthly_value(data)}

Client Email Delivery:
Client Confirmation Accepted by SMTP: {'YES' if result.client_sent else 'NO'}
Client Error: {result.client_error or 'None'}

Attachment Report:
{format_attachment_report(attachment_status)}

Lead Backup:
{lead_status}

Pricing Sent To Prospect:
{requested_pricing_block(data)}

Notes:
This is a non-binding Expression of Interest Request only. No lease has been executed through the portal."""
    message.attach(MIMEText(body, "plain"))
    return message


def send_one_email(server: smtplib.SMTP, message: MIMEMultipart, from_addr: str, recipients: List[str]) -> Tuple[bool, str]:
    try:
        refused = server.sendmail(from_addr, recipients, message.as_string())
        if refused:
            return False, f"Recipient refused: {refused}"
        return True, ""
    except Exception as exc:
        logger.exception("Email send failed")
        return False, f"{type(exc).__name__}: {exc}"


def send_emails(data: dict) -> Tuple[EmailSendResult, AttachmentStatus, str]:
    sender_email, admin_email, smtp_username, password = get_email_config()
    result = EmailSendResult(
        smtp_username=smtp_username,
        sender_email=sender_email,
        admin_email=admin_email,
        client_email=data.get("email", ""),
    )

    client_message, attachment_status = build_client_email(data, sender_email)

    if not password:
        result.client_error = "Missing EMAIL_PASSWORD in Streamlit secrets."
        result.admin_error = "Missing EMAIL_PASSWORD in Streamlit secrets."
        lead_status = save_lead(data, result, attachment_status)
        return result, attachment_status, lead_status

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(smtp_username, password)

            result.client_sent, result.client_error = send_one_email(
                server,
                client_message,
                sender_email,
                [data["email"], admin_email],
            )

            provisional_lead_status = save_lead(data, result, attachment_status)
            admin_message = build_admin_email(
                data=data,
                sender_email=sender_email,
                admin_email=admin_email,
                attachment_status=attachment_status,
                result=result,
                lead_status=provisional_lead_status,
            )
            result.admin_sent, result.admin_error = send_one_email(
                server,
                admin_message,
                sender_email,
                [admin_email],
            )
    except smtplib.SMTPAuthenticationError as exc:
        error = f"SMTPAuthenticationError: {exc}. Check Gmail app password / SMTP_USERNAME."
        result.client_error = error
        result.admin_error = error
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        result.client_error = error
        result.admin_error = error

    final_lead_status = save_lead(data, result, attachment_status)
    return result, attachment_status, final_lead_status


def render_email_diagnostics(result: EmailSendResult) -> None:
    st.markdown(
        f"""
        <div class='diagnostic-card'>
        <b>Email Diagnostic</b><br>
        SMTP Username: {safe_html_text(result.smtp_username)}<br>
        Sender Email: {safe_html_text(result.sender_email)}<br>
        Client Email: {safe_html_text(result.client_email)}<br>
        Admin / Verification Copy: {safe_html_text(result.admin_email)}<br>
        Client Confirmation Accepted by SMTP: {'YES' if result.client_sent else 'NO'}<br>
        Admin Allocation Notice Accepted by SMTP: {'YES' if result.admin_sent else 'NO'}<br>
        Client Error: {safe_html_text(result.client_error or 'None')}<br>
        Admin Error: {safe_html_text(result.admin_error or 'None')}
        </div>
        """,
        unsafe_allow_html=True,
    )


def assessment_page() -> None:
    render_header()
    with st.form("assessment_form", clear_on_submit=False):
        st.markdown("### <span class='gold-text'>Expression of Interest Request</span>", unsafe_allow_html=True)
        st.caption("For contractors, infrastructure operators, fleet users, and commercial tenants seeking secured yard space.")

        client_type = st.selectbox("1. Client / Organization Type", CLIENT_TYPES)
        scope = st.selectbox("2. Operational Scope", list(PRICING_DEALS.keys()))
        space_requirement = st.selectbox("3. Approximate Space Requirement", SPACE_REQUIREMENTS)
        lease_term = st.selectbox("4. Preferred Lease Structure", LEASE_TERMS)
        send_full_pricing = st.checkbox(
            "Send me the complete preliminary pricing schedule for all storage options",
            value=False,
            help="For major or custom requirements, EagleView may provide a tailored pricing review instead of relying only on standard schedule pricing.",
        )
        strategic_value = st.select_slider("5. Strategic Value of Location", options=VALUE_OPTIONS)
        deployment_window = st.radio("6. Target Deployment Date", DEPLOYMENT_WINDOWS)
        amenities = st.multiselect("7. Critical Site Requirements", AMENITIES)
        project_notes = st.text_area(
            "8. Project / Fleet Requirement Notes",
            placeholder="Equipment type, number of units, access frequency, security requirements, or timeline.",
            height=120,
        )

        st.markdown(
            "<div class='privacy-note'>Information submitted through this portal will be used to evaluate preliminary yard leasing requirements, site allocation suitability, pricing structure, and follow-up priority.</div>",
            unsafe_allow_html=True,
        )
        terms_acknowledged = st.checkbox("I understand this is a non-binding preliminary leasing request and does not create a reservation, lease, exclusivity, or guarantee of availability.")
        privacy_acknowledged = st.checkbox("I understand the submitted information may be used by EagleView Estates to evaluate site allocation suitability and follow-up priority.")

        name = st.text_input("Company / Representative Name", placeholder="Example: ABC Contracting Ltd.")
        email = st.text_input("Direct Email", placeholder="name@company.com")
        submitted = st.form_submit_button("Validate & Continue")

    if submitted:
        if not name.strip():
            st.warning("Please enter a company or representative name.")
            return
        if not is_valid_email(email.strip().lower()):
            st.warning("Please enter a valid email address.")
            return
        if not terms_acknowledged:
            st.warning("Please acknowledge that this is a non-binding preliminary leasing request.")
            return
        if not privacy_acknowledged:
            st.warning("Please acknowledge the privacy / commercial review notice.")
            return

        st.session_state.user_data = {
            "name": name.strip(),
            "email": email.strip().lower(),
            "client_type": client_type,
            "scope": scope,
            "space_requirement": space_requirement,
            "lease_term": lease_term,
            "send_full_pricing": send_full_pricing,
            "strategic_value": strategic_value,
            "deployment_window": deployment_window,
            "amenities": amenities,
            "project_notes": project_notes.strip(),
            "terms_acknowledged": terms_acknowledged,
            "privacy_acknowledged": privacy_acknowledged,
        }
        st.session_state.page = "eoi"
        st.rerun()


def eoi_page() -> None:
    data = st.session_state.get("user_data", {})
    if not data:
        reset_portal()
        return

    render_header()
    st.markdown(
        f"""
        <div class='eoi-document'>
        <h2 style='text-align:center; color:#d4af37; text-transform:uppercase;'>Expression of Interest Request</h2>
        <p><span class='gold-text'>Prospective Tenant:</span> {safe_html_text(data.get('name'))}</p>
        <hr style='border: 0.5px solid #d4af37;'>
        <p><b>1. Client Type:</b> {safe_html_text(data.get('client_type'))}</p>
        <p><b>2. Scope:</b> <span class='gold-text'>{safe_html_text(data.get('scope'))}</span></p>
        <p><b>3. Space Requirement:</b> {safe_html_text(data.get('space_requirement'))}</p>
        <p><b>4. Lease Structure:</b> {safe_html_text(data.get('lease_term'))}</p>
        <p><b>5. Target Window:</b> {safe_html_text(data.get('deployment_window'))}</p>
        <p><b>6. Preliminary Review:</b> Your request will be reviewed for availability, access requirements, insurance requirements, and site allocation suitability.</p>
        <p><b>7. Non-Binding Acknowledgement:</b> This request is not a lease, reservation, exclusivity, or binding commitment.</p>
        <p style='font-size:.9rem; color:#bbb; margin-top:1.5rem;'><i>By signing below, you confirm interest in receiving preliminary leasing information and, where applicable, a private site allocation review.</i></p>
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
        if st.button("Submit EOI Request"):
            if not signature.strip():
                st.warning("Please enter your full name and title as a digital signature.")
                return
            st.session_state.user_data["signature"] = signature.strip()
            result, attachment_status, lead_status = send_emails(st.session_state.user_data)
            st.session_state.email_result = result
            if result.client_sent and result.admin_sent:
                st.session_state.page = "thankyou"
                st.rerun()
            st.error("Email delivery failed or partially failed. Diagnostic details are below.")
            st.info(lead_status)
            st.text(format_attachment_report(attachment_status))
            render_email_diagnostics(result)


def thankyou_page() -> None:
    render_header()
    booking_link = get_booking_link()
    if booking_link:
        booking_html = f"<p><b>Next Step:</b> <a href='{safe_html_text(booking_link)}' target='_blank' style='color:#d4af37;'>Schedule a Private Site Allocation Review</a>.</p>"
    else:
        booking_html = "<p><b>Next Step:</b> Watch for your preliminary leasing framework by email. For larger requirements, EagleView may conduct an internal site allocation review before confirming availability.</p>"

    st.markdown("<div style='text-align:center; margin-top:2rem; font-size:4rem;'>✔️</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='color:#d4af37; font-size:1.8rem; text-align:center; letter-spacing:.22em; margin-bottom:1rem; text-transform:uppercase;'>Request Received</div>
        <div class='notice-card'>
        <h4 style='color:#d4af37; margin-top:0; text-transform:uppercase; letter-spacing:.12em;'>Expression of Interest Request Received</h4>
        <p>Your Expression of Interest Request has been received. A preliminary leasing package has been sent to the email provided.</p>
        <p>A verification copy was also sent to EagleView for internal review and follow-up.</p>
        {booking_html}
        <p>If the confirmation package does not arrive shortly, check your <b style='color:#d4af37;'>Junk/Spam folder</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Submit Another EOI Request"):
        reset_portal()


def main() -> None:
    ensure_directories()
    init_state()
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
