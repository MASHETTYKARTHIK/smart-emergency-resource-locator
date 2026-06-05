import math
import os
import sys

import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from components.sidebar import (
    render_language_selector,
    render_page_styling,
    render_sidebar,
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

# Page Configuration
st.set_page_config(
    page_title="Emergency Resource Locator | Team MTSKV",
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
    """
    <div class="hero-section">
        <div class="hero-title">🚑 RESOURCES</div>
        <div class="hero-subtitle">
            High-speed resource discovery for life-critical situations.
        </div>
    </div>
""",
    unsafe_allow_html=True,
)


# --- SEARCH PANEL ---
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    resource_type = st.selectbox(
        "What do you need?",
        ["Hospital", "Blood Bank", "Police Station", "Fire Station"],
    )
with col2:
    user_area = st.selectbox("Select Area", list(AREA_COORDS.keys()))
with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    search_btn = st.button("Search Resources")

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

    st.markdown(f"### 📍 Top Results near {user_area}")

    for _index, row in sorted_df.iterrows():
        # Navigation link: Explicitly use resource row coordinates for destination
        nav_link = (
            f"https://www.google.com/maps/dir/?api=1&"
            f"destination={row['Latitude']},{row['Longitude']}"
        )

        st.markdown(
            f"""
            <div class="resource-card">
                <div class="resource-name">
                    {icon_map[resource_type]} {row["Name"]}
                </div>
                <div class="resource-info">
                    <span class="icon">📍</span> <b>Area:</b> {row["Area"]}
                </div>
                <div class="resource-info">
                    <span class="icon">📏</span> <b>Distance:</b>
                    {row["Distance (km)"]:.2f} km
                </div>
                <div class="resource-info">
                    <span class="icon">📞</span> <b>Contact:</b> {row["Contact"]}
                </div>
                <a href="{nav_link}" target="_blank" class="nav-btn">🧭 Navigate</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- FOOTER ---
st.markdown(
    """
    <div style='text-align: center; color: #4A5568; margin-top: 50px;'>
        © 2026 Team MTSKV | Smart Emergency Resource Locator
    </div>
    """,
    unsafe_allow_html=True,
)
