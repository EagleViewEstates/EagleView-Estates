import streamlit as st
import datetime

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="EagleView Estates & Earthworks", layout="centered", page_icon="🦅")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1e40af; color: white; font-weight: bold; }
    .price-box { padding: 20px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .maintenance-card { padding: 15px; border-left: 5px solid #fbbf24; background-color: #fffbeb; margin-bottom: 10px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- APP NAVIGATION ---
tab1, tab2 = st.tabs(["🏗️ Book Storage (Estates)", "🚜 Maintenance Hub (Earthworks)"])

# --- TAB 1: EAGLEVIEW ESTATES (THE LEASING APP) ---
with tab1:
    st.title("🦅 EagleView Estates")
    st.info("Direct Access Contractor Yards | Red Fife Road, Rosser")

    st.write("### 1. Choose Your Pad")
    pad_choice = st.radio("Standard Pad Sizes:", 
                          ["Small Trade (1,000 sq ft)", "Contractor Pad (2,500 sq ft)", "Heavy Civil (5,000 sq ft)"],
                          horizontal=True)

    # Pricing Logic ($0.75 - $1.50)
    pricing_data = {
        "Small Trade (1,000 sq ft)": {"rate": 1.50, "sqft": 1000},
        "Contractor Pad (2,500 sq ft)": {"rate": 1.00, "sqft": 2500},
        "Heavy Civil (5,000 sq ft)": {"rate": 0.75, "sqft": 5000}
    }

    selected = pricing_data[pad_choice]
    monthly_rent = selected['rate'] * selected['sqft']

    st.write("### 2. Add-On Services")
    col1, col2 = st.columns(2)
    with col1:
        snow = st.checkbox("Priority Snow Clear", help="Earthworks clears right to your bumper")
    with col2:
        wash = st.checkbox("Bi-Weekly Unit Wash")

    extra_fees = (150 if snow else 0) + (250 if wash else 0)
    total = monthly_rent + extra_fees

    st.markdown(f"""
        <div class="price-box">
            <h2 style='margin:0; color:#1e40af;'>${total:,.2f} / month</h2>
            <p style='color:#64748b;'>Zoning: I2 General Industrial | Access: 24/7 Automated</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("PROCEED TO SECURE CHECKOUT"):
        st.warning("🔗 Redirecting to Stripe for Payment & ID Verification...")
        # In a live app, you would use: st.link_button("Pay Now", "https://buy.stripe.com/your_link_id")

# --- TAB 2: EAGLEVIEW EARTHWORKS (THE SERVICE APP) ---
with tab2:
    st.title("🚜 EagleView Earthworks")
    st.write("Logged in as: **Tenant at Pad #204 (Red Fife Rd)**")
    
    st.markdown("""
        <div class="maintenance-card">
            <strong>Current Site Condition:</strong> Dry & Graded (Last Maintained: May 4, 2026)
        </div>
    """, unsafe_allow_html=True)

    with st.form("maintenance_request"):
        st.write("### Request Property Maintenance")
        service_type = st.selectbox("Issue/Service Needed", 
                                   ["Gravel Grading", "Dust Suppression", "Snow Removal", "Equipment Recovery", "Report Fence Damage"])
        
        urgency = st.select_slider("Urgency Level", options=["Routine", "High", "EMERGENCY"])
        
        details = st.text_area("Details (e.g., 'Soft spot near Pad A4 after rain')")
        
        photo = st.file_uploader("Upload Photo (Optional)", type=['jpg', 'png'])
        
        submit_service = st.form_submit_button("SUBMIT TO EAGLEVIEW CREW")

    if submit_service:
        st.success("✅ Request Sent. EagleView Earthworks has been dispatched to your location.")
        # Logic here to send a text to your phone via Twilio or Email
