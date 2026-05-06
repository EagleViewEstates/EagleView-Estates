import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | EOI Portal", layout="centered", page_icon="🦅")

# --- DUAL-EMAIL FUNCTION (Sends to You AND the Client) ---
def send_emails(data, is_eoi=False):
    try:
        sender_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]
        
        # 1. NOTIFICATION TO YOU
        msg_to_admin = MIMEMultipart()
        msg_to_admin["From"] = sender_email
        msg_to_admin["To"] = sender_email
        msg_to_admin["Subject"] = f"🚨 NEW EOI: {data['name']} - CentrePort"
        
        admin_body = f"Expression of Interest Received:\n\nCompany: {data['name']}\nContact: {data['contact']}\nScope: {data['q1']}\nTimeline: {data['q3']}\n\nSigned: {data.get('signature', 'Inquiry Only')}"
        msg_to_admin.attach(MIMEText(admin_body, "plain"))

        # 2. THANK YOU TO CLIENT
        msg_to_client = MIMEMultipart()
        msg_to_client["From"] = sender_email
        msg_to_client["To"] = data['contact'] # Assumes they entered an email
        msg_to_client["Subject"] = "Expression of Interest Received - EagleView Estates"
        
        client_body = f"""
Dear {data['name']},

Thank you very much for your time and interest in EagleView Estates at CentrePort.

We have received your Expression of Interest for the {data['q1']} configuration. Our team is currently reviewing the site engineering plans for the June 1st deployment.

We will be sending over formal lease options and pricing details to this email address immediately.

We look forward to partnering in the future.

Best regards,

The Development Team
EagleView Estates | Winnipeg, MB
        """
        msg_to_client.attach(MIMEText(client_body, "plain"))

        # Execute Sending
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, msg_to_admin.as_string())
        # Attempt to send to client (might fail if they provided a phone number)
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
    }
    .stButton>button { 
        background-color: #d4af37 !important; color: #000 !important; font-weight: bold; border-radius: 0; 
        height: 4em; border: none; letter-spacing: 2px; text-transform: uppercase; width: 100%;
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
        st.write("### Strategic Site Assessment")
        q1 = st.selectbox("1. Operational Scope", ["💎 ANCHOR TENANT: 5-Acre Parcel", "Dedicated Pad (1-5k sqft)", "Hourly Flex Staging", "Winter Storage"])
        q2 = st.select_slider("2. Strategic Value of Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
        q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Summer 2026", "Fall/Winter 2026"])
        q4 = st.multiselect("4. Critical Site Amenities", ["Biometric Access", "LED Lighting", "CCTV", "Engineered Gravel", "Site Maintenance"])
        q5 = st.radio("5. Would you like to submit a formal Expression of Interest for priority site-plan integration?", ["YES - Submit EOI", "NO - Just send general info"])
        
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
                st.warning("Please provide contact details.")

# --- PAGE 2: EXPRESSION OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <h3 style='text-align:center; border-bottom: 1px solid #1a1a1a; padding-bottom:10px;'>EXPRESSION OF INTEREST</h3>
        <p><b>PROSPECTIVE TENANT:</b> {st.session_state.user_data['name']}<br>
        <b>DEVELOPMENT:</b> CentrePort Canada Hub</p>
        <p>By submitting this Expression of Interest (EOI), the Prospective Tenant confirms a strategic interest in securing space at the EagleView Estates development for the <b>{st.session_state.user_data['q3']}</b> window.</p>
        <p><b>NEXT STEPS:</b> Upon submission, EagleView Estates will immediately transmit current lease options, engineered site specs, and pricing structures to the contact provided.</p>
        <p><i>Note: This is a non-binding expression of interest used for site configuration and queue priority.</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Type Full Name to Confirm Interest")
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
            Thank you very much for your time, <b>{st.session_state.user_data['name']}</b>. <br><br>
            An automated confirmation has been sent to <b>{st.session_state.user_data['contact']}</b>. 
            Please check your inbox immediately for lease options and pricing details.
            <br><br>
            We look forward to partnering in the future.
        </div>
    """, unsafe_allow_html=True)
