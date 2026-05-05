import streamlit as st
import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates", layout="centered", page_icon="🦅")

# Custom CSS for the Deep Black & Elegant Aesthetic
st.markdown("""
    <style>
    /* Force Deep Black Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Elegant Typography */
    h1, h2, h3, h4, p, span { color: #ffffff !important; font-family: 'Helvetica Neue', sans-serif; }
    .subtext { color: #a1a1aa !important; font-size: 1.1em; text-align: center; margin-bottom: 20px;}
    
    /* Sleek, Premium Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        height: 3.5em; 
        background-color: #1a1a1a; 
        color: #ffffff; 
        font-weight: bold; 
        border: 1px solid #333333; 
        transition: 0.3s;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #ffffff; color: #000000; border: 1px solid #ffffff; }
    
    /* Dark Mode Pricing Boxes */
    .price-box { 
        padding: 25px; 
        background-color: #0a0a0a; 
        border-radius: 8px; 
        border: 1px solid #1f2937; 
        text-align: center; 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .promo-text { color: #34d399 !important; font-weight: bold; font-size: 0.9em; letter-spacing: 0.5px;}
    
    /* Style Tabs for Dark Mode */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #a1a1aa; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DAILY PROMPT / NOTIFICATION ---
st.toast("🚨 JUNE 1st LAUNCH: Phase 1 Pads available for immediate reservation.", icon="🦅")

# --- HEADER & VIDEO (The Cinematic First Page) ---
st.markdown("<h1 style='text-align: center; font-size: 3em; font-weight: 300; letter-spacing: 3px;'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>The Pinnacle of Modern Industrial Design | CentrePort, MB</p>", unsafe_allow_html=True)

# Embed the Video (Requires the mp4 file in your GitHub repo)
try:
    st.video("eagleview_promo.mp4", format="video/mp4", start_time=0)
except Exception as e:
    st.info("Video loading... Please ensure 'eagleview_promo.mp4' is in the repository.")

st.divider()

# --- APP NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["RESERVE MONTHLY", "HOURLY QUICK-PARK", "MAINTENANCE & REFERRALS"])

# --- TAB 1: MONTHLY LEASE ---
with tab1:
    st.write("### Secure Your Space")
    
    col_a, col_b = st.columns(2)
    with col_a:
        pad_choice = st.selectbox("Select Pad Configuration", ["Trade Pad (1k sqft)", "Contractor Hub (2.5k sqft)", "Heavy Civil Fleet (5k sqft)"])
    with col_b:
        lease_term = st.slider("Lease Duration (Months)", 1, 12, 1)

    rates = {"Trade Pad (1k sqft)": 1500, "Contractor Hub (2.5k sqft)": 2500, "Heavy Civil Fleet (5k sqft)": 3750}
    base_price = rates[pad_choice]
    
    total_contract_value = base_price * lease_term
    savings = 0
    if lease_term >= 6:
        savings = base_price
        st.markdown(f"<p class='promo-text'>✓ PLATINUM TIER APPLIED: First Month Complimentary (${base_price:,.0f} value)</p>", unsafe_allow_html=True)

    final_due = total_contract_value - savings

    st.markdown(f"""
        <div class="price-box">
            <p style='color:#a1a1aa; text-transform: uppercase; font-size: 0.8em; letter-spacing: 1px;'>Total Contract Value</p>
            <h2 style='color:#ffffff; font-size: 2.5em; margin: 10px 0;'>${final_due:,.2f}</h2>
            <p style='color:#a1a1aa;'>Due Today to Secure Gate Access: <span style='color:#ffffff; font-weight:bold;'>${base_price if lease_term < 6 else 0:,.2f}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Spacer
    if st.button("AUTHORIZE LEASE & PAYMENT"):
        st.success("Redirecting to Secure Encrypted Checkout...")

# --- TAB 2: HOURLY QUICK-PARK ---
with tab2:
    st.write("### On-Demand Access")
    
    hr_col1, hr_col2 = st.columns(2)
    with hr_col1:
        hours = st.number_input("Duration Requested (Hours)", 1, 24, 2)
    with hr_col2:
        vehicle_type = st.radio("Asset Classification", ["Service Vehicle", "Transport/Semi", "Heavy Civil Machinery"])

    hr_rates = {"Service Vehicle": 15, "Transport/Semi": 25, "Heavy Civil Machinery": 40}
    total_hr = hr_rates[vehicle_type] * hours

    st.markdown(f"""
        <div class="price-box" style="padding: 15px;">
            <h4>Total for {hours} Hours: ${total_hr:,.2f}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("GENERATE TEMPORARY GATE CODE"):
        st.code(f"TEMPORARY ACCESS PIN: #EV-{datetime.datetime.now().strftime('%M%S')}")

# --- TAB 3: MAINTENANCE & REFERRALS ---
with tab3:
    st.write("### Earthworks Fleet Services")
    with st.expander("Request On-Site Maintenance"):
        st.selectbox("Service Classification", ["Precision Grading", "Winter Maintenance / Snow", "Dust Suppression"])
        st.button("DISPATCH EAGLEVIEW CREW")

    st.divider()
    
    st.write("### The EagleView Network")
    st.write("Refer a qualified industry partner. A 6-month lease signature grants a **$500 premium credit** to your account.")
    ref_code = st.text_input("Enter Partner Referral Code")
    if ref_code:
        st.success("Referral verified. Credit will be applied at checkout.")
