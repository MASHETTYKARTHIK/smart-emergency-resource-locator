import os
import sys
import traceback
from html import escape
from typing import Any

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

NOMINATIM_TIMEOUT_SECONDS = 10
OVERPASS_TIMEOUT_SECONDS = 30
OVERPASS_SERVER_TIMEOUT_SECONDS = 25


def parse_json_response(response: requests.Response, service_name: str) -> Any:
    """Return JSON only after confirming the upstream response is usable."""
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise RuntimeError(
            f"{service_name} request failed with status {response.status_code}"
        ) from exc

    content_type = response.headers.get("content-type", "").lower()
    if "json" not in content_type:
        raise RuntimeError(f"{service_name} returned a non-JSON response")

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(f"{service_name} returned invalid JSON") from exc


st.set_page_config(page_title=t["resource_map"], layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-title">🗺️ {t["emergency_resource_map"]}</div>
        <div class="hero-subtitle">
            {t["map_subtitle"]}
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

# Filter Panel
with st.container():
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(
            f"""
            <div style="
                padding-top: 10px;
                color: #94A3B8;
                font-weight: 600;
                font-size: 0.8rem;
            ">
                {t["filter_view"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        resource = st.selectbox(
            t["select_asset_type"],
            [
                "Hospitals",
                "Blood Banks",
                "Police Stations",
                "Fire Stations",
            ],
            format_func=lambda option: {
                "Hospitals": t["hospitals"],
                "Blood Banks": t["blood_banks"],
                "Police Stations": t["police_stations"],
                "Fire Stations": t["fire_stations"],
            }[option],
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

st.markdown(
    """
    <style>
    iframe[title="streamlit_folium.st_folium"] {
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

m = folium.Map(
    location=[17.44, 78.38],
    zoom_start=11,
    tiles=(
        "cartodbpositron"
        if st.session_state.get("theme") == "light"
        else "CartoDB dark_matter"
    ),
)

for _, row in df.iterrows():
    translated_name = resource_name_translations.get(
        row["Name"],
        row["Name"],
    )
    translated_area = area_name_translations.get(row["Area"], row["Area"])
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=f"<b>{translated_name}</b><br>{row['Contact']}<br>{translated_area}",
        tooltip=translated_name,
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(m)

st_folium(m, width="stretch", height=600)

st.divider()

st.markdown(
    f"""
    <div
        style="
            border-left: 5px solid #FF4B4B;
            padding-left: 15px;
            margin: 30px 0 20px 0;
        "
    >
        <h3 style="color: #F8FAFC; margin: 0;">
            🔍 {t["search_live_location"]}
        </h3>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 1])

with col1:
    location_query = st.text_input(
        t["enter_location"],
        placeholder=t["location_placeholder"],
    )

with col2:
    radius_km = st.slider(t["radius"], 1, 20, 5)

col_a, col_b = st.columns(2)

with col_a:
    if location_query:
        st.link_button(
            f"🌐 {t['google_maps']}",
            (f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"),
            width="stretch",
        )

with col_b:
    search_btn = st.button(
        f"🚀 {t['find_nearby']}",
        width="stretch",
    )

# Session state setup
if "resource_map_search_results" not in st.session_state:
    st.session_state.resource_map_search_results = None

if "resource_map_search_location" not in st.session_state:
    st.session_state.resource_map_search_location = ""

if "resource_map_search_lat" not in st.session_state:
    st.session_state.resource_map_search_lat = None

if "resource_map_search_lng" not in st.session_state:
    st.session_state.resource_map_search_lng = None


def render_resource_map_results(results, location_name, lat, lng):
    st.success(
        t["found_results_near"].format(count=len(results), location=location_name)
    )

    emoji_map = {
        "hospital": "🏥",
        "fire_station": "🚒",
        "police": "👮",
    }
    amenity_labels = {
        "hospital": t["hospital"],
        "fire_station": t["fire_station"],
        "police": t["police_station"],
    }

    cols = st.columns(2)

    for i, r in enumerate(results):
        col_idx = i % 2

        with cols[col_idx]:
            emoji = emoji_map.get(r["Amenity"], "📍")
            translated_result_name = resource_name_translations.get(
                r["Name"],
                r["Name"],
            )
            safe_result_name = escape(str(translated_result_name))
            safe_address = escape(str(r["Address"]))

            nav_link = (
                "https://www.google.com/maps/dir/?api=1&destination="
                f"{r['Latitude']},{r['Longitude']}"
            )

            result_card_html = f"""
                <div class="resource-card">
                    <div class="resource-name">{emoji} {safe_result_name}</div>
                    <div class="resource-info">
                        <span class="material-symbols-rounded resource-icon">
                            location_on
                        </span>
                        <b>{t["address"]}:</b> {safe_address}
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
                """

            st.markdown(
                result_card_html,
                unsafe_allow_html=True,
            )

    live_map = folium.Map(
        location=[lat, lng],
        zoom_start=13,
        tiles="CartoDB dark_matter",
    )

    folium.Marker(
        [lat, lng],
        popup=t["search_location"],
        icon=folium.Icon(color="red", icon="search"),
    ).add_to(live_map)

    for r in results:
        if r["Latitude"] and r["Longitude"]:
            folium.Marker(
                [r["Latitude"], r["Longitude"]],
                popup=f"{resource_name_translations.get(r['Name'], r['Name'])}"
                f" ({amenity_labels.get(r['Amenity'], r['Amenity'])})",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(live_map)

    st_folium(
        live_map,
        height=400,
        width="stretch",
    )


if search_btn and location_query:
    st.session_state.resource_map_search_results = None
    st.session_state.resource_map_search_location = ""
    st.session_state.resource_map_search_lat = None
    st.session_state.resource_map_search_lng = None

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
                nom_url,
                params=nom_params,
                headers=nom_headers,
                timeout=NOMINATIM_TIMEOUT_SECONDS,
            )
            nom_data = parse_json_response(nom_resp, "Nominatim")

            if nom_data:
                lat = float(nom_data[0]["lat"])
                lng = float(nom_data[0]["lon"])

                overpass_url = "https://overpass-api.de/api/interpreter"

                amenities = "hospital|fire_station|police"

                around = f"around:{radius_km * 1000},{lat},{lng}"

                overpass_query = f"""
                [out:json][timeout:{OVERPASS_SERVER_TIMEOUT_SECONDS}];
                (
                  node["amenity"~"{amenities}"]({around});
                  way["amenity"~"{amenities}"]({around});
                );
                out center;
                """

                resp = requests.post(
                    overpass_url,
                    data={"data": overpass_query},
                    headers=nom_headers,
                    timeout=OVERPASS_TIMEOUT_SECONDS,
                )
                data = parse_json_response(resp, "Overpass")

                elements = data.get("elements", [])

                if elements:
                    results = []

                    for el in elements[:10]:
                        tags = el.get("tags", {})

                        el_lat = el.get("lat") or el.get("center", {}).get("lat")

                        el_lng = el.get("lon") or el.get("center", {}).get("lon")

                        results.append(
                            {
                                "Name": tags.get(
                                    "name",
                                    t["unknown"],
                                ),
                                "Address": tags.get(
                                    "addr:full",
                                    tags.get(
                                        "addr:street",
                                        t["location_details_unavailable"],
                                    ),
                                ),
                                "Latitude": el_lat,
                                "Longitude": el_lng,
                                "Amenity": tags.get(
                                    "amenity",
                                    t["unknown"],
                                ),
                            }
                        )

                    st.session_state.resource_map_search_results = results
                    st.session_state.resource_map_search_location = location_query
                    st.session_state.resource_map_search_lat = lat
                    st.session_state.resource_map_search_lng = lng

                    render_resource_map_results(
                        results,
                        location_query,
                        lat,
                        lng,
                    )

                else:
                    st.warning(t["no_results"])

            else:
                st.error(t["location_not_found"])

        except requests.Timeout:
            st.error(
                f"{t['error']}: Live data request timed out. "
                "Please try again or reduce the radius."
            )
        except Exception as e:
            print(f"[RESOURCE_MAP_DEBUG] Full traceback={traceback.format_exc()!r}")
            st.error(f"{t['error']}: {str(e)}")

if (
    not search_btn
    and st.session_state.resource_map_search_results
    and st.session_state.resource_map_search_location
):
    render_resource_map_results(
        st.session_state.resource_map_search_results,
        st.session_state.resource_map_search_location,
        st.session_state.resource_map_search_lat,
        st.session_state.resource_map_search_lng,
    )
