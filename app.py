import streamlit as st
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Closing Portal", layout="centered", page_icon="🦅")

# --- EMAIL FUNCTION (Saves Results + Digital Signature) ---
def send_deal_email(data, signed=False):
    try:
        sender_email = "info@eagleviewearthworks.com"
        receiver_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]
        
        status = "✅ SIGNED LOI" if signed else "👀 INQUIRY ONLY"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"{status}: {data['name']} - CentrePort"

        body = f"""
        EagleView Estates - Site Assessment Record:
        
        Status: {status}
        Company: {data['name']}
        Contact: {data['contact']}
        
        Scope: {data['q1']}
        Value of Location: {data['q2']}
        Timeframe: {data['q3']}
        Amenities: {data['q4']}
        Pre-Lease Interest: {data['q5']}
        
        Digital Signature: {data.get('signature', 'N/A')}
        Date/Timestamp: 2026-05-05 (EST)
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

# --- CSS: THE BILLION DOLLAR BRANDING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .brand-gold {
        text-align: center; font-family: 'serif'; font-size: 3.5em; font-weight: 200; letter-spacing: 10px;
        margin: 40px 0 10px 0; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase;
    }
    .sub-brand { text-align: center; color: #d4af37; letter-spacing: 4px; font-size: 0.9em; text-transform: uppercase; margin-bottom: 40px; }
    .loi-box {
        background-color: #111; border: 1px solid #d4af37; padding: 30px; border-radius: 4px;
        font-family: 'Courier New', Courier, monospace; color: #ccc; line-height: 1.5; font-size: 0.9em;
    }
    .stButton>button { 
        background-color: #d4af37 !important; color: #000 !important; font-weight: bold; border-radius: 0; 
        height: 3.5em; border: none; letter-spacing: 2px; text-transform: uppercase; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'assessment'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- PAGE 1: ASSESSMENT ---
if st.session_state.page == 'assessment':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-brand'>CentrePort Canada • Winnipeg</div>", unsafe_allow_html=True)

    if os.path.exists("site_photo.jpg"):
        st.image("site_photo.jpg", use_column_width=True)

    with st.form("assessment_form"):
        st.write("### Strategic Site Assessment")
        q1 = st.selectbox("1. Operational Scope", ["💎 ANCHOR TENANT: 5-Acre Parcel", "Dedicated Pad (1-5k sqft)", "Hourly Flex Staging", "Seasonal Overload"])
        q2 = st.select_slider("2. Strategic Value of Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
        q3 = st.radio("3. Target Move-in", ["June 1st", "Summer 2026", "Fall 2026"])
        q4 = st.multiselect("4. Must-Have Amenities", ["Biometric Gate", "LED Lighting", "Live CCTV Feed", "Snow Removal", "Grading Support"])
        q5 = st.radio("5. Secure your position with a 'Pre-Lease' intent?", ["YES - Finalize Intent Now", "MAYBE - Send details", "NO - Not now"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        name = st.text_input("Company / Representative Name")
        contact = st.text_input("Direct Phone or Email")
        
        submit = st.form_submit_button("CONTINUE TO VERIFICATION")

        if submit:
            if name and contact:
                st.session_state.user_data = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
                if q5 == "YES - Finalize Intent Now":
                    st.session_state.page = 'loi'
                    st.rerun()
                else:
                    send_deal_email(st.session_state.user_data, signed=False)
                    st.session_state.page = 'thankyou'
                    st.rerun()
            else:
                st.warning("Please provide contact details.")

# --- PAGE 2: DIGITAL LOI ---
elif st.session_state.page == 'loi':
    st.markdown("<div class='brand-gold'>Letter of Intent</div>", unsafe_allow_html=True)
    st.write("### Priority Reservation Terms")
    
    st.markdown(f"""
    <div class='loi-box'>
        <b>RE: CentrePort Industrial Expansion (June 1st Launch)</b><br><br>
        This Letter of Intent (LOI) summarizes the basic terms upon which <b>{st.session_state.user_data['name']}</b> 
        would lease industrial staging space from EagleView Estates.<br><br>
        1. <b>CONCURRENT ENGINEERING:</b> Developer is currently finalizing site engineering for a {st.session_state.user_data['q1']}.<br>
        2. <b>CONTINGENCY:</b> This intent is subject to Developer securing final municipal permits and grading approvals.<br>
        3. <b>FORCE MAJEURE:</b> In the event of construction delays or extenuating circumstances beyond the Developer's control, 
        this LOI may be voided by the Developer without penalty.<br>
        4. <b>NON-BINDING:</b> This document represents a serious intent to lease but is not a final binding lease agreement.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    sig = st.text_input("Type Full Name to Digitally Sign")
    
    if st.button("EXECUTE INTENT & CLOSE"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_deal_email(st.session_state.user_data, signed=True)
            st.session_state.page = 'thankyou'
            st.rerun()
        else:
            st.error("Signature required to execute.")

# --- PAGE 3: THANK YOU ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.5em; text-align:center; letter-spacing: 5px;'>DEAL VERIFIED</div>", unsafe_allow_html=True)
    st.write("")
    st.write(f"Thank you, {st.session_state.user_data['name']}. Your data has been integrated into our June 1st site plan.")
    st.write("We have received your priority inquiry and look forward to partnering in the future.")
    st.balloons()
