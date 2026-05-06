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
        
        msg_to_admin = MIMEMultipart()
        msg_to_admin["From"] = f"EagleView Estates Portal <{sender_email}>"
        msg_to_admin["To"] = sender_email
        msg_to_admin["Subject"] = f"🚨 NEW EOI: {data['name']}"
        
        admin_body = f"EOI Received:\n\nCompany: {data['name']}\nContact: {data['contact']}\nSelection: {selected_scope}\n\nSigned: {data.get('signature', 'Inquiry Only')}"
        msg_to_admin.attach(MIMEText(admin_body, "plain"))

        msg_to_client = MIMEMultipart()
        msg_to_client["From"] = f"EagleView Estates <{sender_email}>"
        msg_to_client["To"] = data['contact']
        msg_to_client["Subject"] = f"Lease Options & Pricing: {data['name']}"
        
        client_body = f"""
Dear {data['name']},

Thank you for submitting your Expression of Interest for EagleView Estates.

Based on your selection for {selected_scope}, here is the dynamic pricing range:

--- LEASE OPTIONS & RATE RANGES ---
> Daily Rate: {p['Daily']}
> Weekly Rate: {p['Weekly']}
> Monthly Rate: {p['Monthly']}
> Yearly Rate: {p['Yearly']}
> Multi-Year: {p['Multi-Year']}

SITE DETAILS: {p['details']}
--------------------------------------

*PRICING NOTE: Rates are subject to change based on final site engineering and availability.*

Best regards,
The EagleView Team
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

# --- CSS: GOLD & BLACK THEME ---
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
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.2);
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
    
    with st.form("assessment_form"):
        st.markdown("### <span class='gold-text'>Strategic Site Assessment</span>", unsafe_allow_html=True)
        q1 = st.selectbox("1. Operational Scope", list(PRICING_DEALS.keys()))
        q2 = st.select_slider("2. Strategic Value of Location", options=["Low", "Neutral", "Important", "Strategic", "Critical"])
        q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Summer 2026", "Fall/Winter 2026"])
        q4 = st.multiselect("4. Critical Site Amenities", ["Biometric Access", "LED Lighting", "CCTV Surveillance", "Engineered Gravel"])
        q5 = st.radio("5. Execute an Expression of Interest to unlock full-term pricing ranges?", ["YES - Submit EOI", "NO - Just send general info"])
        
        name = st.text_input("Company / Representative Name")
        contact = st.text_input("Direct Email")
        
        if st.form_submit_button("VALIDATE & CONTINUE"):
            if name and contact:
                st.session_state.user_data = {"name": name, "contact": contact, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5}
                if "YES" in q5: st.session_state.page = 'eoi'
                else:
                    send_emails(st.session_state.user_data)
                    st.session_state.page = 'thankyou'
                st.rerun()
            else: st.warning("All fields required.")

# --- PAGE 2: STATEMENT OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <h2 style='text-align: center; color: #d4af37; text-transform: uppercase;'>Expression of Interest</h2>
        <p><span class='gold-text'>PROSPECTIVE TENANT:</span> {st.session_state.user_data['name']}</p>
        <hr style='border: 0.5px solid #d4af37;'>
        <p><b>1. SCOPE:</b> Requirement identified for <span class='gold-text'>{st.session_state.user_data['q1']}</span>.</p>
        <p><b>2. TERMS:</b> Accessing pricing across <b>Daily, Weekly, Monthly, Yearly, and Multi-Year</b> terms.</p>
        <p><b>3. PRIORITY:</b> Establishing site queue position for <b>{st.session_state.user_data['q3']}</b> window.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Digital Signature (Full Name & Title)")
    if st.button("EXECUTE EOI & UNLOCK ALL PRICING"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_emails(st.session_state.user_data, is_eoi=True)
            st.session_state.page = 'thankyou'
            st.rerun()

# --- PAGE 3: THANK YOU & JUNK WARNING ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; margin-top:30px; font-size:4em;'>✔️</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.8em; text-align:center; letter-spacing: 5px;'>EOI VERIFIED</div>", unsafe_allow_html=True)
    
    # RE-ENGINEERED JUNK WARNING BOX
    st.markdown(f"""
        <div style='color:#ffffff; text-align:center; max-width:600px; margin: 30px auto; line-height:1.6; font-size:1.1em;'>
            Thank you, <span class='gold-text'>{st.session_state.user_data['name']}</span>. <br>
            Your requirements are now being reviewed by our development team. <br><br>
            Your <b>Full Multi-Term Pricing Package</b> has been dispatched to: <br>
            <span style='color:#d4af37; font-family:monospace; font-size:1.2em;'>{st.session_state.user_data['contact']}</span>
        </div>
        
        <div style='background: linear-gradient(145deg, #1a1a1a, #000000); 
                    border: 2px solid #d4af37; 
                    padding: 25px; 
                    border-radius: 10px; 
                    text-align: center; 
                    max-width: 600px; 
                    margin: 40px auto;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);'>
            <h4 style='color: #d4af37; margin-top: 0; text-transform: uppercase; letter-spacing: 2px;'>⚠️ Critical Action Required</h4>
            <p style='color: #ffffff; margin-bottom: 15px;'>If you do not see our pricing package in your inbox within 60 seconds:</p>
            <ul style='color: #ffffff; text-align: left; display: inline-block; margin-bottom: 0;'>
                <li>Check your <b style='color: #d4af37;'>Junk or Spam folder</b>.</li>
                <li>Mark the email as <b style='color: #d4af37;'>"Not Junk"</b>.</li>
                <li>Add <b style='color: #d4af37;'>info@eagleviewearthworks.com</b> to your contacts.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
