import os
import sys

import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import (  # noqa: E402
    render_language_selector,
    render_page_styling,
    render_sidebar,
)
from utils.translations import (  # noqa: E402
    AREA_NAME_TRANSLATIONS,
    RESOURCE_NAME_TRANSLATIONS,
    TRANSLATIONS,
)

lang = st.session_state.get(
    "language_selector",
    st.session_state.get("language", "English"),
)
t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
st.session_state["language"] = lang if lang in TRANSLATIONS else "English"
resource_name_translations = RESOURCE_NAME_TRANSLATIONS.get(
    lang,
    RESOURCE_NAME_TRANSLATIONS["English"],
)
area_name_translations = AREA_NAME_TRANSLATIONS.get(
    lang,
    AREA_NAME_TRANSLATIONS["English"],
)

st.set_page_config(page_title=t["hospitals"], layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title(f"🏥 {t['hospitals']}")

df = pd.read_csv("data/hospitals.csv")

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
                    {t["hospital_network"]}
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    {t["hospital_network_subtitle"]}
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
                ">{t["total_active"]}</div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .resource-icon {
        font-size: 18px;
        color: #FF4B4B;
    }

    .nav-icon {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Grid Layout for Cards
cols = st.columns(2)
for i, (_index, row) in enumerate(df.iterrows()):
    col_idx = i % 2
    with cols[col_idx]:
        translated_name = resource_name_translations.get(
            row["Name"],
            row["Name"],
        )
        translated_area = area_name_translations.get(row["Area"], row["Area"])
        nav_link = (
            f"https://www.google.com/maps/dir/?api=1&destination="
            f"{row['Latitude']},{row['Longitude']}"
        )
        st.markdown(
            f"""
            <div class="resource-card">
                <div class="resource-name">🏥 {translated_name}</div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">location_on</span>
                    <b>{t["area_label"]}:</b> {translated_area}
                </div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">call</span>
                    <b>{t["contact"]}:</b> {row["Contact"]}
                </div>
                <a href="{nav_link}" target="_blank" class="nav-btn">
                    <span style="display: flex; align-items: center; gap: 8px;">
                        <span class="material-symbols-rounded" style="
                            font-size: 18px;
                        ">directions</span>
                        {t["navigate_now"]}
                    </span>
                </a>
            </div>
        """,
            unsafe_allow_html=True,
        )

# folium, requests and st_folium are imported at module level

st.divider()
st.markdown(
    f"""
    <div style="border-left: 5px solid #FF4B4B; padding-left: 15px; \
margin: 30px 0 20px 0;">
        <h3 style="color: #F8FAFC; margin: 0;">🔍 {t["search_live_location"]}</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 1])
with col1:
    location_query = st.text_input(
        t["enter_location"], placeholder=t["location_placeholder"]
    )
with col2:
    radius_km = st.slider(t["radius"], 1, 20, 5)

col_a, col_b = st.columns(2)
with col_a:
    if location_query:
        st.link_button(
            f"🌐 {t['google_maps']}",
            f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}",
            width="stretch",
        )
with col_b:
    search_btn = st.button(f"🚀 {t['find_nearby']}", width="stretch")

if "hospital_search_results" not in st.session_state:
    st.session_state.hospital_search_results = None

if "hospital_search_location" not in st.session_state:
    st.session_state.hospital_search_location = ""

if "hospital_search_lat" not in st.session_state:
    st.session_state.hospital_search_lat = None

if "hospital_search_lng" not in st.session_state:
    st.session_state.hospital_search_lng = None


def render_search_results(results, location_query, lat, lng):
    st.success(
        t["found_results_near"].format(count=len(results), location=location_query)
    )

    cols = st.columns(2)
    for i, r in enumerate(results):
        col_idx = i % 2
        with cols[col_idx]:
            translated_result_name = resource_name_translations.get(
                r["Name"],
                r["Name"],
            )
            nav_link = (
                f"https://www.google.com/maps/dir/?api=1&destination="
                f"{r['Latitude']},{r['Longitude']}"
            )
            st.markdown(
                f"""
                <div class="resource-card">
                    <div class="resource-name">🏥 {translated_result_name}</div>
                    <div class="resource-info">
                        <span class="material-symbols-rounded resource-icon">
                            location_on
                        </span>
                        <b>{t["address"]}:</b> {r["Address"]}
                    </div>
                    <div class="resource-info">
                        <span class="material-symbols-rounded resource-icon">
                            directions_run
                        </span>
                        <b>{t["distance"]}:</b> {t["live_tracking_active"]}
                    </div>
                    <a href="{nav_link}" target="_blank" class="nav-btn">
                        <span style="display: flex; align-items: center; gap: 8px;">
                            <span class="material-symbols-rounded nav-icon">
                                directions
                            </span>
                            {t["navigate_now"]}
                        </span>
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )

    m = folium.Map(location=[lat, lng], zoom_start=13, tiles="CartoDB dark_matter")
    folium.Marker(
        [lat, lng],
        popup=t["search_location"],
        icon=folium.Icon(color="red", icon="search"),
    ).add_to(m)
    for r in results:
        if r["Latitude"] and r["Longitude"]:
            folium.Marker(
                [r["Latitude"], r["Longitude"]],
                popup=resource_name_translations.get(r["Name"], r["Name"]),
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(m)
    st_folium(m, height=400, width="stretch")


if search_btn and location_query:
    with st.spinner(t["fetching_live_data"]):
        try:
            # Get coordinates from Nominatim
            nom_url = "https://nominatim.openstreetmap.org/search"
            nom_params: dict[str, str | int] = {
                "q": location_query,
                "format": "json",
                "limit": 1,
            }
            nom_headers = {"User-Agent": "SmartEmergencyAllocator/1.0"}
            nom_resp = requests.get(
                nom_url, params=nom_params, headers=nom_headers, timeout=10
            )
            nom_data = nom_resp.json()

            if nom_data:
                lat = float(nom_data[0]["lat"])
                lng = float(nom_data[0]["lon"])

                overpass_url = "https://overpass-api.de/api/interpreter"
                overpass_query = f"""
                [out:json];
                (
                  node["amenity"="hospital"](around:{radius_km * 1000},{lat},{lng});
                  way["amenity"="hospital"](around:{radius_km * 1000},{lat},{lng});
                );
                out center;
                """

                resp = requests.post(
                    overpass_url,
                    data=overpass_query,
                    headers=nom_headers,
                    timeout=10,
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
                                "Name": tags.get("name", t["unknown"]),
                                "Address": tags.get(
                                    "addr:full",
                                    tags.get(
                                        "addr:street", t["location_details_unavailable"]
                                    ),
                                ),
                                "Latitude": el_lat,
                                "Longitude": el_lng,
                            }
                        )

                    st.session_state.hospital_search_results = results
                    st.session_state.hospital_search_location = location_query
                    st.session_state.hospital_search_lat = lat
                    st.session_state.hospital_search_lng = lng

                    st.success(
                        t["found_results_near"].format(
                            count=len(results),
                            location=location_query,
                        )
                    )

                    # Results Grid with Card Style
                    cols = st.columns(2)
                    for i, r in enumerate(results):
                        col_idx = i % 2
                        with cols[col_idx]:
                            translated_result_name = resource_name_translations.get(
                                r["Name"],
                                r["Name"],
                            )
                            nav_link = (
                                f"https://www.google.com/maps/dir/?api=1&destination="
                                f"{r['Latitude']},{r['Longitude']}"
                            )
                            st.markdown(
                                f"""
                                <div class="resource-card">
                                    <div class="resource-name">
                                        🏥 {translated_result_name}
                                    </div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" \
style="font-size: 18px; color: #FF4B4B;">location_on</span>
                                        <b>{t["address"]}:</b> {r["Address"]}
                                    </div>
                                    <div class="resource-info">
                                        <span class="material-symbols-rounded" \
style="font-size: 18px; color: #FF4B4B;">directions_run</span>
                                        <b>{t["distance"]}:</b>
                                        {t["live_tracking_active"]}
                                    </div>
                                    <a href="{nav_link}" target="_blank" \
class="nav-btn">
                                        <span style="display: flex; \
align-items: center; gap: 8px;">
                                            <span class="material-symbols-rounded" \
style="font-size: 18px;">directions</span>
                                            {t["navigate_now"]}
                                        </span>
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # folium and st_folium are imported at module level

                    m = folium.Map(
                        location=[lat, lng], zoom_start=13, tiles="CartoDB dark_matter"
                    )
                    folium.Marker(
                        [lat, lng],
                        popup=t["search_location"],
                        icon=folium.Icon(color="red", icon="search"),
                    ).add_to(m)
                    for r in results:
                        if r["Latitude"] and r["Longitude"]:
                            folium.Marker(
                                [r["Latitude"], r["Longitude"]],
                                popup=resource_name_translations.get(
                                    r["Name"], r["Name"]
                                ),
                                icon=folium.Icon(color="blue", icon="info-sign"),
                            ).add_to(m)
                    st_folium(m, height=400, width="stretch")
                else:
                    st.warning(t["no_results"])
            else:
                st.error(t["location_not_found"])
        except Exception as e:
            st.error(f"{t['error']}: {str(e)}")

if (
    not search_btn
    and st.session_state.hospital_search_results
    and st.session_state.hospital_search_location
):
    render_search_results(
        st.session_state.hospital_search_results,
        st.session_state.hospital_search_location,
        st.session_state.hospital_search_lat,
        st.session_state.hospital_search_lng,
    )
