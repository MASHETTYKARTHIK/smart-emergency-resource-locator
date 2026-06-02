import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("🗺️ Emergency Resource Map")

resource = st.selectbox(
    "Select Resource Type",
    [
        "Hospitals",
        "Blood Banks",
        "Police Stations",
        "Fire Stations"
    ]
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

m = folium.Map(
    location=[17.44, 78.38],
    zoom_start=11
)

for _, row in df.iterrows():

    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=f"{row['Name']}\n{row['Contact']}",
        tooltip=row["Area"],
        icon=folium.Icon(color=color)
    ).add_to(m)

st_folium(
    m,
    width=1000,
    height=600
)