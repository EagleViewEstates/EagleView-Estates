import streamlit as st
import datetime

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="EagleView Estates - On-Demand Storage", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1E3A8A; color: white; }
    .price-box { padding: 20px; background-color: #ffffff; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🦅 EagleView Estates")
st.subheader("On-Demand Industrial Storage | Red Fife Road")

# --- STEP 1: SELECT PAD SIZE ---
st.write("### 1. Select Your Space")
pad_type = st.selectbox(
    "Choose a Pad Size",
    ["Small Trade Pad (1,000 sq ft)", "Contractor Pad (2,500 sq ft)", "Heavy Civil Pad (5,000 sq ft)", "Custom Oversized"]
)

# Logic for dynamic pricing based on your $0.75 - $1.50 model
pricing = {
    "Small Trade Pad (1,000 sq ft)": 1.50,
    "Contractor Pad (2,500 sq ft)": 1.00,
    "Heavy Civil Pad (5,000 sq ft)": 0.75,
    "Custom Oversized": 1.25
}

sq_ft_map = {
    "Small Trade Pad (1,000 sq ft)": 1000,
    "Contractor Pad (2,500 sq ft)": 2500,
    "Heavy Civil Pad (5,000 sq ft)": 5000,
    "Custom Oversized": 10000
}

rate = pricing[pad_type]
total_monthly = sq_ft_map[pad_type] * rate

# --- STEP 2: DURATION & MAINTENANCE ---
st.write("### 2. Duration & Services")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.date.today())
with col2:
    months = st.number_input("Months", min_value=1, max_value=12, value=1)

# EagleView Earthworks Integration
st.write("**EagleView Earthworks Add-ons:**")
snow_clearing = st.checkbox("Priority Snow Clearing (Direct to Equipment)")
equipment_wash = st.checkbox("Weekly Mobile Pressure Wash")

service_fee = 0
if snow_clearing: service_fee += 150
if equipment_wash: service_fee += 300

# --- STEP 3: TOTALS ---
final_total = total_monthly + service_fee
st.markdown(f"""
<div class="price-box">
    <h4>Monthly Quote: ${final_total:,.2f}</h4>
    <p style='color: gray;'>Rate: ${rate}/sq ft | Location: 3275 Red Fife Rd (Rosser)</p>
</div>
""", unsafe_allow_html=True)

# --- STEP 4: LEGAL & CHECKOUT ---
st.write("### 3. Finalize & Sign")
with st.expander("Read Rental Agreement (Digital Signature Required)"):
    st.write("""
    **EagleView Estates Terms of Service:**
    - I agree to provide proof of insurance for all equipment.
    - I indemnify EagleView Estates and the Landlord against any environmental spills.
    - No hazardous waste storage permitted.
    - RM of Rosser bylaws apply.
    """)

agreed = st.checkbox("I have read and agree to the Digital Lease Agreement.")

if st.button("BOOK NOW & GET ACCESS CODE"):
    if agreed:
        st.success(f"SUCCESS! Payment of ${final_total:,.2f} processed via Stripe.")
        st.balloons()
        st.info("🔓 YOUR GATE ACCESS CODE: **#2026-FIFE**")
        st.write("A copy of the signed lease and site map has been sent to your email.")
    else:
        st.warning("Please agree to the terms to proceed.")
