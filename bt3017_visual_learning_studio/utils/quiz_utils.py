import json
import random
from typing import Any

import streamlit as st

from config import QUIZ_BANK_FILE, QUIZ_QUESTIONS_PER_TOPIC


def load_quiz_bank() -> dict[str, list[dict[str, Any]]]:
    """Load the quiz bank from JSON."""
    if not QUIZ_BANK_FILE.exists():
        return {}

    with open(QUIZ_BANK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_questions_for_topic(topic: str) -> list[dict[str, Any]]:
    """Return a stable sampled set of questions for the topic within the session."""
    quiz_bank = load_quiz_bank()
    topic_questions = quiz_bank.get(topic, [])

    if not topic_questions:
        return []

    session_key = f"selected_questions_{topic}"

    if session_key not in st.session_state:
        sample_size = min(QUIZ_QUESTIONS_PER_TOPIC, len(topic_questions))
        st.session_state[session_key] = random.sample(topic_questions, sample_size)

    return st.session_state[session_key]


def reset_topic_questions(topic: str) -> None:
    """Reset selected questions for a topic."""
    session_key = f"selected_questions_{topic}"
    if session_key in st.session_state:
        del st.session_state[session_key]