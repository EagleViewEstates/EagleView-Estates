import streamlit as st

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates | Market Assessment", layout="centered", page_icon="🦅")

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
st.markdown("<p class='subtext'>Industrial Site Selection & Demand Assessment</p>", unsafe_allow_html=True)

st.markdown("""
<div class='survey-card'>
    <h3>Strategic Facility Planning</h3>
    <p style='color: #a1a1aa;'>We are deploying a 1.5-acre high-load industrial pad at CentrePort. 
    Your feedback directly influences the final site amenities and security protocols.</p>
</div>
""", unsafe_allow_html=True)

# --- SURVEY FORM ---
with st.form("demand_survey"):
    
    # Question 1: Industry
    q1 = st.selectbox("1. Industry Sector", 
                     ["General Contracting", "Heavy Civil / Earthworks", "Logistics & Transport", "Landscaping / Snow Removal", "Other"])
    
    # Question 2: Use Case
    q2 = st.radio("2. Primary Storage Need", 
                 ["Long-term Dedicated Pad", "Hourly/Daily Staging", "Seasonal Overload"])
    
    # Question 3: Amenities
    q3 = st.multiselect("3. High-Priority Features", 
                       ["24/7 Gate Access", "LED Site Lighting", "High-Definition CCTV", "Snow Removal Service", "On-site Earthworks Crew"])
    
    # Question 4: Location Value
    q4 = st.select_slider("4. Strategic Value of a CentrePort Location", 
                         options=["Low", "Moderate", "Neutral", "High", "Critical"])
    
    # Question 5: Pain Points
    q5 = st.text_area("5. What is the #1 problem with your current storage/parking yard?")

    # --- THE CRITICAL "PRE-LEASE" QUESTION ---
    st.markdown("---")
    st.markdown("### Availability & Reservation")
    q6 = st.radio("6. Would your firm be interested in signing a 'Pre-Lease' agreement to guarantee a dedicated pad for a June 1st move-in?",
                 ["Yes - Contact me immediately with terms", 
                  "Maybe - I need more details on pricing", 
                  "No - We only require on-demand hourly access"])

    st.divider()
    
    # Lead Capture
    st.markdown("### Contact Details")
    name = st.text_input("Contact Name / Company")
    email = st.text_input("Email or Phone Number")
    
    submit_button = st.form_submit_button("SUBMIT MARKET ASSESSMENT")

if submit_button:
    if email and name:
        st.success(f"Thank you, {name}. Your assessment has been recorded.")
        # Logic for pre-lease interest
        if "Yes" in q6:
            st.info("⚡ Priority Flag: Our team will move you to the top of the June 1st queue.")
        st.balloons()
    else:
        st.warning("Please provide your contact details so we can verify your entry.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #333; font-size: 0.8em;'>© 2026 EAGLEVIEW ESTATES | WINNIPEG, MB</p>", unsafe_allow_html=True)
