import streamlit as st

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates | Demand Survey", layout="centered", page_icon="🦅")

# Custom CSS for the Blue/Black Premium Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3em; font-weight: 200; letter-spacing: 6px; margin-top: 20px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    h3 { color: #3b82f6 !important; font-weight: 300; }
    .subtext { color: #60a5fa !important; font-size: 1em; text-align: center; margin-bottom: 30px; letter-spacing: 1px; text-transform: uppercase;}
    
    /* Survey Card Styling */
    .survey-card {
        padding: 30px; background-color: #0a0a0a; border-radius: 8px; border: 1px solid #1e3a8a; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); margin-bottom: 25px;
    }
    
    .stButton>button { 
        width: 100%; border-radius: 4px; height: 3.5em; background-color: #3b82f6; 
        color: #ffffff; font-weight: bold; border: none; letter-spacing: 2px; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #ffffff; color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Storage & Infrastructure Assessment</p>", unsafe_allow_html=True)

st.markdown("""
<div class='survey-card'>
    <h3>Market Demand Survey</h3>
    <p style='color: #a1a1aa;'>We are finalizing a premium 1.5-acre secure storage facility at CentrePort Canada. 
    Help us tailor our services to your fleet's needs.</p>
</div>
""", unsafe_allow_html=True)

# --- SURVEY QUESTIONS ---
with st.form("demand_survey"):
    
    # Question 1
    q1 = st.selectbox("1. What best describes your operation?", 
                     ["General Contracting", "Heavy Civil / Earthworks", "Logistics & Transport", "Landscaping / Snow Removal", "Other"])
    
    # Question 2
    q2 = st.radio("2. What is your primary storage requirement?", 
                 ["Dedicated Monthly Pad", "Daily/Hourly Staging & Parking", "Emergency Overload Space"])
    
    # Question 3
    q3 = st.multiselect("3. Which features are 'Must-Haves' for your fleet?", 
                       ["24/7 Secure Gate Access", "High-Load Compacted Gravel", "Site Lighting", "Security Perimeter", "Snow Clearing Included"])
    
    # Question 4
    q4 = st.select_slider("4. How critical is a CentrePort location to your efficiency?", 
                         options=["Not Critical", "Somewhat", "Neutral", "Important", "Critical"])
    
    # Question 5
    q5 = st.text_input("5. What is the biggest frustration with your current storage setup?")

    st.divider()
    
    # Lead Capture
    st.markdown("### Join the June 1st Priority List")
    email = st.text_input("Email Address / Phone Number")
    
    submit_button = st.form_submit_button("SUBMIT ASSESSMENT")

if submit_button:
    if email:
        st.success("Thank you. Your feedback is being integrated into the EagleView site plan.")
        st.balloons()
        # In a real scenario, you'd save these to a database or Google Sheet.
    else:
        st.warning("Please provide a contact method to join the priority list.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #333; font-size: 0.8em;'>© 2026 EAGLEVIEW ESTATES | WINNIPEG, MB</p>", unsafe_allow_html=True)
