import streamlit as st


def render_topic_card(title: str, description: str, why_it_matters: str) -> None:
    st.markdown(
        f"""
        <div class="topic-card">
            <h3 style="margin-top:0; margin-bottom:0.75rem;">{title}</h3>
            <p style="margin-bottom:0.55rem;"><b style="color:#EDF2FF;">What it covers:</b> {description}</p>
            <p style="margin-bottom:0;"><b style="color:#EDF2FF;">Why it matters:</b> {why_it_matters}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4 style="margin-top:0; margin-bottom:0.45rem; color:#C9D5F2;">{label}</h4>
            <p style="font-size:1.45rem; font-weight:800; margin:0; color:#9BB6FF;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )