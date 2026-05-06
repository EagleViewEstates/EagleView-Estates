import streamlit as st
import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | EOI Portal", layout="centered", page_icon="🦅")

# --- BACKGROUND IMAGE HELPER ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(bin_file):
    if os.path.exists(bin_file):
        bin_str = get_base64_of_bin_file(bin_file)
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    else:
        st.markdown("<style>.stApp { background-color: #050505; }</style>", unsafe_allow_html=True)

# Apply Background
set_png_as_page_bg('site_photo.jpg')

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

# --- EMAIL LOGIC ---
def send_emails(data):
    try:
        sender_email = "info@eagleviewearthworks.com"
        password = st.secrets["EMAIL_PASSWORD"]
        p = PRICING_DEALS.get(data['q1'])
        
        msg = MIMEMultipart()
        msg["From"] = f"EagleView Estates <{sender_email}>"
        msg["To"] = data['contact']
        msg["Subject"] = f"Priority Pricing: {data['name']}"
        
        body = f"Dear {data['name']},\n\nSelection: {data['q1']}\n\nTerm Pricing:\n- Daily: {p['Daily']}\n- Weekly: {p['Weekly']}\n- Monthly: {p['Monthly']}\n- Yearly: {p['Yearly']}\n- Multi-Year: {p['Multi-Year']}\n\nSite Details: {p['details']}"
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, data['contact'], msg.as_string())
        server.quit()
        return True
    except: return False

# --- GLOBAL STYLING ---
st.markdown("""
    <style>
    .brand-gold {
        text-align: center; font-family: 'serif'; font-size: 3.5em; font-weight: 200; letter-spacing: 10px;
        margin: 40px 0 10px 0; background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase;
    }
    .sub-brand { text-align: center; color: #d4af37; letter-spacing: 4px; font-size: 0.8em; text-transform: uppercase; margin-bottom: 40px; }
    .gold-text { color: #d4af37; font-weight: bold; }
    [data-testid="stForm"] { background-color: rgba(0, 0, 0, 0.7) !important; border: 1px solid #d4af37 !important; padding: 30px !important; }
    .eoi-document {
        background-color: rgba(0, 0, 0, 0.9); color: #ffffff; padding: 45px; border: 1px solid #d4af37;
        border-radius: 2px; font-family: 'serif'; line-height: 1.4; margin-bottom: 30px;
        box-shadow: 0 0 40px rgba(212, 175, 55, 0.2);
    }
    .stButton>button { background-color: #d4af37 !important; color: #000 !important; font-weight: bold; border-radius: 0; height: 4em; width: 100%; border: none; letter-spacing: 2px; }
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
        q3 = st.radio("3. Target Deployment Date", ["June 1st - Immediate", "Summer 2026", "Fall/Winter 2026"])
        name = st.text_input("Company / Representative Name")
        contact = st.text_input("Direct Email")
        
        if st.form_submit_button("VALIDATE & CONTINUE"):
            if name and contact:
                st.session_state.user_data = {"name": name, "contact": contact, "q1": q1, "q3": q3}
                st.session_state.page = 'eoi'
                st.rerun()
            else: st.warning("All fields required.")

# --- PAGE 2: STATEMENT OF INTEREST ---
elif st.session_state.page == 'eoi':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='eoi-document'>
        <h2 style='text-align: center; color: #d4af37; text-transform: uppercase;'>Statement of Interest</h2>
        <p><span class='gold-text'>PROSPECTIVE TENANT:</span> {st.session_state.user_data.get('name', 'Valued Partner')}</p>
        <hr style='border: 0.5px solid #d4af37;'>
        <p><b>1. SCOPE:</b> Requirement identified for <span class='gold-text'>{st.session_state.user_data.get('q1')}</span>.</p>
        <p><b>2. PRIORITY:</b> Establishing site queue position for <b>{st.session_state.user_data.get('q3')}</b> window.</p>
        <p style='font-size: 0.8em; color: #888;'>By signing, you unlock full-term pricing ranges for the selection above.</p>
    </div>
    """, unsafe_allow_html=True)
    
    sig = st.text_input("Digital Signature (Full Name & Title)")
    if st.button("EXECUTE & UNLOCK PRICING"):
        if sig:
            st.session_state.user_data['signature'] = sig
            send_emails(st.session_state.user_data)
            st.session_state.page = 'thankyou'
            st.rerun()

# --- PAGE 3: THANK YOU & JUNK WARNING ---
elif st.session_state.page == 'thankyou':
    st.markdown("<div class='brand-gold'>EagleView Estates</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; margin-top:30px; font-size:4em;'>✔️</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#d4af37; font-size: 1.8em; text-align:center; letter-spacing: 5px;'>EOI VERIFIED</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: linear-gradient(145deg, rgba(26,26,26,0.9), rgba(0,0,0,0.9)); border: 2px solid #d4af37; padding: 25px; border-radius: 10px; text-align: center; max-width: 600px; margin: 40px auto;'>
            <h4 style='color: #d4af37; margin-top: 0; text-transform: uppercase; letter-spacing: 2px;'>⚠️ Critical Action Required</h4>
            <p style='color: #ffffff;'>Check your <b style='color: #d4af37;'>Junk/Spam folder</b> if the pricing doesn't arrive within 60 seconds.</p>
            <p style='color: #ffffff;'>Mark the email as <b style='color: #d4af37;'>"Not Junk"</b> to ensure delivery of lease docs.</p>
        </div>
    """, unsafe_allow_html=True)
