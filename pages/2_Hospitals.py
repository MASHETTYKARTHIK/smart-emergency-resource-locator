import streamlit as st
import pandas as pd

st.title("🏥 Hospitals")

df = pd.read_csv("data/hospitals.csv")

st.dataframe(df)

st.metric("Total Hospitals", len(df))