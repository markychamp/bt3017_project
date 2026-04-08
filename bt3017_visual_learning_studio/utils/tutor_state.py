import streamlit as st


def init_tutor_state() -> None:
    if "tutor_messages" not in st.session_state:
        st.session_state.tutor_messages = {}

    if "tutor_topic_scope" not in st.session_state:
        st.session_state.tutor_topic_scope = "Current Topic"


def get_page_messages(page_key: str) -> list[dict]:
    if page_key not in st.session_state.tutor_messages:
        st.session_state.tutor_messages[page_key] = []
    return st.session_state.tutor_messages[page_key]


def add_page_message(page_key: str, role: str, content: str) -> None:
    if page_key not in st.session_state.tutor_messages:
        st.session_state.tutor_messages[page_key] = []
    st.session_state.tutor_messages[page_key].append(
        {"role": role, "content": content}
    )


def clear_page_messages(page_key: str) -> None:
    st.session_state.tutor_messages[page_key] = []