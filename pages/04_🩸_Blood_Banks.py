import pandas as pd
import streamlit as st

st.title("🩸 Blood Banks")

df = pd.read_csv("data/bloodbanks.csv")

st.dataframe(df)

st.metric("Total Blood Banks", len(df))
