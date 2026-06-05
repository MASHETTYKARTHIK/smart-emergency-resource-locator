import sys
import os
import pandas as pd
import streamlit as st

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import render_sidebar, render_language_selector, render_page_styling

st.set_page_config(page_title="Fire Stations", layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title("🚒 Fire Stations")

df = pd.read_csv("data/firestations.csv")

st.markdown(f"""
    <div class="hero-section" style="padding: 25px; margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #F8FAFC; font-size: 1.2rem; font-weight: 700;">Fire & Rescue Command</div>
                <div style="color: #94A3B8; font-size: 0.9rem;">Rapid response units for fire emergencies.</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #FF4B4B; font-size: 2rem; font-weight: 800;">{len(df)}</div>
                <div style="color: #64748B; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">Total Active</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Grid Layout for Cards
cols = st.columns(2)
for index, row in df.iterrows():
    col_idx = index % 2
    with cols[col_idx]:
        nav_link = f"https://www.google.com/maps/dir/?api=1&destination={row['Latitude']},{row['Longitude']}"
        st.markdown(f"""
            <div class="resource-card">
                <div class="resource-name">🚒 {row['Name']}</div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="font-size: 18px; color: #FF4B4B;">location_on</span>
                    <b>Area:</b> {row['Area']}
                </div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="font-size: 18px; color: #FF4B4B;">call</span>
                    <b>Contact:</b> {row['Contact']}
                </div>
                <a href="{nav_link}" target="_blank" class="nav-btn">
                    <span style="display: flex; align-items: center; gap: 8px;">
                        <span class="material-symbols-rounded" style="font-size: 18px;">directions</span>
                        Navigate Now
                    </span>
                </a>
            </div>
        """, unsafe_allow_html=True)

st.info("In case of fire emergency, call 101 immediately.")
