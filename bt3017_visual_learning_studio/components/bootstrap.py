import streamlit as st
from typing import Optional

from config import APP_ICON, APP_LAYOUT, APP_TITLE, CSS_FILE
from utils.state_utils import init_session_state


def load_css() -> None:
    """Load external CSS file."""
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render shared sidebar with custom navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <h2>🧠 BT3017 Studio</h2>
                <p>Interactive visual learning for key BT3017 topics</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-nav-note">
                Use the navigation below to move through the learning studio.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/2_PCA.py", label="PCA", icon="📉")
        st.page_link("pages/3_Audio_Features.py", label="Audio Features", icon="🎵")
        st.page_link("pages/4_Graph_Learning.py", label="Graph Learning", icon="🕸️")
        st.page_link("pages/5_Progress_Review.py", label="Progress & Review", icon="📊")


def setup_page(page_title: Optional[str] = None) -> None:
    """Shared setup for every page in the multipage app."""
    st.set_page_config(
        page_title=page_title or APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state="expanded",
    )
    load_css()
    init_session_state()
    render_sidebar()