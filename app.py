import streamlit as st
import pandas as pd
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: #FF4B4B;
}

h2,h3 {
    color: white;
}

div[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #FF4B4B;
    padding: 15px;
    border-radius: 15px;
}

.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Smart Emergency Resource Locator",
    page_icon="🚑",
    layout="wide"
)

st.title("🚑 Smart Emergency Resource Locator")

st.markdown("""
### About the Project

Smart Emergency Resource Locator helps citizens quickly locate emergency services during critical situations.

### Available Services

🏥 Hospitals

🩸 Blood Banks

👮 Police Stations

🚒 Fire Stations
""")

resource = st.selectbox(
    "Select Emergency Type",
    ["Hospital", "Blood Bank", "Police Station", "Fire Station"]
)

location = st.selectbox(
    "Select Location",
    [
        "Gachibowli",
        "Madhapur",
        "Kukatpally",
        "Ameerpet",
        "Secunderabad"
    ]
)

if st.button("Search Resources"):

    if resource == "Hospital":
        df = pd.read_csv("data/hospitals.csv")

    elif resource == "Blood Bank":
        df = pd.read_csv("data/bloodbanks.csv")

    elif resource == "Police Station":
        df = pd.read_csv("data/policestations.csv")

    else:
        df = pd.read_csv("data/firestations.csv")

    filtered = df[
        df["Area"].str.contains(
            location,
            case=False,
            na=False
        )
    ]

    st.success("Resources Found")

    st.dataframe(filtered)

st.divider()

st.subheader("📞 Emergency Contacts")

col1, col2 = st.columns(2)

with col1:
    st.info("🚓 Police : 100")
    st.info("🚑 Ambulance : 108")

with col2:
    st.info("🚒 Fire : 101")
    st.info("👩 Women Helpline : 181")