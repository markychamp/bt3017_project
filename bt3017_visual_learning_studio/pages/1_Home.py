import json
import streamlit as st

from components.bootstrap import setup_page
from components.cards import render_metric_card, render_topic_card
from components.ui import (
    add_vertical_space,
    render_glass_container,
    render_info_box,
    render_page_header,
    render_section_header,
    render_takeaway_box,
)
from config import TOPIC_CONTENT_FILE
from utils.state_utils import get_attempted_quiz_count, get_completed_count

setup_page("BT3017 Visual Learning Studio")


def load_topic_content() -> dict:
    if not TOPIC_CONTENT_FILE.exists():
        return {}

    try:
        with open(TOPIC_CONTENT_FILE, "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if not raw:
                return {}
            return json.loads(raw)
    except json.JSONDecodeError:
        st.warning("topic_content.json is empty or invalid. Using fallback content.")
        return {}


content = load_topic_content()
home_info = content.get("home", {})
topics = content.get("topics", [])

render_page_header(
    title=home_info.get("title", "BT3017 Visual Learning Studio"),
    subtitle=home_info.get(
        "subtitle",
        "An interactive platform for visualising and learning selected BT3017 topics."
    ),
    icon="🧠",
)

render_info_box(
    "What this platform does",
    home_info.get(
        "description",
        (
            "This application helps undergraduate students learn BT3017 through "
            "guided explanations, interactive visualisations, and short quizzes."
        ),
    ),
)

render_glass_container(
    "Why this learning studio is useful",
    (
        "Instead of relying only on static notes, this platform helps you "
        "<span class='accent-text'>see</span> concepts, <span class='accent-text'>interact</span> with them, "
        "and <span class='accent-text'>test</span> your understanding in one place."
    ),
)

add_vertical_space()

# =========================================================
# Dashboard section
# =========================================================
render_section_header(
    "Your learning dashboard",
    "Track your progress as you move through the main BT3017 topics."
)

completed = get_completed_count()
attempted = get_attempted_quiz_count()

col1, col2 = st.columns(2)
with col1:
    render_metric_card("Topics Completed", str(completed))
with col2:
    render_metric_card("Quizzes Attempted", str(attempted))

add_vertical_space()

# =========================================================
# Learning flow
# =========================================================
render_section_header(
    "How to use this app",
    "Each topic page follows the same guided learning structure."
)

render_glass_container(
    "Learning journey",
    (
        "Every topic is designed to take you through a simple sequence: "
        "<span class='accent-text'>learn the concept</span>, "
        "<span class='accent-text'>explore the visualisation</span>, "
        "<span class='accent-text'>check your understanding</span>, "
        "and <span class='accent-text'>review your progress</span>."
    ),
)

flow1, flow2, flow3, flow4 = st.columns(4)

with flow1:
    render_metric_card("1. Learn", "Read the concept")

with flow2:
    render_metric_card("2. Explore", "Interact with visuals")

with flow3:
    render_metric_card("3. Test", "Complete the quiz")

with flow4:
    render_metric_card("4. Review", "Check your progress")

add_vertical_space()

# =========================================================
# Topics section
# =========================================================
render_section_header(
    "Topics Covered",
    "Explore the main BT3017 topics included in this learning studio."
)

if topics:
    for idx in range(0, len(topics), 2):
        cols = st.columns(2)
        for col_idx in range(2):
            if idx + col_idx < len(topics):
                topic = topics[idx + col_idx]
                with cols[col_idx]:
                    render_topic_card(
                        title=topic["name"],
                        description=topic["summary"],
                        why_it_matters=topic["importance"],
                    )
else:
    render_info_box(
        "Topics not loaded",
        "Topic content could not be loaded from topic_content.json, so fallback content is being used."
    )

add_vertical_space()

# =========================================================
# Platform design rationale
# =========================================================
render_section_header(
    "Why this app is structured this way",
    "The platform is designed to support conceptual understanding, not just display code or plots."
)

col_design1, col_design2 = st.columns(2)

with col_design1:
    render_takeaway_box(
        "Teaching design",
        (
            "Each topic combines <b>intuitive explanation</b>, <b>interactive visualisation</b>, "
            "and <b>self-testing</b>. The goal is to make technical material easier to understand "
            "through active learning."
        ),
    )

with col_design2:
    render_glass_container(
        "Recommended order",
        (
            "Start with <b>PCA</b>, then move to <b>Audio Features</b>, then <b>Graph Learning</b>. "
            "After each topic, use the <span class='accent-text'>Progress & Review</span> page to see how much "
            "you have completed."
        ),
    )

add_vertical_space()

# =========================================================
# Final callout
# =========================================================
st.markdown(
    """
    <div class="example-box">
        <div class="example-label">What makes this different from ordinary notes?</div>
        <div style="line-height:1.8; color:#D6E1FB;">
            This platform is designed as an <span class="accent-text">interactive learning experience</span>,
            not just a summary page. You are encouraged to explore the visuals, compare outputs,
            and build intuition before testing yourself.
        </div>
        <div style="margin-top:0.8rem;">
            <span class="highlight-pill">learn visually</span>
            <span class="highlight-pill">interact actively</span>
            <span class="highlight-pill">revise effectively</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)