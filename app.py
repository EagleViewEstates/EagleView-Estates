import streamlit as st
import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView estates", layout="centered", page_icon="🦅")

# Custom CSS for the EagleView Brand
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background: #1e40af; border: none; }
    .price-box { padding: 20px; background-color: #ffffff; border-radius: 15px; border: 2px solid #e2e8f0; text-align: center; }
    .promo-text { color: #16a34a; font-weight: bold; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- DAILY PROMPT / NOTIFICATION ---
# Use st.toast for a "Daily Prompt" that disappears, or st.info for a sticky one.
st.toast("🚨 JUNE 1st LAUNCH: Only 4 Heavy Civil Pads remaining at Red Fife Rd!", icon="🔥")

# --- APP NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["🏗️ Monthly Lease", "⏱️ Hourly Quick-Park", "🚜 Maintenance & Referrals"])

# --- TAB 1: MONTHLY LEASE (With Promo Logic) ---
with tab1:
    st.title("🦅 EagleView Estates")
    st.caption("Secure Industrial Storage | CentrePort, MB")

    col_a, col_b = st.columns(2)
    with col_a:
        pad_choice = st.selectbox("Select Pad Size", ["Small Trade (1k sqft)", "Contractor (2.5k sqft)", "Heavy Civil (5k sqft)"])
    with col_b:
        lease_term = st.slider("Lease Duration (Months)", 1, 12, 1)

    # Base Pricing Data
    rates = {"Small Trade (1k sqft)": 1500, "Contractor (2.5k sqft)": 2500, "Heavy Civil (5k sqft)": 3750}
    base_price = rates[pad_choice]
    
    # PROMO LOGIC: 6 Months = 1st Month Free
    total_contract_value = base_price * lease_term
    savings = 0
    if lease_term >= 6:
        savings = base_price
        st.markdown(f"<p class='promo-text'>✅ '6-MONTH BULK' APPLIED: 1st Month is FREE (${base_price:,.0f} value)</p>", unsafe_allow_html=True)

    final_due = total_contract_value - savings

    st.markdown(f"""
        <div class="price-box">
            <h4 style='color:gray;'>Total Contract Value</h4>
            <h2 style='color:#1e3a8a;'>${final_due:,.2f}</h2>
            <p>Due Today: ${base_price if lease_term < 6 else 0:,.2f}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("RESERVE PAD & SIGN LEASE"):
        st.balloons()
        st.success("Redirecting to Secure Payment...")

# --- TAB 2: HOURLY QUICK-PARK ---
with tab2:
    st.title("⏱️ Hourly Quick-Park")
    st.write("Need a spot for a few hours? Book instantly.")
    
    hr_col1, hr_col2 = st.columns(2)
    with hr_col1:
        hours = st.number_input("How many hours?", 1, 24, 2)
    with hr_col2:
        vehicle_type = st.radio("Vehicle Type", ["Service Van", "Semi-Truck", "Heavy Equipment"])

    hr_rates = {"Service Van": 15, "Semi-Truck": 25, "Heavy Equipment": 40}
    total_hr = hr_rates[vehicle_type] * hours

    st.info(f"Total for Hourly Parking: **${total_hr:,.2f}**")
    if st.button("GENERATE ONE-TIME ACCESS CODE"):
        st.code(f"GATE CODE: #FIFE-{datetime.datetime.now().strftime('%M%S')}")

# --- TAB 3: MAINTENANCE & REFERRALS ---
with tab3:
    st.subheader("🚜 Earthworks Maintenance")
    with st.expander("Request Site Service"):
        st.selectbox("Service Required", ["Gravel Grading", "Snow Clearing", "Dust Control"])
        st.button("Dispatch EagleView Crew")

    st.divider()
    
    st.subheader("🤝 Refer-a-Friend")
    st.write("Refer a fellow contractor. If they sign a 6-month lease, you get **$500 off** your next month.")
    ref_code = st.text_input("Enter Friend's Referral Code to Apply Discount")
    if ref_code:
        st.success("Referral code valid! $500 will be deducted from checkout.")
