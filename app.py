import math
import os
import sys

import pandas as pd
import streamlit as st

# Add src to path for imports
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

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


# --- DISTANCE CALCULATIONS ---
def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on the earth."""
    R = 6371  # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Predefined coordinates for areas
AREA_COORDS = {
    "Gachibowli": (17.4401, 78.3489),
    "HITEC City": (17.4500, 78.3810),
    "Madhapur": (17.4483, 78.3915),
    "Kukatpally": (17.4948, 78.3996),
    "Jubilee Hills": (17.4320, 78.4070),
    "Banjara Hills": (17.4120, 78.4340),
    "Ameerpet": (17.4374, 78.4482),
    "Panjagutta": (17.4260, 78.4510),
    "Begumpet": (17.4440, 78.4660),
    "Secunderabad": (17.4399, 78.4983),
    "Mehdipatnam": (17.3910, 78.4300),
    "LB Nagar": (17.3450, 78.5520),
    "Dilsukhnagar": (17.3650, 78.5200),
    "Uppal": (17.4040, 78.5550),
    "Charminar": (17.3616, 78.4747),
}

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

# Page Configuration
st.set_page_config(
    page_title=t["app_page_title"],
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

# --- MAIN CONTENT ---
st.markdown(
    f"""
    <div class="hero-section">
        <div class="hero-title">🚑 {t["resources"]}</div>
        <div class="hero-subtitle">
            {t["hero_subtitle"]}
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(f"### 🗺️ {t['google_maps']}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.link_button(
        f"🏥 {t['hospitals_near_me']}",
        "https://www.google.com/maps/search/hospitals+near+me",
        width="stretch",
    )
with col2:
    st.link_button(
        f"💉 {t['blood_banks_near_me']}",
        "https://www.google.com/maps/search/blood+banks+near+me",
        width="stretch",
    )
with col3:
    st.link_button(
        f"🚒 {t['fire_stations_near_me']}",
        "https://www.google.com/maps/search/fire+stations+near+me",
        width="stretch",
    )
with col4:
    st.link_button(
        f"👮 {t['police_stations_near_me']}",
        "https://www.google.com/maps/search/police+stations+near+me",
        width="stretch",
    )

st.divider()

# --- SEARCH PANEL ---
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    resource_labels = {
        "Hospital": t["hospital"],
        "Blood Bank": t["blood_bank"],
        "Police Station": t["police_station"],
        "Fire Station": t["fire_station"],
    }
    resource_type = st.selectbox(
        t["need"],
        ["Hospital", "Blood Bank", "Police Station", "Fire Station"],
        format_func=lambda option: resource_labels[option],
    )
with col2:
    user_area = st.selectbox(
        t["area"],
        list(AREA_COORDS.keys()),
        format_func=lambda option: area_name_translations.get(option, option),
    )
with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    search_btn = st.button(t["search"])

st.divider()

# --- RESULTS ENGINE ---
if search_btn:
    file_map = {
        "Hospital": "data/hospitals.csv",
        "Blood Bank": "data/bloodbanks.csv",
        "Police Station": "data/policestations.csv",
        "Fire Station": "data/firestations.csv",
    }
    icon_map = {
        "Hospital": "🏥",
        "Blood Bank": "🩸",
        "Police Station": "👮",
        "Fire Station": "🚒",
    }

    df = pd.read_csv(file_map[resource_type])

    # Calculate Distances
    user_lat, user_lon = AREA_COORDS[user_area]
    df["Distance (km)"] = df.apply(
        lambda row: haversine(user_lat, user_lon, row["Latitude"], row["Longitude"]),
        axis=1,
    )

    # Sort
    sorted_df = df.sort_values(by="Distance (km)")

    translated_user_area = area_name_translations.get(user_area, user_area)
    st.markdown(f"### 📍 {t['top_results_near']} {translated_user_area}")

    for _index, row in sorted_df.iterrows():
        translated_name = resource_name_translations.get(
            row["Name"],
            row["Name"],
        )
        translated_area = area_name_translations.get(row["Area"], row["Area"])
        # Navigation link: Explicitly use resource row coordinates for destination
        nav_link = (
            f"https://www.google.com/maps/dir/?api=1&"
            f"destination={row['Latitude']},{row['Longitude']}"
        )

        st.markdown(
            f"""
            <div class="resource-card">
                <div class="resource-name">
                    {icon_map[resource_type]} {translated_name}
                </div>
                <div class="resource-info">
                    <span class="icon">📍</span>
                    <b>{t["area_label"]}:</b> {translated_area}
                </div>
                <div class="resource-info">
                    <span class="icon">📏</span> <b>{t["distance"]}:</b>
                    {row["Distance (km)"]:.2f} km
                </div>
                <div class="resource-info">
                    <span class="icon">📞</span> <b>{t["contact"]}:</b> {row["Contact"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button(f"🧭 {t['navigate']}", nav_link, type="primary")

# --- FOOTER ---
st.markdown(
    f"""
    <div style='text-align: center; color: #4A5568; margin-top: 50px;'>
        © 2026 Team MTSKV | {t["app_name"]}
    </div>
    """,
    unsafe_allow_html=True,
)
