import os
import sys

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import (
    render_language_selector,
    render_page_styling,
    render_sidebar,
)

st.set_page_config(page_title="Resource Map", layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title("🗺️ Emergency Resource Map")

st.markdown(
    """
    <div class="hero-section" style="padding: 25px; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="
                background: rgba(255, 75, 75, 0.1);
                width: 50px;
                height: 50px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid rgba(255, 75, 75, 0.2);
            ">
                <span class="material-symbols-rounded" 
                      style="color: #FF4B4B; font-size: 30px;">
                    map
                </span>
            </div>
            <div>
                <div style="color: #F8FAFC; font-size: 1.5rem; font-weight: 700;">
                    Spatial Intelligence
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    Interactive visualization of emergency assets across Hyderabad.
                </div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Filter Panel
with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            """
            <div style="
                padding-top: 10px;
                color: #94A3B8;
                font-weight: 600;
                font-size: 0.8rem;
            ">FILTER VIEW</div>
            """,
            unsafe_allow_html=True,
        )
        resource = st.selectbox(
            "Select Asset Type",
            ["Hospitals", "Blood Banks", "Police Stations", "Fire Stations"],
            label_visibility="collapsed",
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
st.markdown(
    """
    <div style="
        margin-top: 20px;
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    ">
    """,
    unsafe_allow_html=True,
)
m = folium.Map(
    location=[17.44, 78.38],
    zoom_start=11,
    tiles="cartodbpositron"
    if st.session_state.get("theme") == "light"
    else "CartoDB dark_matter",
)

for _, row in df.iterrows():
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=f"<b>{row['Name']}</b><br>{row['Contact']}<br>{row['Area']}",
        tooltip=row["Name"],
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(m)

st_folium(m, width="100%", height=600)
st.markdown("</div>", unsafe_allow_html=True)

import requests

st.divider()
st.markdown(
    """
    <div style="border-left: 5px solid #FF4B4B; padding-left: 15px; margin: 30px 0 20px 0;">
        <h3 style="color: #F8FAFC; margin: 0;">🔍 Search Live Location on Google Maps</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

location_query = st.text_input("Enter location:", placeholder="e.g., Emergency Service Hyderabad")
maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"
if location_query:
    st.link_button("🌐 Open in Google Maps", url=maps_url)

if st.button("🚀 Find Nearby on Map"):
    if not location_query:
        st.error("Please enter a location first!")
    else:
        with st.spinner("Fetching data from OpenStreetMap..."):
            overpass_url = "https://overpass-api.de/api/interpreter"
            query = """
            [out:json];
            (
              node["amenity"~"hospital|fire_station|police"](around:5000, 17.3850, 78.4867);
              way["amenity"~"hospital|fire_station|police"](around:5000, 17.3850, 78.4867);
            );
            out;
            """
            try:
                headers = {
                    "User-Agent": "SmartEmergencyAllocator/1.0 (contact@example.com)"
                }
                response = requests.get(overpass_url, params={'data': query}, headers=headers)
                response.raise_for_status()
                data = response.json()
                if not data['elements']:
                    st.warning("No results found nearby.")
                else:
                    results = []
                    for element in data['elements']:
                        name = element.get('tags', {}).get('name', 'Unknown')
                        lat = element.get('lat', 0)
                        lon = element.get('lon', 0)
                        amenity = element.get('tags', {}).get('amenity', 'Unknown')
                        addr = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Location details unavailable'))
                        results.append({
                            'Name': name, 
                            'Latitude': lat, 
                            'Longitude': lon, 
                            'Amenity': amenity,
                            'Address': addr
                        })
                    
                    df_res = pd.DataFrame(results)
                    
                    # Emoji Mapping
                    emoji_map = {
                        "hospital": "🏥",
                        "fire_station": "🚒",
                        "police": "👮"
                    }
                    
                    # Results Grid
                    cols = st.columns(2)
                    for i, (_, row) in enumerate(df_res.iterrows()):
                        col_idx = i % 2
                        with cols[col_idx]:
                            emoji = emoji_map.get(row["Amenity"], "📍")
                            nav_link = f"https://www.google.com/maps/dir/?api=1&destination={row['Latitude']},{row['Longitude']}"
                            st.markdown(
                                f"""
                                <div class="resource-card">
                                    <div class="resource-name">{emoji} {row["Name"]}</div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" style="font-size: 18px; color: #FF4B4B;">location_on</span>
                                        <b>Address:</b> {row["Address"]}
                                    </div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" style="font-size: 18px; color: #FF4B4B;">directions_run</span>
                                        <b>Distance:</b> Live Tracking Active
                                    </div>
                                    <a href="{nav_link}" target="_blank" class="nav-btn">
                                        <span style="display: flex; align-items: center; gap: 8px;">
                                            <span class="material-symbols-rounded" style="font-size: 18px;">directions</span>
                                            Navigate Now
                                        </span>
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    m = folium.Map(location=[17.3850, 78.4867], zoom_start=13, tiles="CartoDB dark_matter")
                    for _, row in df_res.iterrows():
                        folium.Marker([row['Latitude'], row['Longitude']], popup=f"{row['Name']} ({row['Amenity']})").add_to(m)
                    st_folium(m, width="100%", height=400)
            except Exception as e:
                st.error(f"Error fetching data: {e}")
