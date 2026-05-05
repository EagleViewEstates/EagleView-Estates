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
    .subtext { color: #a1a1aa !important; font-size: 1.1em; text-align: center; margin-bottom: 40px; letter-spacing: 1px;}
    
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
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #ffffff; color: #000000; border: 1px solid #ffffff; }
    
    /* Dark Mode Pricing Boxes */
    .price-box { 
        padding: 30px; 
        background-color: #0a0a0a; 
        border-radius: 2px; 
        border: 1px solid #1f2937; 
        text-align: center; 
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
        margin-top: 20px;
    }
    
    .promo-text { color: #34d399 !important; font-weight: bold; font-size: 0.9em; letter-spacing: 0.5px; text-transform: uppercase;}
    
    /* Style Tabs for Dark Mode */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #1f2937; }
    .stTabs [data-baseweb="tab"] { color: #a1a1aa; padding: 15px 25px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (The Visual Punch) ---
st.markdown("<h1 style='text-align: center; font-size: 3.5em; font-weight: 200; letter-spacing: 8px; margin-top: 50px;'>EAGLEVIEW</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1.2em; font-weight: 400; letter-spacing: 4px; color: #a1a1aa !important;'>ESTATES</h3>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Premium Industrial Storage | CentrePort Canada</p>", unsafe_allow_html=True)

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
        st.markdown(f"<p class='promo-text'>✓ PLATINUM STATUS: 6-Month Term Applied (1st Month Free)</p>", unsafe_allow_html=True)

    final_due = total_contract_value - savings

    st.markdown(f"""
        <div class="price-box">
            <p style='color:#a1a1aa; text-transform: uppercase; font-size: 0.75em; letter-spacing: 2px;'>Projected Contract Total</p>
            <h2 style='color:#ffffff; font-size: 3em; margin: 10px 0; font-weight: 300;'>${final_due:,.2f}</h2>
            <p style='color:#a1a1aa;'>Initial Security Deposit: <span style='color:#ffffff; font-weight:bold;'>${base_price if lease_term < 6 else 0:,.2f}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.write("") 
    if st.button("AUTHORIZE LEASE & PAYMENT"):
        st.toast("Connecting to Secure Encryption Layer...", icon="🔒")
        # In live: st.link_button("Complete Checkout", "YOUR_STRIPE_LINK")

# --- TAB 2: HOURLY QUICK-PARK ---
with tab2:
    st.write("### On-Demand Staging")
    
    hr_col1, hr_col2 = st.columns(2)
    with hr_col1:
        hours = st.number_input("Hours Required", 1, 24, 2)
    with hr_col2:
        vehicle_type = st.radio("Asset Class", ["Service Vehicle", "Transport/Semi", "Heavy Civil Machinery"])

    hr_rates = {"Service Vehicle": 15, "Transport/Semi": 25, "Heavy Civil Machinery": 40}
    total_hr = hr_rates[vehicle_type] * hours

    st.markdown(f"""
        <div class="price-box" style="padding: 20px;">
            <p style='color:#a1a1aa; text-transform: uppercase; font-size: 0.75em;'>Rate for {hours} Hours</p>
            <h3 style='margin:0;'>${total_hr:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("REQUEST INSTANT PIN"):
        st.code(f"TEMPORARY ACCESS PIN: #EV-{datetime.datetime.now().strftime('%M%S')}")

# --- TAB 3: MAINTENANCE & REFERRALS ---
with tab3:
    st.write("### Earthworks Maintenance")
    with st.expander("Request Site Service"):
        st.selectbox("Service Classification", ["Precision Grading", "Winter Maintenance", "Dust Suppression"])
        st.button("DISPATCH CREW")

    st.divider()
    
    st.write("### Partnership Network")
    st.write("Refer a qualified industry partner for a $500 premium credit.")
    ref_code = st.text_input("Enter Referral Code")
    if ref_code:
        st.success("Referral code active.")
