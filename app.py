import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Assessment", layout="centered", page_icon="🦅")

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3em; font-weight: 200; letter-spacing: 6px; margin-top: 20px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    h3 { color: #3b82f6 !important; }
    .survey-card { padding: 30px; background-color: #0a0a0a; border-radius: 8px; border: 1px solid #1e3a8a; }
    .stButton>button { width: 100%; border-radius: 4px; height: 3.5em; background-color: #3b82f6; color: #ffffff; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='survey-card'>
    <h3>Strategic Facility Planning</h3>
    <p>We are deploying a 1.5-acre high-load industrial pad at CentrePort, with expansion capabilities up to a <b>5-acre parcel</b> for an anchor tenant.</p>
</div>
""", unsafe_allow_html=True)

with st.form("demand_survey"):
    q1 = st.selectbox("1. Industry Sector", ["General Contracting", "Heavy Civil / Earthworks", "Logistics", "Landscaping", "Other"])
    q2 = st.radio("2. Primary Storage Need", ["Dedicated Pad", "Large-Scale Fleet Base (1-5 Acres)", "Hourly/Daily Staging"])
    q6 = st.radio("3. Interested in a 'Pre-Lease' agreement for June 1st?", ["Yes", "Maybe", "No"])
    
    name = st.text_input("Company Name")
    email = st.text_input("Contact Info")
    
    if st.form_submit_button("SUBMIT ASSESSMENT"):
        st.success("Assessment Recorded.")
