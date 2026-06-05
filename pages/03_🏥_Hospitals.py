import pandas as pd
import streamlit as st

st.title("🏥 Hospitals")

df = pd.read_csv("data/hospitals.csv")

st.dataframe(df)

st.metric("Total Hospitals", len(df))

import requests
import folium
from streamlit_folium import st_folium

st.divider()
st.subheader("🔍 Search Live Location on Google Maps")

location_query = st.text_input("Enter location:", placeholder="e.g., Apollo Hospital Hyderabad")
maps_url = f"https://www.google.com/maps/search/{location_query.replace(' ', '+')}"
if location_query:
    st.link_button("Open in Google Maps", url=maps_url)

if st.button("Find Nearby on Map"):
    if not location_query:
        st.error("Please enter a location first!")
    else:
        with st.spinner("Fetching data from OpenStreetMap..."):
            overpass_url = "https://overpass-api.de/api/interpreter"
            query = """
            [out:json];
            (
              node["amenity"="hospital"](around:5000, 17.3850, 78.4867);
              way["amenity"="hospital"](around:5000, 17.3850, 78.4867);
            );
            out;
            """
            try:
                headers = {
                    "User-Agent": "SmartEmergencyAllocator/1.0 (contact@example.com)"
                }
                response = requests.get(overpass_url, params={'data': query}, headers=headers)
                response.raise_for_status()
                data = response.json()
                if not data['elements']:
                    st.warning("No results found nearby.")
                else:
                    results = []
                    for element in data['elements']:
                        name = element.get('tags', {}).get('name', 'Unknown')
                        lat = element.get('lat', 0)
                        lon = element.get('lon', 0)
                        results.append({'Name': name, 'Latitude': lat, 'Longitude': lon})
                    df_res = pd.DataFrame(results)
                    st.dataframe(df_res)
                    m = folium.Map(location=[17.3850, 78.4867], zoom_start=13)
                    for _, row in df_res.iterrows():
                        folium.Marker([row['Latitude'], row['Longitude']], popup=row['Name']).add_to(m)
                    st_folium(m, width=700, height=400)
            except Exception as e:
                st.error(f"Error fetching data: {e}")
