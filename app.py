import streamlit as st
import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates", layout="centered", page_icon="🦅")

# Custom CSS for the Blue/Black Premium Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3.5em; font-weight: 200; letter-spacing: 8px; margin-top: 20px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    h1, h2, h3 { color: #3b82f6 !important; }
    .subtext { color: #60a5fa !important; font-size: 1.1em; text-align: center; margin-bottom: 40px; letter-spacing: 2px; text-transform: uppercase;}
    
    .stButton>button { 
        width: 100%; border-radius: 4px; height: 3.5em; background-color: #000000; 
        color: #3b82f6; font-weight: bold; border: 1px solid #1e40af; letter-spacing: 2px; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #3b82f6; color: #ffffff; border: 1px solid #ffffff; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    
    .price-box { 
        padding: 30px; background-color: #0a0a0a; border-radius: 4px; border: 1px solid #1e3a8a; 
        text-align: center; box-shadow: 0 5px 20px -5px rgba(30, 58, 138, 0.4); margin-top: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #1e3a8a; }
    .stTabs [data-baseweb="tab"] { color: #60a5fa; padding: 15px 25px; }
    .stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>EAGLEVIEW</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Storage | Rosser, MB</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["RESERVE MONTHLY", "HOURLY QUICK-PARK", "MAINTENANCE"])

# --- TAB 1: MONTHLY ---
with tab1:
    st.write("### Monthly Staging")
    pad_choice = st.selectbox("Pad Size", ["Trade Pad (1k sqft)", "Contractor Hub (2.5k sqft)", "Heavy Civil Fleet (5k sqft)"])
    lease_term = st.slider("Lease Duration (Months)", 1, 12, 1)
    
    rates = {"Trade Pad (1k sqft)": 1500, "Contractor Hub (2.5k sqft)": 2500, "Heavy Civil Fleet (5k sqft)": 3750}
    total = (rates[pad_choice] * lease_term) - (rates[pad_choice] if lease_term >= 6 else 0)
    
    st.markdown(f"<div class='price-box'><p style='color:#60a5fa;'>Total Contract Value</p><h2>${total:,.2f}</h2></div>", unsafe_allow_html=True)
    if st.button("PROCESS MONTHLY LEASE"):
        st.info("Redirecting to Secure Payment Portal...")

# --- TAB 2: HOURLY (PAY TO UNLOCK) ---
with tab2:
    st.write("### Hourly Rapid-Park")
    st.caption("Secure payment required for gate code generation.")
    
    col_h, col_v = st.columns(2)
    with col_h:
        hours = st.number_input("Duration (Hours)", 1, 24, 2)
    with col_v:
        vehicle = st.radio("Asset Class", ["Service Van", "Semi-Truck", "Heavy Machinery"])
    
    hr_rates = {"Service Van": 15, "Semi-Truck": 25, "Heavy Machinery": 40}
    due_now = hr_rates[vehicle] * hours
    
    st.markdown(f"<div class='price-box'><p style='color:#60a5fa;'>Amount Due Now</p><h3>${due_now:,.2f}</h3></div>", unsafe_allow_html=True)
    
    if 'payment_complete' not in st.session_state:
        st.session_state.payment_complete = False

    if not st.session_state.payment_complete:
        if st.button(f"PAY ${due_now:,.2f} & UNLOCK GATE"):
            # Simulation of payment success
            st.session_state.payment_complete = True
            st.rerun()
    else:
        st.success("✅ Payment Confirmed")
        st.markdown(f"""
            <div style="border: 2px dashed #3b82f6; padding: 20px; text-align: center; border-radius: 10px; background-color: #0a0a0a;">
                <p style="margin:0; font-size: 0.8em; color: #60a5fa;">YOUR TEMPORARY ACCESS PIN</p>
                <h1 style="margin:0; color: #ffffff !important; letter-spacing: 5px;">#EV-{datetime.datetime.now().strftime('%M%S')}</h1>
                <p style="margin-top:10px; font-size: 0.7em;">Valid for {hours} hours.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("New Booking"):
            st.session_state.payment_complete = False
            st.rerun()

# --- TAB 3: MAINTENANCE ---
with tab3:
    st.write("### EagleView Earthworks")
    st.button("DISPATCH GRADER")
    st.divider()
    st.write("Refer a partner for a $500 credit.")
