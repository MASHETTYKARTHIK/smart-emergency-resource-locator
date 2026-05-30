import streamlit as st
import pandas as pd

st.title("🚑 Smart Emergency Resource Locator")

resource = st.selectbox(
    "Select Emergency Type",
    ["Hospital", "Blood Bank", "Police Station", "Fire Station"]
)

location = st.text_input("Enter Location")

if st.button("Search"):

    if resource == "Hospital":
        df = pd.read_csv("hospitals.csv")

    elif resource == "Blood Bank":
        df = pd.read_csv("bloodbanks.csv")

    elif resource == "Police Station":
        df = pd.read_csv("policestations.csv")

    else:
        df = pd.read_csv("firestations.csv")

    st.success("Resources Found")
    st.dataframe(df)