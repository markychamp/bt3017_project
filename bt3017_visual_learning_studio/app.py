import streamlit as st

from components.bootstrap import setup_page

setup_page("BT3017 Visual Learning Studio")

st.markdown(
    """
    <div class="hero-box">
        <h1>Welcome to BT3017 Visual Learning Studio</h1>
        <p>
            This is a modular interactive learning platform for selected BT3017 topics.
            Use the page navigation on the left to explore concept explanations,
            interactive visualisations, and quizzes.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="info-card">
        <b>How to use this app</b><br>
        1. Start from the Home page.<br>
        2. Go through each topic page.<br>
        3. Interact with the visuals.<br>
        4. Attempt the quiz at the end of each topic.<br>
        5. Review your progress on the Progress & Review page.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Use the multipage navigation in the sidebar to continue.")