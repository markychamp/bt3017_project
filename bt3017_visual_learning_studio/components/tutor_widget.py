import streamlit as st

from components.ui import render_glass_container, render_info_box, render_section_header
from services.openai_client import ask_openai_tutor
from utils.tutor_context import get_topic_context
from utils.tutor_state import (
    add_page_message,
    clear_page_messages,
    get_page_messages,
    init_tutor_state,
)


@st.fragment
def render_tutor_widget(page_key: str, title: str = "Ask the BT3017 Tutor") -> None:
    init_tutor_state()

    messages = get_page_messages(page_key)
    topic_context = get_topic_context(page_key)

    with st.expander(title, expanded=False):
        render_info_box(
            "What this tutor does",
            (
                f"This tutor is focused on <b>{page_key}</b>. Ask it to explain concepts, "
                f"clarify confusion, or compare ideas from this topic."
            ),
        )

        if not messages:
            render_glass_container(
                "Suggested questions",
                """
                - Can you explain this in simpler terms?<br>
                - What is the intuition behind this topic?<br>
                - Can you compare the main ideas here?<br>
                - Why does this matter in machine learning?
                """,
            )

        chat_box = st.container(height=320)

        with chat_box:
            for msg in messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        col1, col2 = st.columns([0.8, 0.2])
        with col2:
            if st.button("Clear Chat", key=f"clear_{page_key}"):
                clear_page_messages(page_key)
                st.rerun()

        # Important: inline chat_input inside the expander/container
        user_input = st.chat_input(
            f"Ask about {page_key}...",
            key=f"chat_input_{page_key}",
        )

        if user_input:
            add_page_message(page_key, "user", user_input)
            reply = ask_openai_tutor(
                messages=get_page_messages(page_key),
                topic_context=topic_context,
                page_name=page_key,
            )
            add_page_message(page_key, "assistant", reply)
            st.rerun()