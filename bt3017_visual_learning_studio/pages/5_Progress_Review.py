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
from config import TOPICS
from utils.state_utils import (
    get_attempted_quiz_count,
    get_completed_count,
    get_total_score,
    reset_progress,
)

setup_page("Progress & Review • BT3017 Visual Learning Studio")

render_page_header(
    title="Progress & Review",
    subtitle=(
        "Track your learning progress across topics, review quiz performance, "
        "and decide what to revisit next."
    ),
    icon="📊",
)

render_info_box(
    "What this page does",
    (
        "This page summarises your <span class='accent-text'>topic completion</span> and "
        "<span class='accent-text'>quiz performance</span> for the current session. "
        "Use it to identify which topics you have covered well and which ones still need revision."
    ),
)

render_glass_container(
    "How to use this page",
    (
        "A good revision flow is to first check your progress, then revisit any weaker topic pages, "
        "interact with the visuals again, and finally retry the quiz."
    ),
)

completed_topics = get_completed_count()
attempted_quizzes = get_attempted_quiz_count()
total_score = get_total_score()
max_possible_score = attempted_quizzes * 3

# =========================================================
# Overall metrics
# =========================================================
render_section_header(
    "Overall Progress",
    "A quick snapshot of your learning progress so far."
)

col1, col2, col3 = st.columns(3)

with col1:
    render_metric_card("Topics Completed", f"{completed_topics}/{len(TOPICS)}")

with col2:
    render_metric_card("Quizzes Attempted", f"{attempted_quizzes}/{len(TOPICS)}")

with col3:
    if attempted_quizzes == 0:
        render_metric_card("Total Quiz Score", "0")
    else:
        render_metric_card("Total Quiz Score", f"{total_score}/{max_possible_score}")

add_vertical_space()

# =========================================================
# Progress bars
# =========================================================
render_section_header(
    "Completion Overview",
    "These progress bars show how far you have moved through the platform."
)

topic_progress = completed_topics / len(TOPICS) if TOPICS else 0
quiz_progress = attempted_quizzes / len(TOPICS) if TOPICS else 0

col_prog1, col_prog2 = st.columns(2)

with col_prog1:
    render_glass_container(
        "Topic Completion",
        (
            f"You have completed <span class='accent-text'>{completed_topics}</span> out of "
            f"<span class='accent-text'>{len(TOPICS)}</span> topic modules."
        ),
    )
    st.progress(topic_progress)

with col_prog2:
    render_glass_container(
        "Quiz Completion",
        (
            f"You have attempted <span class='accent-text'>{attempted_quizzes}</span> out of "
            f"<span class='accent-text'>{len(TOPICS)}</span> topic quizzes."
        ),
    )
    st.progress(quiz_progress)

add_vertical_space()

# =========================================================
# Topic breakdown
# =========================================================
render_section_header(
    "Topic Breakdown",
    "Review your completion status and quiz performance for each topic."
)

quiz_scores = st.session_state.get("quiz_scores", {})
quiz_attempted = st.session_state.get("quiz_attempted", {})
completed = st.session_state.get("completed_topics", {})

for topic in TOPICS:
    attempted = quiz_attempted.get(topic, False)
    done = completed.get(topic, False)
    score = quiz_scores.get(topic)

    status_text = (
        "You completed this topic in the current session."
        if done else
        "This topic has not been completed yet."
    )

    if attempted and score is not None:
        quiz_text = f"Quiz score recorded: {score}/3"
    else:
        quiz_text = "Quiz not attempted yet."

    render_topic_card(
        title=topic,
        description=status_text,
        why_it_matters=quiz_text,
    )

add_vertical_space()

# =========================================================
# Study advice
# =========================================================
render_section_header(
    "Study Advice",
    "Use your progress to decide what to revise next."
)

if completed_topics == 0:
    render_info_box(
        "Getting started",
        (
            "You have not completed any topic yet. A good place to begin is "
            "<b>PCA</b>, followed by <b>Audio Features</b>, then <b>Graph Learning</b>."
        ),
    )
elif completed_topics < len(TOPICS):
    render_info_box(
        "Next step",
        (
            "You have already started making progress. Continue with the remaining topics and use "
            "the quizzes to check whether your understanding is improving."
        ),
    )
else:
    render_takeaway_box(
        "Nice work",
        (
            "You have completed all main topics in this session. Use this page to identify weaker quiz areas "
            "and revisit those topic modules for revision."
        ),
    )

render_glass_container(
    "Recommended revision strategy",
    """
    - Revisit topics where your quiz score was lower<br>
    - Use the interactive visuals again before retrying a quiz<br>
    - Try explaining the topic in your own words after reviewing it<br>
    - Focus on understanding the intuition, not just memorising terms
    """,
)

add_vertical_space()

# =========================================================
# Reset
# =========================================================
render_section_header(
    "Reset Session Progress",
    "Use this if you want to restart the learning journey in the current session."
)

render_glass_container(
    "What reset does",
    (
        "This clears all <span class='accent-text'>topic completion</span> and "
        "<span class='accent-text'>quiz score</span> data stored in the current session."
    ),
)

if st.button("Reset My Progress"):
    reset_progress()
    st.success("Your session progress has been reset.")