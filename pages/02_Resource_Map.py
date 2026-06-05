import sys
import os
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import render_sidebar, render_language_selector, render_page_styling

st.set_page_config(page_title="Resource Map", layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title("🗺️ Emergency Resource Map")

st.markdown("""
    <div class="hero-section" style="padding: 25px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="background: rgba(255, 75, 75, 0.1); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255, 75, 75, 0.2);">
                <span class="material-symbols-rounded" style="color: #FF4B4B; font-size: 30px;">map</span>
            </div>
            <div>
                <div style="color: #F8FAFC; font-size: 1.5rem; font-weight: 700;">Spatial Intelligence</div>
                <div style="color: #94A3B8; font-size: 0.9rem;">Interactive visualization of emergency assets across Hyderabad.</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Filter Panel
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown('<div style="padding-top: 10px; color: #94A3B8; font-weight: 600; font-size: 0.8rem;">FILTER VIEW</div>', unsafe_allow_html=True)
        resource = st.selectbox(
            "Select Asset Type",
            ["Hospitals", "Blood Banks", "Police Stations", "Fire Stations"],
            label_visibility="collapsed"
        )

if resource == "Hospitals":
    df = pd.read_csv("data/hospitals.csv")
    color = "red"
elif resource == "Blood Banks":
    df = pd.read_csv("data/bloodbanks.csv")
    color = "darkred"
elif resource == "Police Stations":
    df = pd.read_csv("data/policestations.csv")
    color = "blue"
else:
    df = pd.read_csv("data/firestations.csv")
    color = "orange"

# Map Container
st.markdown('<div style="margin-top: 20px; border-radius: 24px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.4);">', unsafe_allow_html=True)
m = folium.Map(location=[17.44, 78.38], zoom_start=11, tiles="cartodbpositron" if st.session_state.get("theme") == "light" else "CartoDB dark_matter")

for _, row in df.iterrows():
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=f"<b>{row['Name']}</b><br>{row['Contact']}<br>{row['Area']}",
        tooltip=row["Name"],
        icon=folium.Icon(color=color, icon='info-sign'),
    ).add_to(m)

st_folium(m, width="100%", height=600)
st.markdown('</div>', unsafe_allow_html=True)
