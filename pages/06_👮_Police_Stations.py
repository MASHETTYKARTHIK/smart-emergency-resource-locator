import pandas as pd
import streamlit as st

st.set_page_config(page_title="Police Stations", page_icon="👮")

st.title("👮 Police Stations")

df = pd.read_csv("data/policestations.csv")

st.dataframe(df, use_container_width=True)

st.metric("Total Police Stations", len(df))

st.info(
    "In case of emergency, call 100 immediately to reach the nearest police station."
)
