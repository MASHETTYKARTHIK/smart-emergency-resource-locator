import streamlit as st


def render_sidebar():
    # Google Fonts URLs
    INTER_FONT = (
        "https://fonts.googleapis.com/css2?"
        "family=Inter:wght@400;500;600;700&display=swap"
    )
    MATERIAL_ICONS = (
        "https://fonts.googleapis.com/css2?"
        "family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0"
    )

    # --- PREMIUM CSS STYLING ---
    st.markdown(
        f"""
    <style>
        /* Import Premium Fonts */
        @import url('{INTER_FONT}');
        @import url('{MATERIAL_ICONS}');

        /* Sidebar Styling - Frosted Glass */
        [data-testid="stSidebar"] {{
            background-color: rgba(15, 23, 42, 0.95) !important;
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}

        /* Hide default navigation */
        [data-testid="stSidebarNav"] {{
            display: none;
        }}

        /* Mission Control Card - Glassmorphism */
        .mission-control-card {{
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 18px;
            margin: 10px 0 25px 0;
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }}

        .mission-control-card:hover {{
            border-color: rgba(255, 75, 75, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }}

        .mission-control-card::after {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 100%;
            background: linear-gradient(
                135deg,
                rgba(255, 75, 75, 0.1) 0%,
                transparent 50%,
                rgba(255, 75, 75, 0.05) 100%
            );
            opacity: 0.4;
            z-index: 0;
            animation: pulse-gradient 8s infinite alternate;
        }}

        @keyframes pulse-gradient {{
            0% {{ opacity: 0.2; }}
            100% {{ opacity: 0.5; }}
        }}

        /* Navigation Links - Rounded Pills */
        .stPageLink {{
            border-radius: 12px !important;
            margin-bottom: 6px !important;
            transition: all 0.25s ease !important;
            border: 1px solid transparent !important;
            padding: 8px 14px !important;
        }}

        .stPageLink:hover {{
            background-color: rgba(255, 255, 255, 0.08) !important;
            transform: translateX(6px) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }}

        /* Active Link Gradient Highlight */
        [data-testid="stPageLinkActive"] {{
            background: linear-gradient(
                90deg,
                rgba(255, 75, 75, 0.2) 0%,
                rgba(255, 75, 75, 0.05) 100%
            ) !important;
            border-left: 4px solid #FF4B4B !important;
            color: #FF4B4B !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.1);
        }}

        [data-testid="stPageLinkActive"] span {{
            color: #FF4B4B !important;
        }}

        /* Section Separators */
        .sidebar-section-label {{
            font-size: 0.7rem;
            font-weight: 700;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 20px 0 10px 8px;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # App Logo & Branding - Clean "RESOURCES"
        st.markdown(
            """
        <div style="display: flex; align-items: center; gap: 12px;
                    margin-bottom: 30px; padding: 10px 10px;">
            <div style="background: linear-gradient(135deg, #FF4B4B 0%, #D32F2F 100%);
                        width: 38px; height: 38px; border-radius: 10px;
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);">
                <span class="material-symbols-rounded"
                      style="color: white; font-size: 22px;">emergency</span>
            </div>
            <div>
                <div style="font-size: 1.2rem; font-weight: 700; color: white;
                            letter-spacing: 1px;">RESOURCES</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Mission Control Card
        st.markdown(
            """
        <div class="mission-control-card">
            <div style="position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 10px;
                            margin-bottom: 12px;">
                    <div style="background: rgba(255, 75, 75, 0.15); width: 28px;
                                height: 28px; border-radius: 6px; display: flex;
                                align-items: center; justify-content: center;">
                        <span class="material-symbols-rounded"
                              style="color: #FF4B4B; font-size: 16px;">radar</span>
                    </div>
                    <span style="font-weight: 600; color: #F8FAFC;
                                 font-size: 0.9rem;">Mission Control</span>
                    <div style="margin-left: auto; width: 8px; height: 8px;
                                background: #10B981; border-radius: 50%;
                                box-shadow: 0 0 8px #10B981;"></div>
                </div>
                <p style="color: #94A3B8; font-size: 0.75rem;
                          line-height: 1.4; margin: 0;">
                    Real-time monitoring active. System Status:
                    <span style="color: #10B981; font-weight: 600;">Optimal</span>
                </p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Navigation
        st.markdown(
            '<div class="sidebar-section-label">General</div>', unsafe_allow_html=True
        )
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/01_Dashboard.py", label="Dashboard", icon="📊")
        st.page_link("pages/02_🗺️_Resource_Map.py", label="Resource Map", icon="🗺️")

        st.markdown(
            '<div class="sidebar-section-label">Resources</div>', unsafe_allow_html=True
        )
        st.page_link("pages/03_🏥_Hospitals.py", label="Hospitals", icon="🏥")
        st.page_link("pages/04_Blood_Banks.py", label="Blood Banks", icon="🩸")
        st.page_link("pages/05_🚒_Fire_Stations.py", label="Fire Stations", icon="🚒")
        st.page_link(
            "pages/06_👮_Police_Stations.py", label="Police Stations", icon="👮"
        )

        st.markdown(
            '<div class="sidebar-section-label">AI Intelligence</div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/07_AI_Assistant.py", label="AI Assistant", icon="🤖")


def render_page_styling():
    st.markdown(
        """
    <style>
        /* Global Theme - Deep Navy */
        .main {
            background-color: #0B1120 !important;
            background-image: radial-gradient(
                circle at top right, rgba(255, 75, 75, 0.05), transparent 400px
            ),
            radial-gradient(
                circle at bottom left, rgba(30, 64, 175, 0.1), transparent 400px
            );
        }

        /* Glassmorphism Metrics */
        .stMetric {
            background-color: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 24px !important;
            border-radius: 20px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            transition: transform 0.3s ease;
        }
        .stMetric:hover {
            transform: translateY(-4px);
            border-color: rgba(255, 75, 75, 0.2);
        }

        div[data-testid="metric-container"] {
            background-color: transparent !important;
            border: none !important;
        }

        /* Hero/Search Sections - Glassmorphism */
        .hero-section {
            background: rgba(30, 41, 59, 0.45) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 45px;
            border-radius: 28px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 35px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            position: relative;
        }
        .hero-section::before {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 6px; height: 100%;
            background: linear-gradient(to bottom, #FF4B4B, #D32F2F);
            border-radius: 28px 0 0 28px;
        }
        .hero-title {
            color: #F8FAFC; font-size: 2.8rem; font-weight: 800; margin-bottom: 8px;
            letter-spacing: -1.5px;
        }
        .hero-subtitle { color: #94A3B8; font-size: 1.15rem; font-weight: 400; }

        /* Glassmorphism Cards */
        .resource-card {
            background-color: rgba(30, 41, 59, 0.4) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 28px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .resource-card:hover {
            border-color: rgba(255, 75, 75, 0.3);
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(255, 75, 75, 0.12),
                        0 0 0 1px rgba(255, 75, 75, 0.1);
        }
        .resource-name {
            color: #F8FAFC; font-size: 1.4rem; font-weight: 700; margin-bottom: 14px;
        }
        .resource-info {
            color: #94A3B8; font-size: 0.95rem; margin-bottom: 10px;
            display: flex; align-items: center; gap: 12px;
        }

        /* Forms & Inputs - Glassmorphism */
        .stSelectbox, .stTextInput, .stTextArea {
            background-color: rgba(30, 41, 59, 0.3) !important;
            border-radius: 14px !important;
        }
        div[data-baseweb="select"] {
            background-color: rgba(30, 41, 59, 0.4) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        div[data-baseweb="input"] {
            background-color: rgba(30, 41, 59, 0.4) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        /* Buttons - Gradient */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #FF4B4B 0%, #B91C1C 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 14px 28px !important;
            border-radius: 14px !important;
            border: none !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-size: 0.85rem !important;
            box-shadow: 0 8px 20px rgba(255, 75, 75, 0.25) !important;
        }
        .stButton>button:hover {
            transform: scale(1.03) translateY(-2px);
            box-shadow: 0 12px 25px rgba(255, 75, 75, 0.4) !important;
        }

        /* AI Assistant - Chat Bubbles */
        .chat-message {
            padding: 1.5rem; border-radius: 20px; margin-bottom: 1rem;
            display: flex; gap: 1rem; backdrop-filter: blur(10px);
        }
        .chat-message.user {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .chat-message.bot {
            background-color: rgba(255, 75, 75, 0.05);
            border: 1px solid rgba(255, 75, 75, 0.1);
        }

        /* Navigation Button (Link) */
        .nav-btn {
            display: inline-block;
            padding: 12px 24px;
            background: rgba(255, 75, 75, 0.08);
            color: #FF4B4B !important;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-top: 18px;
            border: 1px solid rgba(255, 75, 75, 0.15);
            transition: all 0.3s ease;
        }
        .nav-btn:hover {
            background: #FF4B4B;
            color: white !important;
            box-shadow: 0 8px 20px rgba(255, 75, 75, 0.3);
            transform: scale(1.05);
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_language_selector():
    # Language selector at top right - Glassmorphism
    col1, col2, col3 = st.columns([7, 2, 1])
    with col2:
        st.markdown(
            """
        <div style="display: flex; align-items: center;
                    justify-content: flex-end; gap: 10px; height: 100%;">
            <div style="background: rgba(255, 255, 255, 0.05); width: 34px;
                        height: 34px; border-radius: 10px; display: flex;
                        align-items: center; justify-content: center;
                        border: 1px solid rgba(255, 255, 255, 0.1);">
                <span class="material-symbols-rounded"
                      style="color: #94A3B8; font-size: 20px;">language</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        st.selectbox(
            "Language",
            ["English", "हिन्दी", "తెలుగు"],
            label_visibility="collapsed",
            index=0,
            key="language_selector",
        )
