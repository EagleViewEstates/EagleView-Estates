import streamlit as st
import os

# --- CONFIG ---
st.set_page_config(page_title="EagleView Estates | Assessment", layout="centered", page_icon="🦅")

# --- PREMIUM BLACK & GOLD THEME ---
st.markdown("""
    <style>
    /* Background and Base Text */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Gold Gradient Title */
    .main-title {
        text-align: center; font-size: 3em; font-weight: 200; letter-spacing: 7px; margin-top: 20px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    .subtext { color: #d4af37 !important; font-size: 1em; text-align: center; margin-bottom: 20px; letter-spacing: 2px; text-transform: uppercase;}
    
    h3 { color: #d4af37 !important; font-weight: 300; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    
    /* Image Styling with Gold Glow */
    .stImage > img {
        border-radius: 4px;
        border: 1px solid #d4af37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    /* Gold Buttons */
    .stButton>button { 
        width: 100%; border-radius: 0px; height: 3.5em; background-color: #d4af37; 
        color: #000000; font-weight: bold; border: none; letter-spacing: 2px; text-transform: uppercase;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ffffff; color: #000000; box-shadow: 0 0 15px #d4af37; }
    
    /* Form Cards */
    .survey-card {
        padding: 25px; background-color: #0f0f0f; border: 1px solid #262626; border-radius: 4px; margin-bottom: 20px;
    }
    
    /* Input Styling */
    input, textarea, select { background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BRANDING ---
st.markdown("<h1 class='main-title'>EAGLEVIEW ESTATES</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Industrial Infrastructure & Heavy Staging</p>", unsafe_allow_html=True)

# --- SITE PHOTO ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Proposed CentrePort Site: Red Fife Road", use_column_width=True)
else:
    st.info("Visualizing: Red Fife Road Site (Photo: site_photo.jpg not found)")

st.markdown("""
<div class='survey-card'>
    <h3>Strategic Site Assessment</h3>
    <p style='color: #888;'>We are securing a prime 1.5 to 5-acre parcel in the Rosser/CentrePort area. 
    Final site engineering is underway for June 1st deployment.</p>
</div>
""", unsafe_allow_html=True)

# --- 5-QUESTION SURVEY ---
with st.form("demand_assessment"):
    
    # 1. NEED
    q1 = st.selectbox("1. Operational Need", 
                     ["Dedicated Monthly Pad (1,000 - 5,000 sqft)", 
                      "Anchor Tenant Parcel (1 - 5 Full Acres)", 
                      "Hourly/Daily Flex-Staging", 
                      "Heavy Equipment Winter Storage"])

    # 2. LOCATION
    q2 = st.select_slider("2. Importance of CentrePort/Rosser Location", 
                         options=["Low Impact", "Convenient", "Strategic", "Essential", "Critical to Operations"])

    # 3. TIMEFRAME
    q3 = st.radio("3. Desired Move-in Timeframe", 
                 ["Immediate (June 1st)", "Summer 2026", "Fall/Winter 2026"])

    # 4. AMENITIES
    q4 = st.multiselect("4. Critical Site Amenities", 
                       ["24/7 Encoded Gate Access", "High-Intensity LED Lighting", 
                        "CCTV Surveillance", "Engineered Compacted Gravel", 
                        "On-Site Grading/Maintenance Support"])

    # 5. PRE-LEASE
    st.markdown("---")
    q5 = st.radio("5. Are you interested in a 'Pre-Lease' agreement to secure current rates and guaranteed space before June 1st?",
                 ["Yes - Send terms for review", 
                  "Maybe - Dependent on final pricing", 
                  "No - Prefer on-demand availability"])

    st.divider()
    
    # LEAD CAPTURE
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Company / Contact Name")
    with col2:
        contact = st.text_input("Email or Phone")

    submit = st.form_submit_button("SUBMIT ASSESSMENT")

if submit:
    if name and contact:
        st.success(f"Form Submitted. EagleView management will contact {name} regarding the {q3} timeframe.")
        if "Yes" in q5:
            st.warning("⚡ High Priority: Pre-Lease interest flagged.")
        st.balloons()
    else:
        st.error("Please provide a name and contact method to record your feedback.")

# --- FOOTER ---
st.markdown("<br><p style='text-align: center; color: #444; font-size: 0.8em; letter-spacing: 3px;'>EAGLEVIEW ESTATES | ROSSER, MB</p>", unsafe_allow_html=True)
