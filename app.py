import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | EOI Portal", layout="centered", page_icon="🦅")

# --- COMPREHENSIVE PRICING ENGINE ---
PRICING_DEALS = {
    "💎 ANCHOR TENANT: 5-Acre Parcel": {
        "Daily": "$1,200/day",
        "Weekly": "$5,500/week",
        "Monthly": "$12,500/month",
        "Yearly": "$140,000/annum",
        "Multi-Year": "Contact for Institutional Rates",
        "details": "Full 5-acre integrated site. Pricing includes exclusive biometric gate access."
    },
    "Dedicated Pad (1-5k sqft)": {
        "Daily": "$250/day",
        "Weekly": "$1,200/week",
        "Monthly": "$3,500/month",
        "Yearly": "$38,000/annum",
        "Multi-Year": "$32,000/annum (3+ Year Commitment)",
        "details": "Engineered gravel pad with dedicated LED lighting and CCTV coverage."
    },
    "Hourly Flex Staging": {
        "Daily": "$450/day (Flat Rate)",
        "Weekly": "$2,200/week",
        "Monthly": "$6,500/month",
        "Yearly": "N/A",
        "Multi-Year": "N/A",
        "details": "Rapid-access staging for cross-docking and immediate fleet positioning."
    },
    "Winter Storage": {
        "Daily": "N/A",
        "Weekly": "N/A",
        "Monthly": "$1,800/month",
        "Yearly": "$15,000 (Seasonal Oct-May)",
        "Multi-Year": "Contact for Fleet Discounts",
        "details": "Secure winterization storage for heavy fleet equipment."
    }
}

