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

col1, col2 = st.columns([3, 1])
with col1:
    location_query = st.text_input(
        "Enter location:", placeholder="e.g. Hyderabad, Gachibowli"
    )
with col2:
    radius_km = st.slider("Radius (km)", 1, 20, 5)

col_a, col_b = st.columns(2)
with col_a:
    if location_query:
        st.link_button(
            "🌐 Open in Google Maps",
            f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}",
            use_container_width=True,
        )
with col_b:
    search_btn = st.button("🚀 Find Nearby on Map", use_container_width=True)

if search_btn and location_query:
    with st.spinner("Fetching live data..."):
        try:
            import requests

            # Get coordinates from Nominatim
            nom_url = "https://nominatim.openstreetmap.org/search"
            nom_params = {"q": location_query, "format": "json", "limit": 1}
            nom_headers = {"User-Agent": "SmartEmergencyAllocator/1.0"}
            nom_resp = requests.get(nom_url, params=nom_params, headers=nom_headers)
            nom_data = nom_resp.json()

            if nom_data:
                lat = float(nom_data[0]["lat"])
                lng = float(nom_data[0]["lon"])

                overpass_url = "https://overpass-api.de/api/interpreter"
                overpass_query = f"""
                [out:json];
                (
                  node["amenity"~"hospital|fire_station|police"](around:{radius_km * 1000},{lat},{lng});
                  way["amenity"~"hospital|fire_station|police"](around:{radius_km * 1000},{lat},{lng});
                );
                out center;
                """

                resp = requests.post(
                    overpass_url, data=overpass_query, headers=nom_headers
                )
                data = resp.json()
                elements = data.get("elements", [])

                if elements:
                    results = []
                    for el in elements[:10]:
                        tags = el.get("tags", {})
                        el_lat = el.get("lat") or el.get("center", {}).get("lat")
                        el_lng = el.get("lon") or el.get("center", {}).get("lon")
                        results.append(
                            {
                                "Name": tags.get("name", "Unknown"),
                                "Address": tags.get(
                                    "addr:full",
                                    tags.get(
                                        "addr:street", "Location details unavailable"
                                    ),
                                ),
                                "Latitude": el_lat,
                                "Longitude": el_lng,
                                "Amenity": tags.get("amenity", "Unknown"),
                            }
                        )

                    st.success(f"Found {len(results)} results near {location_query}")

                    # Emoji Mapping
                    emoji_map = {"hospital": "🏥", "fire_station": "🚒", "police": "👮"}

                    # Results Grid with Card Style
                    cols = st.columns(2)
                    for i, r in enumerate(results):
                        col_idx = i % 2
                        with cols[col_idx]:
                            emoji = emoji_map.get(r["Amenity"], "📍")
                            nav_link = f"https://www.google.com/maps/dir/?api=1&destination={r['Latitude']},{r['Longitude']}"
                            st.markdown(
                                f"""
                                <div class="resource-card">
                                    <div class="resource-name">{emoji} {r["Name"]}</div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" style="font-size: 18px; color: #FF4B4B;">location_on</span>
                                        <b>Address:</b> {r["Address"]}
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

                    import folium
                    from streamlit_folium import st_folium

                    m = folium.Map(
                        location=[lat, lng], zoom_start=13, tiles="CartoDB dark_matter"
                    )
                    folium.Marker(
                        [lat, lng],
                        popup="Search Location",
                        icon=folium.Icon(color="red", icon="search"),
                    ).add_to(m)
                    for r in results:
                        if r["Latitude"] and r["Longitude"]:
                            folium.Marker(
                                [r["Latitude"], r["Longitude"]],
                                popup=f"{r['Name']} ({r['Amenity']})",
                                icon=folium.Icon(color="blue", icon="info-sign"),
                            ).add_to(m)
                    st_folium(m, height=400, use_container_width=True)
                else:
                    st.warning(
                        "No results found. Try a different location or increase radius."
                    )
            else:
                st.error("Location not found. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
