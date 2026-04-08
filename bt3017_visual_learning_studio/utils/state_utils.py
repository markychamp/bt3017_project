import streamlit as st

from config import TOPICS


def init_session_state() -> None:
    """Initialise all session state keys used across the app."""
    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {topic: None for topic in TOPICS}

    if "quiz_attempted" not in st.session_state:
        st.session_state.quiz_attempted = {topic: False for topic in TOPICS}

    if "completed_topics" not in st.session_state:
        st.session_state.completed_topics = {topic: False for topic in TOPICS}

    if "selected_questions" not in st.session_state:
        st.session_state.selected_questions = {}

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    if "last_page" not in st.session_state:
        st.session_state.last_page = "Home"


def mark_topic_completed(topic: str) -> None:
    """Mark a topic as completed."""
    if topic in st.session_state.completed_topics:
        st.session_state.completed_topics[topic] = True


def save_quiz_score(topic: str, score: int) -> None:
    """Save quiz score and mark quiz attempted."""
    st.session_state.quiz_scores[topic] = score
    st.session_state.quiz_attempted[topic] = True


def get_completed_count() -> int:
    """Return number of completed topics."""
    return sum(st.session_state.completed_topics.values())


def get_attempted_quiz_count() -> int:
    """Return number of quizzes attempted."""
    return sum(st.session_state.quiz_attempted.values())


def get_total_score() -> int:
    """Return sum of all available quiz scores."""
    total = 0
    for score in st.session_state.quiz_scores.values():
        if score is not None:
            total += score
    return total


def reset_progress() -> None:
    """Reset completion and quiz state."""
    st.session_state.quiz_scores = {topic: None for topic in TOPICS}
    st.session_state.quiz_attempted = {topic: False for topic in TOPICS}
    st.session_state.completed_topics = {topic: False for topic in TOPICS}
    st.session_state.selected_questions = {}
    st.session_state.user_answers = {}