# --- DUAL-EMAIL FUNCTION ---
def send_emails(data, is_eoi=False):
    try:
        sender_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]
        
        selected_scope = data.get('q1')
        p = PRICING_DEALS.get(selected_scope)
        
        # 1. ADMIN NOTIFICATION
        msg_to_admin = MIMEMultipart()
        msg_to_admin["From"] = f"EagleView Estates Portal <{sender_email}>"
        msg_to_admin["To"] = sender_email
        msg_to_admin["Subject"] = f"🚨 FULL SPECTRUM EOI: {data['name']}"
        
        admin_body = f"EOI Received:\n\nCompany: {data['name']}\nContact: {data['contact']}\nSelection: {selected_scope}\n\nUser Signed: {data.get('signature', 'Inquiry Only')}"
        msg_to_admin.attach(MIMEText(admin_body, "plain"))

        # 2. CLIENT THANK YOU WITH ALL OPTIONS
        msg_to_client = MIMEMultipart()
        msg_to_client["From"] = f"EagleView Estates <{sender_email}>"
        msg_to_client["To"] = data['contact']
        msg_to_client["Subject"] = f"Lease Options & Multi-Term Pricing: {data['name']}"
        
        client_body = f"""
Dear {data['name']},

Thank you for submitting your Expression of Interest for EagleView Estates at CentrePort Canada.

As requested, here is the full-spectrum pricing breakdown for the {selected_scope} configuration:

--- LEASE OPTIONS & RATE STRUCTURE ---
> Daily Rate: {p['Daily']}
> Weekly Rate: {p['Weekly']}
> Monthly Rate: {p['Monthly']}
> Yearly Rate: {p['Yearly']}
> Multi-Year: {p['Multi-Year']}

SITE DETAILS: {p['details']}
TARGET DEPLOYMENT: {data['q3']}
--------------------------------------

*DISCLAIMER: All rates are subject to change based on site availability, market conditions, and final engineering requirements. This quote is preliminary and non-binding.*

NEXT STEPS:
Our team will reach out to finalize your specific deployment window and site layout requirements.

Best regards,

The Development Team
EagleView Estates | Winnipeg, MB
        """
        msg_to_client.attach(MIMEText(client_body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, msg_to_admin.as_string())
        if "@" in data['contact']:
            server.sendmail(sender_email, data['contact'], msg_to_client.as_string())
        server.quit()
        return True
    except:
        return False

# --- CSS: DARK MODE INSTITUTIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .brand-gold {
        text-align: center; font-family: 'serif'; font-size: 3.5em; font-weight: 200; letter-spacing: 10px;
        margin: 40px 0 10px 0; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase;
    }
    .sub-brand { text-align: center; color: #d4af37; letter-spacing: 4px; font-size: 0.9em; text-transform: uppercase; margin-bottom: 40px; }
    
    .eoi-document {
        background-color: #000000; color: #ffffff; padding: 45px; border: 1px solid #333;
        border-radius: 2px; font-family: 'serif'; line-height: 1.4; margin-bottom: 30px;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.1); font-size: 0.95em;
    }
    .eoi-title { 
        text-align: center; font-weight: bold; font-size: 1.2em; border-bottom: 1px solid #d4af37; 
        margin-bottom: 20px; padding-bottom: 10px; text-transform: uppercase; color: #d4af37;
    }
    .stButton>button { 
        background-color: #d4af37 !important; color: #000 !important; font-weight: bold; border-radius: 0; 
        height: 4em; border: none; letter-spacing: 2px; text-transform: uppercase; width: 100%;
    }
    .stButton>button:hover { background-color: #ffffff !important; box-shadow: 0 0 20px #d4af37; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'assessment'
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- PAGE 1: ASSESSMENT ---
if st.session_state.page == 'assessment':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-brand'>CentrePort Canada • Winnipeg</div>", unsafe_allow_html=True)
    
    if os.path.exists("site_photo.jpg"):
        st.image("site_photo.jpg", use_column_width=True)

    with st.form("assessment_form"):
        st.write("### Strategic Site Assessment")
        q1 = st.selectbox("1. Operational Scope", list(PRICING_DEALS.keys()))
        q2 = st.select_slider("2. Strategic Value of Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
        q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Summer 2026", "Fall/Winter 2026"])
        q4 = st.multiselect("4. Critical Site Amenities", ["Biometric Access", "LED Lighting", "CCTV Surveillance", "Engineered Gravel", "Maintenance Support"])
        q5 = st.radio("5. Submit a formal Expression of Interest for multi-term pricing?", ["YES - Submit EOI", "NO - Send general info"])
        
        name = st.text_input("Company / Representative Name")
        contact = st.text_input("Direct Email (for full pricing breakdown)")
        
        if st.form_submit_button("VALIDATE & CONTINUE"):
            if name and contact:
                st.session_state.user_data = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
                if "YES" in q5: st.session_state.page = 'eoi'
                else:
                    send_emails(st.session_state.user_data)
                    st.session_state.page = 'thankyou'
                st.rerun()
            else:
                st.warning("Identification and contact details required.")

# --- PAGE 2: FORMAL STATEMENT OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <div class='eoi-title'>Expression of Interest: Multi-Term Site Selection</div>
        <p><b>PROJECT:</b> CentrePort Canada Industrial Hub</p>
        <p><b>PROSPECTIVE TENANT:</b> {st.session_state.user_data['name']}</p>
        <hr style='border: 0.5px solid #333;'>
        <p><b>1. SCOPE:</b> Prospective Tenant has identified a requirement for <b>{st.session_state.user_data['q1']}</b>.</p>
        <p><b>2. TERMS:</b> Execution of this EOI requests a comprehensive pricing breakdown across <b>Daily, Weekly, Monthly, Yearly, and Multi-Year</b> schedules.</p>
        <p><b>3. PRIORITY:</b> This submission establishes priority status for the <b>{st.session_state.user_data['q3']}</b> window.</p>
        <p><b>4. DISCLAIMER:</b> All rates are subject to market conditions and engineering benchmarks. This document is a non-binding statement of intent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Digital Signature (Full Name & Title)")
    if st.button("EXECUTE EOI & UNLOCK ALL PRICING"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_emails(st.session_state.user_data, is_eoi=True)
            st.session_state.page = 'thankyou'
            st.rerun()
        else: st.error("Signature required.")

# --- PAGE 3: THANK YOU ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.5em; text-align:center; letter-spacing: 5px; margin-top:50px;'>EOI VERIFIED</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='color:#888; text-align:center; max-width:600px; margin: 40px auto; line-height:1.6;'>
            Thank you, <b>{st.session_state.user_data['name']}</b>. Your requirements have been integrated. <br><br>
            A confirmation including your <b>Full Multi-Term Pricing Package</b> has been sent to <b>{st.session_state.user_data['contact']}</b>.
        </div>
    """, unsafe_allow_html=True)
