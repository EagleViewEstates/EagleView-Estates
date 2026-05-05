import streamlit as st
import datetime
import os

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates", layout="centered", page_icon="🦅")

# Custom CSS for Deep Black, Electric Blue, and Crisp White
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; 
        font-size: 3.5em; 
        font-weight: 200; 
        letter-spacing: 8px; 
        margin-top: 20px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h1, h2, h3 { color: #3b82f6 !important; font-family: 'Helvetica Neue', sans-serif; }
    h4, p, span, li { color: #ffffff !important; }
    .subtext { color: #60a5fa !important; font-size: 1.1em; text-align: center; margin-bottom: 20px; letter-spacing: 2px; text-transform: uppercase;}
    
    /* Premium Styling for Media */
    .stVideo, .stImage {
        border-radius: 8px;
        border: 1px solid #1e3a8a;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.3);
        margin-bottom: 20px;
    }

    .stButton>button { 
        width: 100%; border-radius: 4px; height: 3.5em; background-color: #000000; 
        color: #3b82f6; font-weight: bold; border: 1px solid #1e40af; letter-spacing: 2px; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #3b82f6; color: #ffffff; border: 1px solid #ffffff; }
    
    .price-box { 
        padding: 30px; background-color: #0a0a0a; border-radius: 4px; border: 1px solid #1e3a8a; 
        text-align: center; box-shadow: 0 5px 20px -5px rgba(30, 58, 138, 0.4); margin-top: 20px;
    }
    .promo-text { color: #60a5fa !important; font-weight: bold; font-size: 0.9em; text-transform: uppercase;}
    
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #1e3a8a; }
    .stTabs [data-baseweb="tab"] { color: #60a5fa; padding: 15px 25px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>EAGLEVIEW</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1.2em; font-weight: 400; letter-spacing: 6px; color: #ffffff !important; margin-top: -20px;'>ESTATES</h3>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Storage | Infrastructure | Excellence</p>", unsafe_allow_html=True)

# --- MEDIA SECTION (VIDEO & PHOTO) ---
col_vid, col_img = st.columns(2)

with col_vid:
    if os.path.exists("eagleview_promo.mp4"):
        st.video("eagleview_promo.mp4")
    else:
        st.info("Video 'eagleview_promo.mp4' not found on GitHub.")

with col_img:
    if os.path.exists("site_photo.jpg"):
        st.image("site_photo.jpg", caption="Red Fife Rd Site")
    else:
        st.info("Photo 'site_photo.jpg' not found on GitHub.")

st.divider()

# --- APP NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["RESERVE MONTHLY", "HOURLY QUICK-PARK", "MAINTENANCE & REFERRALS"])

# --- TAB 1: MONTHLY LEASE ---
with tab1:
    st.write("### Secure Your Pad")
    col_a, col_b = st.columns(2)
    with col_a:
        pad_choice = st.selectbox("Select Size", ["Trade Pad (1k sqft)", "Contractor Hub (2.5k sqft)", "Heavy Civil Fleet (5k sqft)"])
    with col_b:
        lease_term = st.slider("Lease Term (Months)", 1, 12, 1)

    rates = {"Trade Pad (1k sqft)": 1500, "Contractor Hub (2.5k sqft)": 2500, "Heavy Civil Fleet (5k sqft)": 3750}
    base_price = rates[pad_choice]
    
    total_contract_value = base_price * lease_term
    savings = 0
    if lease_term >= 6:
        savings = base_price
        st.markdown(f"<p class='promo-text'>✓ BLUE-TIER LOYALTY: 1st Month Free Applied</p>", unsafe_allow_html=True)

    final_due = total_contract_value - savings

    st.markdown(f"""
        <div class="price-box">
            <p style='color:#60a5fa; text-transform: uppercase; font-size: 0.75em; letter-spacing: 2px;'>Projected Total</p>
            <h2 style='color:#ffffff !important; font-size: 3.5em; margin: 10px 0; font-weight: 200;'>${final_due:,.2f}</h2>
            <p style='color:#60a5fa;'>Security Deposit Due: <span style='color:#ffffff; font-weight:bold;'>${base_price if lease_term < 6 else 0:,.2f}</span></p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("AUTHORIZE LEASE & GATE ACCESS"):
        st.toast("Connecting to Secure Blue-Shield Servers...", icon="🔵")

# --- TAB 2: HOURLY QUICK-PARK ---
with tab2:
    st.write("### Rapid Staging")
    hr_col1, hr_col2 = st.columns(2)
    with hr_col1:
        hours = st.number_input("Duration (Hours)", 1, 24, 2)
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
    
    if st.button("GENERATE ONE-TIME ACCESS PIN"):
        st.code(f"GATE PIN: #EV-{datetime.datetime.now().strftime('%M%S')}")

# --- TAB 3: MAINTENANCE & REFERRALS ---
with tab3:
    st.write("### EagleView Earthworks")
    with st.expander("Request Property Maintenance"):
        st.selectbox("Requested Service", ["Precision Grading", "Winter Maintenance", "Dust Suppression"])
        st.button("DISPATCH MAINTENANCE CREW")
    
    st.divider()
    st.write("### Partnership Network")
    st.write("Refer an industry partner for a $500 premium credit.")
    ref_code = st.text_input("Enter Referral Code")

st.markdown("<br><p style='text-align: center; color: #333; font-size: 0.8em;'>© 2026 EAGLEVIEW ESTATES & EARTHWORKS | ROSSER, MB</p>", unsafe_allow_html=True)
