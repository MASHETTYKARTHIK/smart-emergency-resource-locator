import math

import pandas as pd
import streamlit as st


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

# --- PREMIUM CSS STYLING ---
st.markdown(
    """
<style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap'
    );
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; }
    .hero-section {
        background: linear-gradient(90deg, #1E1E1E 0%, #121212 100%);
        padding: 40px;
        border-radius: 20px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-title {
        color: #FF4B4B; font-size: 3rem; font-weight: 700; margin-bottom: 10px;
    }
    .hero-subtitle { color: #888888; font-size: 1.2rem; }
    .resource-card {
        background-color: #1E252E;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #2D3748;
        transition: all 0.3s ease;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .resource-card:hover {
        border-color: #FF4B4B;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(255, 75, 75, 0.1);
    }
    .resource-name {
        color: #FFFFFF; font-size: 1.4rem; font-weight: 600; margin-bottom: 10px;
    }
    .resource-info {
        color: #A0AEC0; font-size: 1rem; margin-bottom: 5px;
        display: flex; align-items: center;
    }
    .icon { margin-right: 10px; color: #FF4B4B; }
    section[data-testid="stSidebar"] {
        background-color: #161B22; border-right: 1px solid #2D3748;
    }
    div[data-testid="metric-container"] {
        background-color: #1A202C; border: 1px solid #2D3748;
        padding: 20px; border-radius: 15px; text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #FF4B4B 0%, #D32F2F 100%);
        color: white;
        font-weight: 700;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }
    .nav-btn {
        display: inline-block;
        padding: 8px 16px;
        background-color: #FF4B4B;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1022/1022313.png", width=80)
    st.markdown("## Mission Control")
    st.info("Helping citizens find emergency resources in record time.")
    st.divider()
    st.markdown("### 📞 Emergency Hotline")
    st.error("🚓 **Police:** 100")
    st.error("🚑 **Ambulance:** 108")
    st.error("🚒 **Fire:** 101")
    st.warning("👩 **Women Helpline:** 181")
    st.divider()
    st.markdown("### 🏛️ About Team MTSKV")
    st.caption("A CivicTech initiative for a safer Hyderabad.")

# --- MAIN CONTENT ---
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-title">🚑 Smart Emergency Locator</div>
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
