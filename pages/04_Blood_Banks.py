import os
import sys

import pandas as pd
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
from utils.translations import (  # noqa: E402
    AREA_NAME_TRANSLATIONS,
    RESOURCE_NAME_TRANSLATIONS,
    TRANSLATIONS,
)

lang = st.session_state.get(
    "language_selector",
    st.session_state.get("language", "English"),
)
t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
st.session_state["language"] = lang if lang in TRANSLATIONS else "English"
resource_name_translations = RESOURCE_NAME_TRANSLATIONS.get(
    lang,
    RESOURCE_NAME_TRANSLATIONS["English"],
)
area_name_translations = AREA_NAME_TRANSLATIONS.get(
    lang,
    AREA_NAME_TRANSLATIONS["English"],
)

st.set_page_config(page_title=t["blood_banks"], layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title(f"🩸 {t['blood_banks']}")

df = pd.read_csv("data/bloodbanks.csv")

st.markdown(
    f"""
    <div class="hero-section" style="padding: 25px; margin-bottom: 25px;">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="color: #F8FAFC; font-size: 1.2rem; font-weight: 700;">
                    {t["blood_supply_network"]}
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    {t["blood_supply_subtitle"]}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: #FF4B4B; font-size: 2rem; font-weight: 800;">
                    {len(df)}
                </div>
                <div style="
                    color: #64748B;
                    font-size: 0.7rem;
                    font-weight: 700;
                    text-transform: uppercase;
                ">{t["total_active"]}</div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Grid Layout for Cards
cols = st.columns(2)
for i, (_index, row) in enumerate(df.iterrows()):
    col_idx = i % 2
    with cols[col_idx]:
        translated_name = resource_name_translations.get(
            row["Name"],
            row["Name"],
        )
        translated_area = area_name_translations.get(row["Area"], row["Area"])
        nav_link = (
            f"https://www.google.com/maps/dir/?api=1&destination="
            f"{row['Latitude']},{row['Longitude']}"
        )
        st.markdown(
            f"""
            <div class="resource-card">
                <div class="resource-name">🩸 {translated_name}</div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">location_on</span>
                    <b>{t["area_label"]}:</b> {translated_area}
                </div>
                <div class="resource-info">
                    <span class="material-symbols-rounded" style="
                        font-size: 18px;
                        color: #FF4B4B;
                    ">call</span>
                    <b>{t["contact"]}:</b> {row["Contact"]}
                </div>
                <a href="{nav_link}" target="_blank" class="nav-btn">
                    <span style="display: flex; align-items: center; gap: 8px;">
                        <span class="material-symbols-rounded" style="
                            font-size: 18px;
                        ">directions</span>
                        {t["navigate_now"]}
                    </span>
                </a>
            </div>
        """,
            unsafe_allow_html=True,
        )
