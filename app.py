import streamlit as st
import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates", layout="centered", page_icon="🦅")

# Custom CSS for Deep Black, Electric Blue, and Crisp White
st.markdown("""
    <style>
    /* Force Deep Black Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Blue/White Gradient Typography */
    .main-title {
        text-align: center; 
        font-size: 3.5em; 
        font-weight: 200; 
        letter-spacing: 8px; 
        margin-top: 50px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h1, h2, h3 { color: #3b82f6 !important; font-family: 'Helvetica Neue', sans-serif; }
    h4, p, span, li { color: #ffffff !important; }
    
    .subtext { color: #60a5fa !important; font-size: 1.1em; text-align: center; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase;}
    
    /* Sleek, Premium Buttons with Blue Border */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        height: 3.5em; 
        background-color: #000000; 
        color: #3b82f6; 
        font-weight: bold; 
        border: 1px solid #1e40af; 
        transition: 0.3s;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #3b82f6; color: #ffffff; border: 1px solid #ffffff; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    
    /* Dark Mode Pricing Boxes with Blue Glow */
    .price-box { 
        padding: 30px; 
        background-color: #0a0a0a; 
        border-radius: 4px; 
        border: 1px solid #1e3a8a; 
        text-align: center; 
        box-shadow: 0 5px 20px -5px rgba(30, 58, 138, 0.4);
        margin-top: 20px;
    }
    
    .promo-text { color: #60a5fa !important; font-weight: bold; font-size: 0.9em; letter-spacing: 0.5px; text-transform: uppercase;}
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #1e3a8a; }
    .stTabs [data-baseweb="tab"] { color: #60a5fa; padding: 15px 25px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #3b82f6 !important; }
    
    /* Selectbox and Input Styling */
    div[data-baseweb="select"] > div { background-color: #111 !important; color: white !important; border: 1px solid #1e3a8a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>EAGLEVIEW</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1.2em; font-weight: 400; letter-spacing: 6px; color: #ffffff !important; margin-top: -20px;'>ESTATES</h3>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Storage | Infrastructure | Excellence</p>", unsafe_allow_html=True)

st.divider()

# --- APP NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["RESERVE MONTHLY", "HOURLY QUICK-PARK", "MAINTENANCE & REFERRALS"])

# --- TAB 1: MONTHLY LEASE ---
with tab1:
    st.write("### Configuration")
    
    col_a, col_b = st.columns(2)
    with col_a:
        pad_choice = st.selectbox("Pad Size", ["Trade Pad (1k sqft)", "Contractor Hub (2.5k sqft)", "Heavy Civil Fleet (5k sqft)"])
    with col_b:
        lease_term = st.slider("Duration (Months)", 1, 12, 1)

    rates = {"Trade Pad (1k sqft)": 1500, "Contractor Hub (2.5k sqft)": 2500, "Heavy Civil Fleet (5k sqft)": 3750}
    base_price = rates[pad_choice]
    
    total_contract_value = base_price * lease_term
    savings = 0
    if lease_term >= 6:
        savings = base_price
        st.markdown(f"<p class='promo-text'>✓ BLUE-TIER LOYALTY: 1st Month Complimentary</p>", unsafe_allow_html=True)

    final_due = total_contract_value - savings

    st.markdown(f"""
        <div class="price-box">
            <p style='color:#60a5fa; text-transform: uppercase; font-size: 0.75em; letter-spacing: 2px;'>Projected Total</p>
            <h2 style='color:#ffffff !important; font-size: 3.5em; margin: 10px 0; font-weight: 200;'>${final_due:,.2f}</h2>
            <p style='color:#60a5fa;'>Security Deposit: <span style='color:#ffffff; font-weight:bold;'>${base_price if lease_term < 6 else 0:,.2f}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") 
    if st.button("AUTHORIZE LEASE & GATE ACCESS"):
        st.toast("Connecting to Secure Blue-Shield Servers...", icon="🔵")

# --- TAB 2: HOURLY QUICK-PARK ---
with tab2:
    st.write("### Rapid Staging")
    
    hr_col1, hr_col2 = st.columns(2)
    with hr_col1:
        hours = st.number_input("Hours Requested", 1, 24, 2)
    with hr_col2:
        vehicle_type = st.radio("Asset Class", ["Service Vehicle", "Transport/Semi", "Heavy Civil Machinery"])

    hr_rates = {"Service Vehicle": 15, "Transport/Semi": 25, "Heavy Civil Machinery": 40}
    total_hr = hr_rates[vehicle_type] * hours

    st.markdown(f"""
        <div class="price-box" style="padding: 20px;">
            <p style='color:#60a5fa; text-transform: uppercase; font-size: 0.75em;'>Rate for {hours} Hours</p>
            <h3 style='margin:0; color:#ffffff !important;'>${total_hr:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("INSTANT ACCESS PIN"):
        st.code(f"PIN: #EV-{datetime.datetime.now().strftime('%M%S')}")

# --- TAB 3: MAINTENANCE & REFERRALS ---
with tab3:
    st.write("### Earthworks Maintenance")
    with st.expander("Request Site Service"):
        st.selectbox("Service Classification", ["Precision Grading", "Winter Maintenance", "Dust Suppression"])
        st.button("DISPATCH EAGLEVIEW CREW")

    st.divider()
    
    st.write("### Partnership Network")
    st.write("Refer a partner for a $500 premium credit.")
    ref_code = st.text_input("Enter Code")
    if ref_code:
        st.success("Referral active.")
