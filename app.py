import streamlit as st
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Anchor Assessment", layout="centered", page_icon="🦅")

# --- EMAIL FUNCTION ---
def send_email(data):
    try:
        sender_email = "info@eagleviewearthworks.com"
        receiver_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"🚨 CENTRE PORT INQUIRY: {data['name']}"

        body = f"""
        New Strategic Assessment Received:
        
        Company/Name: {data['name']}
        Contact: {data['contact']}
        
        1. Operational Scope: {data['q1']}
        2. Location Importance: {data['q2']}
        3. Timeframe: {data['q3']}
        4. Amenities: {data['q4']}
        5. Pre-Lease Interest: {data['q5']}
        """
        
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except:
        return False

# --- PREMIUM BLACK & GOLD THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3.5em; font-weight: 200; letter-spacing: 8px; margin-top: 20px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .subtext { color: #d4af37 !important; font-size: 1.1em; text-align: center; margin-bottom: 20px; letter-spacing: 3px; text-transform: uppercase;}
    
    .anchor-card {
        padding: 30px; 
        background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        border: 2px solid #d4af37; 
        border-radius: 8px; 
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.15);
    }
    .anchor-highlight {
        color: #d4af37; font-size: 1.5em; font-weight: bold; letter-spacing: 2px; text-transform: uppercase;
    }
    
    h3 { color: #d4af37 !important; font-weight: 300; border-bottom: 1px solid #333; padding-bottom: 10px; }
    .stButton>button { 
        width: 100%; border-radius: 0px; height: 4em; background-color: #d4af37; 
        color: #000000; font-weight: bold; border: none; letter-spacing: 2px; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #ffffff; box-shadow: 0 0 20px #d4af37; }
    
    /* Eagle Animation Container */
    .eagle-container { text-align: center; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING ---
st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>CentrePort Canada | Industrial Site Selection</p>", unsafe_allow_html=True)

# --- ANCHOR TENANT FEATURE ---
st.markdown("""
<div class='anchor-card'>
    <p style='margin:0; font-size: 0.8em; color: #888;'>CENTREPORT STRATEGIC OPPORTUNITY</p>
    <div class='anchor-highlight'>5-ACRE ANCHOR PARCEL</div>
    <p style='color: #ffffff; margin-top: 10px;'>Evaluating high-load expansion capabilities within North America's largest inland port. 
    Custom site configurations available for June 1st deployment.</p>
</div>
""", unsafe_allow_html=True)

# --- SITE PHOTO ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Strategic CentrePort Development Area", use_column_width=True)

# --- SURVEY FORM ---
with st.form("anchor_survey", clear_on_submit=True):
    st.write("### Logistics Requirements")
    
    q1 = st.selectbox("1. Operational Scope", 
                     ["💎 ANCHOR TENANT: 5-Acre Integrated Parcel", 
                      "🏗️ DEDICATED PAD: 1,000 - 5,000 sqft", 
                      "🚛 RAPID-STAGING: Daily / Hourly Flex Access", 
                      "❄️ WINTER STORAGE: Heavy Equipment Only"])

    q2 = st.select_slider("2. Strategic Value of CentrePort Winnipeg Proximity", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
    q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Q3 2026", "2027 Strategic Planning"])
    q4 = st.multiselect("4. Must-Have Amenities", ["Biometric/Coded Gate", "LED Lighting", "Live CCTV Feed", "Snow Removal", "On-Site Grading Support"])
    
    st.markdown("---")
    q5 = st.radio("5. Secure your position with a 'Pre-Lease' agreement prior to the June 1st launch?", 
                 ["YES - Send terms for the 5-Acre Parcel", 
                  "YES - Send terms for a Dedicated Pad", 
                  "MAYBE - Send pricing details", 
                  "NO - On-demand only"])

    st.divider()
    name = st.text_input("Company / Representative Name")
    contact = st.text_input("Direct Phone or Email")

    submit_button = st.form_submit_button("SUBMIT ASSESSMENT")

if submit_button:
    if name and contact:
        results = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
        
        if send_email(results):
            # EAGLE ANIMATION INSTEAD OF BALLOONS
            st.markdown("""
                <div class='eagle-container'>
