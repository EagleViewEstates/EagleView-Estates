import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Assessment", layout="centered", page_icon="🦅")

# --- EMAIL FUNCTION ---
def send_email(data):
    try:
        sender_email = "info@eagleviewearthworks.com"
        receiver_email = "info@eagleviewearthworks.com"
        # Access secret securely from Streamlit dashboard
        password = st.secrets["EMAIL_PASSWORD"]

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"🚨 INSTANT PRE-LEASE INQUIRY: {data['name']}"

        body = f"""
        New High-Priority Strategic Assessment Received:
        
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
    except Exception as e:
        # st.error(f"Error: {e}") # Debugging
        return False

# --- PREMIUM BLACK & GOLD THEME & ANIMATIONS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Gold Title with Shimmer */
    .main-title {
        text-align: center; font-size: 3.5em; font-weight: 200; letter-spacing: 8px; margin-top: 20px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        animation: shimmer_text 5s infinite;
    }
    
    @keyframes shimmer_text { 0% { background-position: -500px; } 100% { background-position: 500px; } }
    
    .subtext { color: #d4af37 !important; font-size: 1.1em; text-align: center; margin-bottom: 20px; letter-spacing: 3px; text-transform: uppercase;}
    
    /* ANCHOR TENANT CALLOUT */
    .anchor-card {
        padding: 30px; background: linear-gradient(145deg, #0f0f0f, #1a1a1a);
        border: 2px solid #d4af37; border-radius: 8px; text-align: center;
        margin-bottom: 30px; box-shadow: 0 0 30px rgba(212, 175, 55, 0.15);
    }
    .anchor-highlight { color: #d4af37; font-size: 1.5em; font-weight: bold; letter-spacing: 2px; text-transform: uppercase;}
    
    h3 { color: #d4af37 !important; font-weight: 300; border-bottom: 1px solid #333; padding-bottom: 10px; }
    
    /* Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 0px; height: 4em; background-color: #d4af37; 
        color: #000000; font-weight: bold; border: none; letter-spacing: 2px; text-transform: uppercase;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    .stButton>button:hover { background-color: #ffffff; box-shadow: 0 0 30px rgba(212, 175, 55, 0.6); }
    
    /* Form Cards */
    .survey-card { padding: 25px; background-color: #0f0f0f; border: 1px solid #262626; border-radius: 4px; margin-bottom: 20px; }
    
    /* Assessment Verified Success Container */
    .success-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0, 0, 0, 0.95);
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        z-index: 1000;
        opacity: 0;
        animation: fade_in_overlay 1s forwards;
    }
    
    @keyframes fade_in_overlay { 100% { opacity: 1; } }
    
    /* Dynamic Eagle Build-Out SVG Animation */
    .eagle-build-out {
        width: 150px; height: 150px;
        fill: #d4af37;
        opacity: 0;
        animation: 
            build_out_eagle 0.8s 0.5s cubic-bezier(0.175, 0.885, 0.320, 1.275) forwards, 
            shimmer_eagle 3s 1.3s infinite;
    }
    
    @keyframes build_out_eagle {
        0% { transform: scale(0.5) rotate(-30deg); opacity: 0; }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }
    
    @keyframes shimmer_eagle {
        0% { box-shadow: 0 0 20px rgba(212, 175, 55, 0); }
        50% { box-shadow: 0 0 50px rgba(212, 175, 55, 0.6); }
        100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0); }
    }
    
    .premium-success-title {
        color: #d4af37; font-size: 2.2em; font-weight: bold; 
        margin-top: 30px; text-transform: uppercase; letter-spacing: 4px;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
    }
    .premium-success-text {
        color: #aaaaaa; font-size: 1.1em; margin-top: 15px; max-width: 80%; text-align: center;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & BRANDING ---
st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Site Selection & Demand Assessment</p>", unsafe_allow_html=True)

# --- ANCHOR TENANT FEATURE ---
st.markdown("""
<div class='anchor-card'>
    <p style='margin:0; font-size: 0.8em; color: #888;'>PREMIUM LOGISTICS HUB</p>
    <div class='anchor-highlight'>CENTREPORT 5-ACRE ANCHOR PARCEL</div>
    <p style='color: #ffffff; margin-top: 10px;'>Evaluating high-load expansion capabilities within CentrePort Canada, Winnipeg. 
    Custom site configurations available for June 1st deployment.</p>
