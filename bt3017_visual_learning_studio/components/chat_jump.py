import streamlit as st


def render_floating_chat_jump(anchor_id: str = "bt3017-chatbot") -> None:
    st.markdown(
        f"""
        <a href="#{anchor_id}" class="floating-chat-jump">
            💬 Ask Tutor
        </a>
        """,
        unsafe_allow_html=True,
    )