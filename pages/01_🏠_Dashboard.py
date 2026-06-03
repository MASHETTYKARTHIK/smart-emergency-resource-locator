import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard")

st.title("📊 Smart Emergency Resource Locator Dashboard")

hospitals = pd.read_csv("data/hospitals.csv")
bloodbanks = pd.read_csv("data/bloodbanks.csv")
police = pd.read_csv("data/policestations.csv")
fire = pd.read_csv("data/firestations.csv")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏥 Hospitals", len(hospitals))

with col2:
    st.metric("🩸 Blood Banks", len(bloodbanks))

with col3:
    st.metric("👮 Police Stations", len(police))

with col4:
    st.metric("🚒 Fire Stations", len(fire))

st.divider()

chart_data = pd.DataFrame(
    {
        "Resource": ["Hospitals", "Blood Banks", "Police Stations", "Fire Stations"],
        "Count": [len(hospitals), len(bloodbanks), len(police), len(fire)],
    }
)

pie = px.pie(
    chart_data,
    names="Resource",
    values="Count",
    title="Emergency Resources Distribution",
)

st.plotly_chart(pie, use_container_width=True)

bar = px.bar(chart_data, x="Resource", y="Count", title="Resource Count Comparison")

st.plotly_chart(bar, use_container_width=True)

st.divider()

all_data = pd.concat(
    [hospitals[["Area"]], bloodbanks[["Area"]], police[["Area"]], fire[["Area"]]]
)

area_count = all_data["Area"].value_counts().reset_index()
area_count.columns = pd.Index(["Area", "Resources"])

area_chart = px.bar(
    area_count, x="Area", y="Resources", title="Area-wise Resource Distribution"
)

st.plotly_chart(area_chart, use_container_width=True)
