import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Assessment", layout="centered", page_icon="🦅")

# --- EMAIL FUNCTION ---
def send_email(data):
    # These secrets are set in your Streamlit Cloud Dashboard (Settings > Secrets)
    # To test locally, you can replace these with strings, but DON'T push your password to GitHub!
    sender_email = "info@eagleviewearthworks.com"
    receiver_email = "info@eagleviewearthworks.com"
    password = st.secrets["EMAIL_PASSWORD"] # Generate an 'App Password' in your email settings

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"NEW LEAD: {data['name']} - EagleView Site Assessment"

    body = f"""
    New Market Assessment Received:
    
    Company/Name: {data['name']}
    Contact: {data['contact']}
    
    1. Operational Need: {data['q1']}
    2. Location Importance: {data['q2']}
    3. Timeframe: {data['q3']}
    4. Amenities: {data['q4']}
    5. Pre-Lease Interest: {data['q5']}
    """
    
    message.attach(MIMEText(body, "plain"))

    try:
        # Using Gmail/Google Workspace settings as default
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# --- PREMIUM BLACK & GOLD THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3em; font-weight: 200; letter-spacing: 7px; margin-top: 20px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .subtext { color: #d4af37 !important; font-size: 1em; text-align: center; margin-bottom: 20px; letter-spacing: 2px; text-transform: uppercase;}
    h3 { color: #d4af37 !important; font-weight: 300; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .stImage > img { border-radius: 4px; border: 1px solid #d4af37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.2); }
    .stButton>button { 
        width: 100%; border-radius: 0px; height: 3.5em; background-color: #d4af37; 
        color: #000000; font-weight: bold; border: none; letter-spacing: 2px; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #ffffff; color: #000000; box-shadow: 0 0 15px #d4af37; }
    .survey-card { padding: 25px; background-color: #0f0f0f; border: 1px solid #262626; border-radius: 4px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING ---
st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Infrastructure & Heavy Staging</p>", unsafe_allow_html=True)

# --- SITE PHOTO ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Red Fife Road - Secure Industrial Staging Area", use_column_width=True)

st.markdown("""
<div class='survey-card'>
    <h3>Strategic Site Assessment</h3>
    <p style='color: #888;'>We are securing a prime 1.5 to 5-acre parcel in the Rosser/CentrePort area. 
    Final site engineering is underway for June 1st deployment.</p>
</div>
""", unsafe_allow_html=True)

# --- SURVEY FORM ---
with st.form("demand_assessment", clear_on_submit=True):
    q1 = st.selectbox("1. Operational Need", ["Dedicated Pad (1-5k sqft)", "Anchor Tenant Parcel (1-5 Full Acres)", "Hourly/Daily Staging", "Winter Storage"])
    q2 = st.select_slider("2. Importance of CentrePort/Rosser Location", options=["Low", "Convenient", "Strategic", "Essential", "Critical"])
    q3 = st.radio("3. Desired Move-in Timeframe", ["Immediate (June 1st)", "Summer 2026", "Fall/Winter 2026"])
    q4 = st.multiselect("4. Critical Site Amenities", ["24/7 Gate", "LED Lighting", "CCTV", "Engineered Gravel", "Maintenance Support"])
    q5 = st.radio("5. Interest in a 'Pre-Lease' agreement to secure current rates and guaranteed space?", ["Yes", "Maybe", "No"])
    
    st.divider()
    name = st.text_input("Company / Contact Name")
    contact = st.text_input("Email or Phone")

    if st.form_submit_button("SUBMIT ASSESSMENT"):
        if name and contact:
            results = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
            
            # Attempt to send email
            if send_email(results):
                st.success("Thank you very much for your time. We have received your assessment and look forward to partnering in the future.")
                st.balloons()
            else:
                st.error("Submission failed. Please contact info@eagleviewearthworks.com directly.")
        else:
            st.warning("Please provide contact details.")

st.markdown("<br><p style='text-align: center; color: #444; font-size: 0.8em; letter-spacing: 3px;'>EAGLEVIEW ESTATES | ROSSER, MB</p>", unsafe_allow_html=True)
