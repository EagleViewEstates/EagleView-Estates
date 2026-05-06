import streamlit as st
import os

# --- CONFIG & THEME ---
st.set_page_config(page_title="EagleView Estates | Market Assessment", layout="centered", page_icon="🦅")

# Custom CSS for the Blue/Black Premium Aesthetic & Images
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        text-align: center; font-size: 3em; font-weight: 200; letter-spacing: 6px; margin-top: 20px;
        background: linear-gradient(to right, #ffffff, #3b82f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    h3 { color: #3b82f6 !important; font-weight: 300; }
    .subtext { color: #60a5fa !important; font-size: 1em; text-align: center; margin-bottom: 20px; letter-spacing: 1px; text-transform: uppercase;}
    
    /* Premium Image Styling */
    .stImage > img {
        border-radius: 8px;
        border: 1px solid #1e3a8a;
        box-shadow: 0 5px 25px rgba(59, 130, 246, 0.3);
        margin-bottom: 25px;
    }
    
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

# --- SITE PHOTO ---
if os.path.exists("site_photo.jpg"):
    st.image("site_photo.jpg", caption="Red Fife Road - Secure Industrial Staging Area", use_column_width=True)
else:
    st.info("Photo placeholder: Upload 'site_photo.jpg' to GitHub to display the site image here.")

st.markdown("""
<div class='survey-card'>
    <h3>Strategic Facility Planning</h3>
    <p style='color: #a1a1aa;'>We are deploying a 1.5-acre high-load industrial pad at CentrePort, with immediate expansion capabilities up to a full <b>5-acre parcel</b> for large-scale operations or an anchor tenant. 
    Your feedback directly influences our site configurations, amenities, and security protocols.</p>
</div>
""", unsafe_allow_html=True)

# --- SURVEY FORM ---
with st.form("demand_survey"):
    
    q1 = st.selectbox("1. Industry Sector", 
                     ["General Contracting", "Heavy Civil / Earthworks", "Logistics & Transport", "Landscaping / Snow Removal", "Other"])
    
    q2 = st.radio("2. Primary Storage Need", 
                 ["Long-term Dedicated Pad (1k - 5k sqft)", "Large-Scale Fleet Base (1 to 5 Acres)", "Hourly/Daily Staging", "Seasonal Overload"])
    
    q3 = st.multiselect("3. High-Priority Features", 
                       ["24/7 Gate Access", "LED Site Lighting", "High-Definition CCTV", "Snow Removal Service", "On-site Earthworks Crew"])
    
    q4 = st.select_slider("4. Strategic Value of a CentrePort Location", 
                         options=["Low", "Moderate", "Neutral", "High", "Critical"])
    
    q5 = st.text_area("5. What is the
