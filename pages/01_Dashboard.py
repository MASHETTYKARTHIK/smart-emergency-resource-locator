import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Add src to path for imports
SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from components.sidebar import (  # noqa: E402
    render_language_selector,
    render_page_styling,
    render_sidebar,
)
from utils.translations import AREA_NAME_TRANSLATIONS, TRANSLATIONS  # noqa: E402

lang = st.session_state.get(
    "language_selector",
    st.session_state.get("language", "English"),
)
t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
st.session_state["language"] = lang if lang in TRANSLATIONS else "English"
area_name_translations = AREA_NAME_TRANSLATIONS.get(
    lang,
    AREA_NAME_TRANSLATIONS["English"],
)

st.set_page_config(page_title=t["dashboard"], layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title(f"📊 {t['resource_dashboard']}")

hospitals = pd.read_csv("data/hospitals.csv")
bloodbanks = pd.read_csv("data/bloodbanks.csv")
police = pd.read_csv("data/policestations.csv")
fire = pd.read_csv("data/firestations.csv")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(f"🏥 {t['hospitals']}", len(hospitals))

with col2:
    st.metric(f"🩸 {t['blood_banks']}", len(bloodbanks))

with col3:
    st.metric(f"👮 {t['police_stations']}", len(police))

with col4:
    st.metric(f"🚒 {t['fire_stations']}", len(fire))

st.divider()

chart_data = pd.DataFrame(
    {
        t["resource"]: [
            t["hospitals"],
            t["blood_banks"],
            t["police_stations"],
            t["fire_stations"],
        ],
        t["count"]: [len(hospitals), len(bloodbanks), len(police), len(fire)],
    }
)

pie = px.pie(
    chart_data,
    names=t["resource"],
    values=t["count"],
    title=t["emergency_resources_distribution"],
)

st.plotly_chart(pie, width="stretch")

bar = px.bar(
    chart_data,
    x=t["resource"],
    y=t["count"],
    title=t["resource_count_comparison"],
)

st.plotly_chart(bar, width="stretch")

st.divider()

all_data = pd.concat(
    [hospitals[["Area"]], bloodbanks[["Area"]], police[["Area"]], fire[["Area"]]]
)

area_count = all_data["Area"].value_counts().reset_index()
area_count["Area"] = area_count["Area"].map(
    lambda area: area_name_translations.get(area, area)
)
area_count.columns = pd.Index([t["area_label"], t["resources"]])

area_chart = px.bar(
    area_count,
    x=t["area_label"],
    y=t["resources"],
    title=t["area_wise_resource_distribution"],
)

st.plotly_chart(area_chart, width="stretch")
