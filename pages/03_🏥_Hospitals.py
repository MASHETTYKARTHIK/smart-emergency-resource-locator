import pandas as pd
import streamlit as st

st.title("🏥 Hospitals")

df = pd.read_csv("data/hospitals.csv")

st.dataframe(df)

st.metric("Total Hospitals", len(df))
