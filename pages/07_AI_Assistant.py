import os
import sys

import streamlit as st

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from components.sidebar import (
    render_language_selector,
    render_page_styling,
    render_sidebar,
)

st.set_page_config(page_title="AI Assistant", layout="wide")

# Render Components
render_sidebar()
render_language_selector()
render_page_styling()

st.title("🤖 AI Emergency Assistant")

st.markdown(
    """
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
                    Intelligent Dispatcher
                </div>
                <div style="color: #94A3B8; font-size: 0.9rem;">
                    Describe your emergency for instant resource routing.
                </div>
            </div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

user_input = st.text_area(
    "Emergency Description",
    placeholder=(
        "Example: Medical emergency near HITEC City or fire reported "
        "in Banjara Hills..."
    ),
    height=120,
)

if st.button("Analyze Situation"):
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
                    ">YOU</div>
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
            service = "Hospital"
            icon = "hospital"
            suggestion = "AIG Hospital, Gachibowli"
        elif "blood" in text:
            service = "Blood Bank"
            icon = "bloodtype"
            suggestion = "Red Cross Blood Bank"
        elif "fire" in text or "smoke" in text:
            service = "Fire Station"
            icon = "fire_truck"
            suggestion = "Gachibowli Fire Station"
        elif (
            "theft" in text or "robbery" in text or "crime" in text or "police" in text
        ):
            service = "Police Station"
            icon = "local_police"
            suggestion = "Gachibowli Police Station"

        if service:
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
                        ">AI ASSISTANT</div>
                        <div style="color: #F8FAFC; margin-bottom: 10px;">
                            Situation analyzed. 
                            Recommended emergency service identified:
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
                                ">{service} Required</div>
                                <div style="
                                    font-size: 0.8rem;
                                    color: #94A3B8;
                                ">Nearest Unit: {suggestion}</div>
                            </div>
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
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
                        ">AI ASSISTANT</div>
                        <div style="color: #F8FAFC;">
                            I'm having trouble identifying the emergency type.
                            Please provide more specific details (e.g., medical,
                            fire, accident).
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("Please enter a description first.")
