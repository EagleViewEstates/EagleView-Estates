import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | EOI Portal", layout="centered", page_icon="🦅")

# --- DYNAMIC PRICING RANGES ---
PRICING_DEALS = {
    "💎 ANCHOR TENANT: 5-Acre Parcel": {
        "Daily": "$1,000 - $1,500/day",
        "Weekly": "$4,500 - $6,500/week",
        "Monthly": "$9,500 - $14,500/month",
        "Yearly": "$110k - $155k/annum",
        "Multi-Year": "Custom Institutional Quote",
        "details": "Full 5-acre integrated site with exclusive biometric gate access."
    },
    "Dedicated Pad (1-5k sqft)": {
        "Daily": "$150 - $350/day",
        "Weekly": "$900 - $1,500/week",
        "Monthly": "$2,250 - $4,500/month",
        "Yearly": "$28k - $45k/annum",
        "Multi-Year": "$25k - $38k/annum (3+ Year Term)",
        "details": "Engineered gravel pad with dedicated LED lighting and CCTV."
    },
    "Hourly Flex Staging": {
        "Daily": "$350 - $550/day",
        "Weekly": "$1,800 - $2,800/week",
        "Monthly": "$5,000 - $7,500/month",
        "Yearly": "N/A",
        "Multi-Year": "N/A",
        "details": "Rapid-access staging for cross-docking and fleet positioning."
    },
    "Winter Storage": {
        "Daily": "N/A",
        "Weekly": "N/A",
        "Monthly": "$1,200 - $2,100/month",
        "Yearly": "$12,500 - $18,000 (Seasonal Oct-May)",
        "Multi-Year": "Fleet Volume Discounts Available",
        "details": "Secure winterization storage for heavy equipment."
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
        
        admin_body = f"EOI Received:\n\nCompany: {data['name']}\nSelection: {selected_scope}\n\nUser Signed: {data.get('signature', 'Inquiry Only')}"
        msg_to_admin.attach(MIMEText(admin_body, "plain"))

        # 2. CLIENT THANK YOU
        msg_to_client = MIMEMultipart()
        msg_to_client["From"] = f"EagleView Estates <{sender_email}>"
        msg_to_client["To"] = data['contact']
        msg_to_client["Subject"] = f"Lease Options & Multi-Term Pricing: {data['name']}"
        
        client_body = f"""
Dear {data['name']},

Thank you for submitting your Expression of Interest for EagleView Estates at CentrePort Canada.

Based on your selection for {selected_scope}, here is the dynamic pricing range for our upcoming June 1st deployment:

--- LEASE OPTIONS & RATE RANGES ---
> Daily Rate: {p['Daily']}
> Weekly Rate: {p['Weekly']}
> Monthly Rate: {p['Monthly']}
> Yearly Rate: {p['Yearly']}
> Multi-Year: {p['Multi-Year']}

SITE DETAILS: {p['details']}
TARGET DEPLOYMENT: {data['q3']}
--------------------------------------

*PRICING NOTE: These ranges represent current market conditions and site engineering costs. Finalized rates within these ranges are determined by fleet volume, specific utility requirements, and term length.*

NEXT STEPS:
Our team will contact you to finalize your specific rate and secure your site position.

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

# --- CSS: GOLD & BLACK HIGHLIGHTS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .brand-gold {
        text-align: center; font-family: 'serif'; font-size: 3.5em; font-weight: 200; letter-spacing: 10px;
        margin: 40px 0 10px 0; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase;
    }
    .sub-brand { text-align: center; color: #d4af37; letter-spacing: 4px; font-size: 0.9em; text-transform: uppercase; margin-bottom: 40px; }
    
    .gold-text { color: #d4af37; font-weight: bold; }
    
    .eoi-document {
        background-color: #000000; color: #ffffff; padding: 45px; border: 1px solid #d4af37;
        border-radius: 2px; font-family: 'serif'; line-height: 1.4; margin-bottom: 30px;
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.2); font-size: 0.95em;
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
    
    .junk-warning {
        background-color: #111; padding: 20px; border: 1px solid #d4af37; color: #d4af37; 
        font-size: 0.9em; text-align: center; border-radius: 4px; margin-top: 30px;
    }
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
        st.markdown("### <span class='gold-text'>Strategic Site Assessment</span>", unsafe_allow_html=True)
        q1 = st.selectbox("1. Operational Scope", list(PRICING_DEALS.keys()))
        q2 = st.select_slider("2. Strategic Value of Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
        q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Summer 2026", "Fall/Winter 2026"])
        q4 = st.multiselect("4. Critical Site Amenities", ["Biometric Access", "LED Lighting", "CCTV Surveillance", "Engineered Gravel", "Maintenance Support"])
        q5 = st.radio("5. Execute an Expression of Interest to unlock full-term pricing ranges?", ["YES - Submit EOI", "NO - Just send general info"])
        
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
                st.warning("Identification required for site planning.")

# --- PAGE 2: FORMAL STATEMENT OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <div class='eoi-title'>Expression of Interest: Multi-Term Site Selection</div>
        <p><span class='gold-text'>PROJECT:</span> CentrePort Canada Industrial Hub</p>
        <p><span class='gold-text'>PROSPECTIVE TENANT:</span> {st.session_state.user_data['name']}</p>
        <hr style='border: 0.5px solid #d4af37;'>
        <p><b>1. SCOPE:</b> Interested Party has identified a requirement for <span class='gold-text'>{st.session_state.user_data['q1']}</span>.</p>
        <p><b>2. TERMS:</b> Execution of this EOI triggers a comprehensive pricing breakdown across <b>Daily, Weekly, Monthly, Yearly, and Multi-Year</b> schedules.</p>
        <p><b>3. PRIORITY:</b> This submission establishes priority status for the <b>{st.session_state.user_data['q3']}</b> window.</p>
        <p><b>4. DISCLAIMER:</b> All rate ranges are subject to market conditions and engineering benchmarks. This document is a non-binding statement of intent.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Digital Signature (Full Name & Title)")
    if st.button("EXECUTE EOI & UNLOCK ALL PRICING"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_emails(st.session_state.user_data, is_eoi=True)
            st.session_state.page = 'thankyou'
            st.rerun()
        else: st.error("Signature required to verify intent.")

# --- PAGE 3: THANK YOU ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.5em; text-align:center; letter-spacing: 5px; margin-top:50px;'>EOI VERIFIED</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='color:#888; text-align:center; max-width:600px; margin: 40px auto; line-height:1.6;'>
            Thank you, <span class='gold-text'>{st.session_state.user_data['name']}</span>. Your requirements have been integrated into our site plan. <br><br>
            Your <b>Multi-Term Pricing Range Package</b> has been sent to <span class='gold-text'>{st.session_state.user_data['contact']}</span>.
            
            <div class='junk-warning'>
                <b>CRITICAL:</b> If the pricing package does not arrive in your inbox within 60 seconds, check your <b>Junk/Spam folder</b>. 
                Mark the message as 'Not Junk' to ensure you receive future engineering updates and lease documents.
            </div>
        </div>
    """, unsafe_allow_html=True)
