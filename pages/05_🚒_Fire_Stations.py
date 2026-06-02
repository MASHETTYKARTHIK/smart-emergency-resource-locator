import pandas as pd
import streamlit as st

st.set_page_config(page_title="Fire Stations", page_icon="🚒")

st.title("🚒 Fire Stations")

df = pd.read_csv("data/firestations.csv")

st.dataframe(df, use_container_width=True)

st.metric("Total Fire Stations", len(df))

st.info("In case of fire emergency, call 101 immediately.")
