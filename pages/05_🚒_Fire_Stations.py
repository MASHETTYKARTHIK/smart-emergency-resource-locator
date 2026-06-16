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

import folium  # noqa: E402
import requests  # noqa: E402
from streamlit_folium import st_folium  # noqa: E402

st.divider()
st.markdown(
    """
    <div style="border-left: 5px solid #FF4B4B; padding-left: 15px; \
margin: 30px 0 20px 0;">
        <h3 style="color: #F8FAFC; margin: 0;">🔍 Search Live Location \
on Google Maps</h3>
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
                  node["amenity"="fire_station"](around:{radius_km*1000},{lat},{lng});
                  way["amenity"="fire_station"](around:{radius_km*1000},{lat},{lng});
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
                            }
                        )

                    st.success(f"Found {len(results)} results near {location_query}")

                    # Results Grid with Card Style
                    cols = st.columns(2)
                    for i, r in enumerate(results):
                        col_idx = i % 2
                        with cols[col_idx]:
                            nav_link = f"https://www.google.com/maps/dir/?api=1&destination={r['Latitude']},{r['Longitude']}"
                            st.markdown(
                                f"""
                                <div class="resource-card">
                                    <div class="resource-name">🚒 {r['Name']}</div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" \
style="font-size: 18px; color: #FF4B4B;">location_on</span>
                                        <b>Address:</b> {r['Address']}
                                    </div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" \
style="font-size: 18px; color: #FF4B4B;">directions_run</span>
                                        <b>Distance:</b> Live Tracking Active
                                    </div>
                                    <a href="{nav_link}" target="_blank" \
class="nav-btn">
                                        <span style="display: flex; \
align-items: center; gap: 8px;">
                                            <span class="material-symbols-rounded" \
style="font-size: 18px;">directions</span>
                                            Navigate Now
                                        </span>
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    import folium  # noqa: E402
                    from streamlit_folium import st_folium  # noqa: E402

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
                                popup=r["Name"],
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
