import os
import sys

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
from utils.translations import RESOURCE_NAME_TRANSLATIONS, TRANSLATIONS  # noqa: E402

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

st.set_page_config(page_title=t["ai_assistant"], layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title(f"🤖 {t['ai_emergency_assistant']}")

st.markdown(
    f"""
    <div class="hero-section" style="padding: 30px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="
                background: rgba(255, 75, 75, 0.1);
                width: 50px;
                height: 50px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid rgba(255, 75, 75, 0.2);
            ">
                <span class="material-symbols-rounded" style="
                    color: #FF4B4B;
                    font-size: 30px;
                ">psychology</span>
            </div>
            <div>
                <div style="color: #F8FAFC; font-size: 1.5rem; font-weight: 700;">
                    {t["intelligent_dispatcher"]}
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    {t["ai_subtitle"]}
                </div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

user_input = st.text_area(
    t["emergency_description"],
    placeholder=t["emergency_placeholder"],
    height=120,
)

if st.button(t["analyze_situation"]):
    if user_input:
        text = user_input.lower()

        # User Message
        st.markdown(
            f"""
            <div class="chat-message user">
                <span class="material-symbols-rounded" style="
                    color: #94A3B8;
                ">person</span>
                <div>
                    <div style="
                        font-weight: 700;
                        color: #F8FAFC;
                        font-size: 0.8rem;
                        margin-bottom: 5px;
                    ">{t["you"]}</div>
                    <div style="color: #CBD5E1;">{user_input}</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Bot logic
        response = None
        icon = "info"
        service = ""
        suggestion = ""

        if "accident" in text or "injury" in text or "medical" in text:
            service = t["hospital"]
            icon = "hospital"
            suggestion = "AIG Hospital"
        elif "blood" in text:
            service = t["blood_bank"]
            icon = "bloodtype"
            suggestion = "Red Cross Blood Bank"
        elif "fire" in text or "smoke" in text:
            service = t["fire_station"]
            icon = "fire_truck"
            suggestion = "Gachibowli Fire Station"
        elif (
            "theft" in text or "robbery" in text or "crime" in text or "police" in text
        ):
            service = t["police_station"]
            icon = "local_police"
            suggestion = "Gachibowli Police Station"

        if service:
            translated_suggestion = resource_name_translations.get(
                suggestion,
                suggestion,
            )
            st.markdown(
                f"""
                <div class="chat-message bot">
                    <span class="material-symbols-rounded" style="
                        color: #FF4B4B;
                    ">smart_toy</span>
                    <div>
                        <div style="
                            font-weight: 700;
                            color: #FF4B4B;
                            font-size: 0.8rem;
                            margin-bottom: 5px;
                        ">{t["ai_assistant_label"]}</div>
                        <div style="color: #F8FAFC; margin-bottom: 10px;">
                            {t["situation_analyzed"]}
                        </div>
                        <div style="
                            background: rgba(255, 75, 75, 0.1);
                            border: 1px solid rgba(255, 75, 75, 0.2);
                            border-radius: 12px;
                            padding: 15px;
                            display: flex;
                            align-items: center;
                            gap: 15px;
                        ">
                            <span class="material-symbols-rounded" style="
                                color: #FF4B4B;
                                font-size: 24px;
                            ">{icon}</span>
                            <div>
                                <div style="
                                    font-weight: 700;
                                    color: #F8FAFC;
                                ">{service} {t["required"]}</div>
                                <div style="
                                    font-size: 0.8rem;
                                    color: #94A3B8;
                                ">{t["nearest_unit"]} {translated_suggestion}</div>
                            </div>
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-message bot">
                    <span class="material-symbols-rounded" style="
                        color: #FF4B4B;
                    ">smart_toy</span>
                    <div>
                        <div style="
                            font-weight: 700;
                            color: #FF4B4B;
                            font-size: 0.8rem;
                            margin-bottom: 5px;
                        ">{t["ai_assistant_label"]}</div>
                        <div style="color: #F8FAFC;">
                            {t["identify_error"]}
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.warning(t["enter_description_warning"])
