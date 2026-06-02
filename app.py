import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Emergency Resource Locator | Team MTSKV",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM CSS STYLING ---
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #0E1117;
    }

    /* Header Styling */
    .hero-section {
        background: linear-gradient(90deg, #1E1E1E 0%, #121212 100%);
        padding: 40px;
        border-radius: 20px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .hero-title {
        color: #FF4B4B;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        color: #888888;
        font-size: 1.2rem;
    }

    /* Card Styling */
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
        color: #FFFFFF;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .resource-info {
        color: #A0AEC0;
        font-size: 1rem;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
    }

    .icon {
        margin-right: 10px;
        color: #FF4B4B;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #2D3748;
    }

    /* Metric Styling */
    div[data-testid="metric-container"] {
        background-color: #1A202C;
        border: 1px solid #2D3748;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }

    /* Button Styling */
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

    /* Input Field Styling */
    div[data-baseweb="select"] {
        border-radius: 10px;
    }

    hr {
        margin: 40px 0;
        border-color: #2D3748;
    }

</style>
""", unsafe_allow_html=True)

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
    st.caption("Developed by: Manoj, Teja, Sampath, Karthik, Viplav")

# --- MAIN CONTENT: HERO SECTION ---
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🚑 Smart Emergency Locator</div>
        <div class="hero-subtitle">High-speed resource discovery for life-critical situations.</div>
    </div>
""", unsafe_allow_html=True)

# --- DASHBOARD METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏥 Hospitals", "24/7", "Active")
col2.metric("🩸 Blood Banks", "Available", "Priority")
col3.metric("👮 Police", "Rapid", "Response")
col4.metric("🚒 Fire", "Ready", "Alert")

st.markdown("<br>", unsafe_allow_html=True)

# --- SEARCH PANEL ---
with st.container():
    search_col1, search_col2, search_col3 = st.columns([2, 2, 1])
    
    with search_col1:
        resource = st.selectbox(
            "What do you need?",
            ["Hospital", "Blood Bank", "Police Station", "Fire Station"],
            index=0
        )
        
    with search_col2:
        location = st.selectbox(
            "Select Area",
            ["Gachibowli", "Madhapur", "Kukatpally", "Ameerpet", "Secunderabad"],
            index=0
        )
        
    with search_col3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        search_btn = st.button("Search Resources")

st.divider()

# --- RESULTS ENGINE ---
if search_btn:
    # Business Logic (Unchanged)
    if resource == "Hospital":
        df = pd.read_csv("data/hospitals.csv")
        icon = "🏥"
    elif resource == "Blood Bank":
        df = pd.read_csv("data/bloodbanks.csv")
        icon = "🩸"
    elif resource == "Police Station":
        df = pd.read_csv("data/policestations.csv")
        icon = "👮"
    else:
        df = pd.read_csv("data/firestations.csv")
        icon = "🚒"

    filtered = df[df["Area"].str.contains(location, case=False, na=False)]

    if not filtered.empty:
        st.markdown(f"### 📍 Found {len(filtered)} {resource}s in {location}")
        
        # Rendering modern cards instead of plain table
        for index, row in filtered.iterrows():
            st.markdown(f"""
                <div class="resource-card">
                    <div class="resource-name">{icon} {row['Name']}</div>
                    <div class="resource-info">
                        <span class="icon">📍</span> <b>Area:</b> {row['Area']}
                    </div>
                    <div class="resource-info">
                        <span class="icon">📞</span> <b>Contact:</b> {row['Contact']}
                    </div>
                    <div class="resource-info">
                        <span class="icon">🌐</span> <b>Coordinates:</b> {row['Latitude']}, {row['Longitude']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"No {resource}s found in {location}. Try a nearby area.")
else:
    # Initial state or "Ready" message
    st.markdown("""
        <div style="text-align: center; padding: 50px; color: #4A5568;">
            <img src="https://cdn-icons-png.flaticon.com/512/854/854878.png" width="100" style="opacity: 0.5;">
            <h3>Select a resource and location above to begin.</h3>
        </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #4A5568; font-size: 0.8rem;">
        © 2026 Team MTSKV | Smart Emergency Resource Locator | Built with Streamlit
    </div>
""", unsafe_allow_html=True)
