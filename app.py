import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | EOI Portal", layout="centered", page_icon="🦅")

# --- PRICING ENGINE ---
# Update these values to your actual rates
PRICING_DEALS = {
    "💎 ANCHOR TENANT: 5-Acre Parcel": {
        "rate": "$12,500/month (Triple Net)",
        "details": "Full 5-acre integrated site, exclusive biometric gate access, and 24/7 priority maintenance."
    },
    "Dedicated Pad (1-5k sqft)": {
        "rate": "$2,500/month",
        "details": "Engineered compacted gravel pad with dedicated LED lighting and CCTV coverage."
    },
    "Hourly Flex Staging": {
        "rate": "$75/hour (4-hour minimum)",
        "details": "Rapid-access staging area for cross-docking and short-term equipment positioning."
    },
    "Winter Storage": {
        "rate": "$1,200/unit (Seasonal)",
        "details": "Secure winterization storage for heavy fleet equipment from Nov 1 to April 1."
    }
}

# --- SPAM-PROOFED DUAL-EMAIL FUNCTION ---
def send_emails(data, is_eoi=False):
    try:
        sender_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]
        
        # Get dynamic pricing based on selection
        selected_scope = data.get('q1', "Dedicated Pad (1-5k sqft)")
        price_info = PRICING_DEALS.get(selected_scope, PRICING_DEALS["Dedicated Pad (1-5k sqft)"])
        
        # 1. NOTIFICATION TO YOU (ADMIN)
        msg_to_admin = MIMEMultipart()
        msg_to_admin["From"] = f"EagleView Estates Portal <{sender_email}>"
        msg_to_admin["To"] = sender_email
        msg_to_admin["Subject"] = f"🚨 NEW EOI: {data['name']} - {selected_scope}"
        
        admin_body = f"""
Official Site Record - EOI Received:

Company: {data['name']}
Contact: {data['contact']}
Selection: {selected_scope}
Timeline: {data['q3']}
Quoted Rate: {price_info['rate']}

Signed By: {data.get('signature', 'Inquiry Only')}
Date: May 5, 2026
        """
        msg_to_admin.attach(MIMEText(admin_body, "plain"))

        # 2. THANK YOU TO CLIENT WITH PRICING
        msg_to_client = MIMEMultipart()
        msg_to_client["From"] = f"EagleView Estates <{sender_email}>"
        msg_to_client["To"] = data['contact']
        msg_to_client["Subject"] = f"Site Options & Pricing for {data['name']}"
        
        client_body = f"""
Dear {data['name']},

Thank you for submitting your Expression of Interest for EagleView Estates at CentrePort Canada.

Based on your strategic requirements for a {selected_scope}, we have generated the following preliminary pricing and site options:

---
SELECTED CONFIGURATION: {selected_scope}
PROPOSED RATE: {price_info['rate']}
SITE DETAILS: {price_info['details']}
TARGET DEPLOYMENT: {data['q3']}
---

NEXT STEPS:
Our development team is currently finalizing the engineered grading for the June 1st launch. Your EOI has secured your priority position in the queue. 

A representative will reach out shortly to discuss specific site layout adjustments and formalize the lease agreement.

Best regards,

The Development Team
EagleView Estates
Winnipeg, Manitoba, Canada
www.eagleviewearthworks.com
        """
        msg_to_client.attach(MIMEText(client_body, "plain"))

        # Execute Sending
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

# --- CSS: INSTITUTIONAL THEME ---
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
        background-color: #ffffff; color: #1a1a1a; padding: 40px; border-radius: 2px;
        font-family: 'Times New Roman', serif; line-height: 1.6; margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.1);
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
        q5 = st.radio("5. Submit a formal Expression of Interest for priority site-plan integration?", ["YES - Submit EOI", "NO - Send general info"])
        
        name = st.text_input("Company / Representative Name")
        contact = st.text_input("Direct Email (for pricing & lease options)")
        
        if st.form_submit_button("VALIDATE & CONTINUE"):
            if name and contact:
                st.session_state.user_data = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
                if "YES" in q5:
                    st.session_state.page = 'eoi'
                else:
                    send_emails(st.session_state.user_data)
                    st.session_state.page = 'thankyou'
                st.rerun()
            else:
                st.warning("Contact details required for site planning.")

# --- PAGE 2: EXPRESSION OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <h3 style='text-align:center; border-bottom: 1px solid #1a1a1a; padding-bottom:10px;'>EXPRESSION OF INTEREST</h3>
        <p><b>PROSPECTIVE TENANT:</b> {st.session_state.user_data['name']}<br>
        <b>DEVELOPMENT:</b> CentrePort Canada Hub</p>
        <p>This document confirms a strategic interest in securing space at EagleView Estates. 
        Submission establishes priority status for the <b>{st.session_state.user_data['q3']}</b> window.</p>
        <p><b>NEXT STEPS:</b> Upon execution, our system will transmit current lease options and pricing structures to the email provided.</p>
        <p style='font-size:0.8em; color:#555;'><i>This is a non-binding expression of interest for site configuration purposes.</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Type Full Name & Title to Confirm Interest")
    if st.button("CONFIRM EOI & RECEIVE PRICING"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_emails(st.session_state.user_data, is_eoi=True)
            st.session_state.page = 'thankyou'
            st.rerun()

# --- PAGE 3: THANK YOU ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.5em; text-align:center; letter-spacing: 5px; margin-top:50px;'>EOI VERIFIED</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='color:#888; text-align:center; max-width:600px; margin: 40px auto; line-height:1.6;'>
            Thank you, <b>{st.session_state.user_data['name']}</b>. Your requirements have been integrated. <br><br>
            A confirmation including your <b>custom pricing package</b> has been sent to <b>{st.session_state.user_data['contact']}</b>.<br><br>
            <div style='background-color:#111; padding:15px; border:1px solid #333; color:#d4af37; font-size:0.9em;'>
            <b>IMPORTANT:</b> If the pricing package does not arrive within 60 seconds, please check your <b>Junk/Spam folder</b>.
            </div>
            <br>
            We look forward to partnering in the future.
        </div>
    """, unsafe_allow_html=True)
