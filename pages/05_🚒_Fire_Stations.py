import os
import sys

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import (
    render_language_selector,
    render_page_styling,
    render_sidebar,
)

st.set_page_config(page_title="Fire Stations", layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title("🚒 Fire Stations")

df = pd.read_csv("data/firestations.csv")

st.markdown(
    f"""
    <div class="hero-section" style="padding: 25px; margin-bottom: 25px;">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="color: #F8FAFC; font-size: 1.2rem; font-weight: 700;">
                    Fire & Rescue Command
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    Rapid response units for fire emergencies.
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: #FF4B4B; font-size: 2rem; font-weight: 800;">
                    {len(df)}
                </div>
                <div style="
                    color: #64748B;
                    font-size: 0.7rem;
                    font-weight: 700;
                    text-transform: uppercase;
                ">Total Active</div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Grid Layout for Cards
cols = st.columns(2)
for i, (_index, row) in enumerate(df.iterrows()):
    col_idx = i % 2
    with cols[col_idx]:
        nav_link = (
            f"https://www.google.com/maps/dir/?api=1&destination="
            f"{row['Latitude']},{row['Longitude']}"
        )
        st.markdown(
            f"""
            <div class="resource-card">
                <div class="resource-name">🚒 {row["Name"]}</div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">location_on</span>
                    <b>Area:</b> {row["Area"]}
                </div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">call</span>
                    <b>Contact:</b> {row["Contact"]}
                </div>
                <a href="{nav_link}" target="_blank" class="nav-btn">
                    <span style="display: flex; align-items: center; gap: 8px;">
                        <span class="material-symbols-rounded" style="
                            font-size: 18px;
                        ">directions</span>
                        Navigate Now
                    </span>
                </a>
            </div>
        """,
            unsafe_allow_html=True,
        )

st.info("In case of fire emergency, call 101 immediately.")

import requests
import folium
from streamlit_folium import st_folium

st.divider()
st.markdown(
    """
    <div style="border-left: 5px solid #FF4B4B; padding-left: 15px; margin: 30px 0 20px 0;">
        <h3 style="color: #F8FAFC; margin: 0;">🔍 Search Live Location on Google Maps</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

location_query = st.text_input("Enter location:", placeholder="e.g., Fire Station Hyderabad")
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
              node["amenity"="fire_station"](around:5000, 17.3850, 78.4867);
              way["amenity"="fire_station"](around:5000, 17.3850, 78.4867);
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
                        addr = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Location details unavailable'))
                        results.append({'Name': name, 'Latitude': lat, 'Longitude': lon, 'Address': addr})
                    
                    df_res = pd.DataFrame(results)
                    
                    # Results Grid
                    cols = st.columns(2)
                    for i, (_, row) in enumerate(df_res.iterrows()):
                        col_idx = i % 2
                        with cols[col_idx]:
                            nav_link = f"https://www.google.com/maps/dir/?api=1&destination={row['Latitude']},{row['Longitude']}"
                            st.markdown(
                                f"""
                                <div class="resource-card">
                                    <div class="resource-name">🚒 {row["Name"]}</div>
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
                        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)
                    st_folium(m, width="100%", height=400)
            except Exception as e:
                st.error(f"Error fetching data: {e}")