</div>
""", unsafe_allow_html=True)

# --- SITE PHOTO ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Red Fife Road Development Area", use_column_width=True)

# --- SURVEY FORM ---
with st.form("anchor_survey", clear_on_submit=True):
    st.write("### Facility Requirements")
    
    q1 = st.selectbox("1. Operational Scope", ["💎 ANCHOR TENANT: 5-Acre Parcel", "Dedicated Pad (1-5k sqft)", "Hourly Flex Staging", "Seasonal Overload"])
    q2 = st.select_slider("2. Strategic Value of CentrePort Winnipeg Location", options=["Low Impact", "Convenient", "Strategic", "Essential", "Critical"])
    q3 = st.radio("3. Target Deployment Date", ["June 1st", "Summer 2026", "Fall/Winter 2026"])
    q4 = st.multiselect("4. High-Priority Amenities", ["Biometric Gate", "LED Lighting", "Live CCTV Feed", "Snow Removal", "Site Maintenance Support"])

    st.markdown("---")
    
    # 5. THE CRITICAL "PRE-LEASE" QUESTION
    q5 = st.radio("5. Secure your priority position with a 'Pre-Lease' agreement prior to the June 1st launch?", 
                 ["YES - Send terms immediately (Opens Real-Time Page)", 
                  "MAYBE - Send pricing details via email", 
                  "NO - Prefer on-demand availability"])

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Company / Representative Name")
    with col2:
        contact = st.text_input("Direct Phone or Email")

    submit_button = st.form_submit_button("SUBMIT PRIORITY ASSESSMENT")

# --- CUSTOM SUBMISSION LOGIC ---
if submit_button:
    if name and contact:
        results = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
        
        # 1. Always send the high-priority email notification
        email_success = send_email(results)
        
        # 2. Case: Contractor shows immediate interest
        if "YES" in q5:
            st.success("Prioritizing pre-lease terms. Redirecting to legal portal now...")
            
            # THE REAL-TIME REDIRECT: Add your legal/pre-lease DocuSign or Stripe URL here
            st.markdown("""
                <script type="text/javascript">
                window.open("your_instant_lease_url_here", "_blank");
                </script>
                """, unsafe_allow_html=True)
        
        # 3. Case: All other submissions (standard process)
        elif email_success:
            st.markdown("""
                <div class='success-overlay'>
                    <svg class='eagle-build-out' viewBox="0 0 100 100">
                        <path d="M50 0C22.4 0 0 22.4 0 50C0 77.6 22.4 100 50 100C77.6 100 100 77.6 100 50C100 22.4 77.6 0 50 0ZM72.7 63.6C69.3 67 64.9 69 60 69C55.1 69 50.7 67 47.3 63.6C43.9 60.2 41.9 55.8 41.9 50.9V36.4C41.9 31.5 43.9 27.1 47.3 23.7C50.7 20.3 55.1 18.3 60 18.3C64.9 18.3 69.3 20.3 72.7 23.7C76.1 27.1 78.1 31.5 78.1 36.4V50.9C78.1 55.8 76.1 60.2 72.7 63.6ZM60 63C56.1 63 52.6 61.4 50 58.9C47.4 56.4 45.8 52.9 45.8 49V38.3C45.8 34.4 47.4 30.9 50 28.4C52.6 25.9 56.1 24.3 60 24.3C63.9 24.3 67.4 25.9 70 28.4C72.6 30.9 74.2 34.4 74.2 38.3V49C74.2 52.9 72.6 56.4 70 58.9C67.4 61.4 63.9 63 60 63ZM27.3 63.6C23.9 67 19.5 69 14.6 69C9.7 69 5.3 67 1.9 63.6C-1.5 60.2 -3.5 55.8 -3.5 50.9V36.4C-3.5 31.5 -1.5 27.1 1.9 23.7C5.3 20.3 9.7 18.3 14.6 18.3C19.5 18.3 23.9 20.3 27.3 23.7C30.7 27.1 32.7 31.5 32.7 36.4V50.9C32.7 55.8 30.7 60.2 27.3 63.6ZM14.6 63C10.7 63 7.2 61.4 4.6 58.9C2 56.4 0.4 52.9 0.4 49V38.3C0.4 34.4 2 30.9 4.6 28.4C7.2 25.9 10.7 24.3 14.6 24.3C18.5 24.3 22 25.9 24.6 28.4C27.2 30.9 28.8 34.4 28.8 38.3V49C28.8 52.9 27.2 56.4 24.6 58.9C22 61.4 18.5 63 14.6 63Z"/>
                    </svg>
                    <div class='premium-success-title'>ASSESSMENT VERIFIED</div>
                    <div class='premium-success-text'>
                        We have received your strategic market assessment for CentrePort and prioritized your inquiry. Thank you for your time, we look forward to partnering in the future.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            # Brief sleep so the success is felt before disappearing
            import time
            time.sleep(2.5)
        else:
            st.error("Submission failed. Email system error. Please contact info@eagleviewearthworks.com directly.")
    else:
        st.warning("Please provide contact details to finalize.")

st.markdown("<br><p style='text-align: center; color: #333; font-size: 0.8em; letter-spacing: 3px; text-transform: uppercase;'>EAGLEVIEW ESTATES | WINNIPEG INDUSTRIAL</p>", unsafe_allow_html=True)
