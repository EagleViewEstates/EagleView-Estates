import streamlit as st
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Assessment", layout="centered", page_icon="🦅")

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
        body = f"New Lead:\n\nName: {data['name']}\nContact: {data['contact']}\nNeed: {data['q1']}\nLocation: {data['q2']}\nTimeframe: {data['q3']}\nAmenities: {data['q4']}\nPre-Lease: {data['q5']}"
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except:
        return False

# --- CSS: THE INSTITUTIONAL LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Branding Header */
    .brand-gold {
        text-align: center; 
        font-family: 'serif';
        font-size: 3.5em; 
        font-weight: 200; 
        letter-spacing: 10px;
        margin: 40px 0 10px 0;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
    }
    
    .sub-brand {
        text-align: center;
        color: #d4af37;
        letter-spacing: 4px;
        font-size: 0.9em;
        text-transform: uppercase;
        margin-bottom: 40px;
    }

    /* Site Image Styling */
    .stImage > img {
        border: 1px solid #d4af37;
        border-radius: 4px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    /* Anchor Card */
    .anchor-card {
        padding: 40px; 
        background-color: #0a0a0a;
        border: 1px solid #d4af37;
        text-align: center;
        margin-top: 25px;
        margin-bottom: 30px;
    }

    /* Full Screen Success Overlay */
    .success-screen {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: #050505;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        z-index: 9999;
        text-align: center;
    }

    /* Premium Gold Button */
    .stButton>button { 
        background-color: #d4af37 !important; color: #000 !important;
        font-weight: bold; border-radius: 0; height: 3.5em; border: none;
        letter-spacing: 2px; text-transform: uppercase;
        width: 100%;
    }
    .stButton>button:hover { background-color: #ffffff !important; box-shadow: 0 0 15px #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- APP UI ---
st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-brand'>CentrePort Canada • Winnipeg</div>", unsafe_allow_html=True)

# --- MAIN SITE IMAGE (KEPT IN CODE) ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Strategic Industrial Development Area", use_column_width=True)

st.markdown("""
<div class='anchor-card'>
    <h2 style='color:#d4af37; font-weight:300; letter-spacing:2px; margin:0;'>STRATEGIC SITE ASSESSMENT</h2>
    <p style='color:#888; margin-top:15px;'>Evaluating a premier 1.5 - 5.0 acre industrial parcel. <br> 
    Final engineering is tailored to major fleet requirements.</p>
</div>
""", unsafe_allow_html=True)

# --- FORM ---
with st.form("main_survey", clear_on_submit=True):
    q1 = st.selectbox("1. Operational Need", ["💎 ANCHOR TENANT: 5-Acre Parcel", "Dedicated Pad (1-5k sqft)", "Hourly Flex Staging", "Seasonal Overload"])
    q2 = st.select_slider("2. Strategic Value of CentrePort Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
    q3 = st.radio("3. Target Move-in", ["June 1st", "Summer 2026", "Fall/Winter 2026"])
    q4 = st.multiselect("4. Must-Have Amenities", ["Biometric Gate", "LED Lighting", "Live CCTV Feed", "Snow Removal", "Site Maintenance"])
    q5 = st.radio("5. Secure your position with a 'Pre-Lease' agreement?", ["YES - Send terms immediately", "MAYBE - Send pricing details", "NO - On-demand only"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    name = st.text_input("Company / Representative Name")
    contact = st.text_input("Direct Phone or Email")
    
    submit = st.form_submit_button("SUBMIT PRIORITY ASSESSMENT")

# --- THANK YOU LOGIC ---
if submit:
    if name and contact:
        results = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
        send_email(results)
        
        # This replaces the page with the institutional Gold/Black thank you
        st.markdown(f"""
            <div class="success-screen">
                <div class="brand-gold">EagleView Estates</div>
                <div style="color:#d4af37; font-size: 1.5em; letter-spacing: 5px; margin-top:20px; text-transform: uppercase;">Assessment Verified</div>
                <div style="color:#888; text-align:center; max-width:600px; margin-top:30px; line-height:1.6; padding: 0 20px; font-family: sans-serif;">
                    Thank you very much for your time. Your data has been integrated into the CentrePort site plan. 
                    We have prioritized your inquiry and look forward to partnering in the future.
                </div>
                <div style="margin-top: 50px; color: #444; font-size: 0.7em; letter-spacing: 2px;">WINNIPEG, MB</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Please provide contact information.")
