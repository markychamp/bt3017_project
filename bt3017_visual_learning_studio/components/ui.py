import streamlit as st


def render_page_header(title: str, subtitle: str = "", icon: str = "") -> None:
    heading = f"{icon} {title}".strip()
    st.markdown(
        f"""
        <div class="hero-box">
            <h1>{heading}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, description: str = "") -> None:
    st.markdown(f"## {title}")
    if description:
        st.markdown(
            f"<p style='margin-top:-0.2rem; margin-bottom:1rem; color:#9FB0D4;'>{description}</p>",
            unsafe_allow_html=True,
        )


def render_info_box(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="info-card">
            <h4 style="margin-top:0; margin-bottom:0.55rem;">{title}</h4>
            <div style="line-height:1.7;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_takeaway_box(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="takeaway-card">
            <h4 style="margin-top:0; margin-bottom:0.55rem;">{title}</h4>
            <div style="line-height:1.7;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_glass_container(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="topic-card">
            <div class="muted-text" style="text-transform:uppercase; letter-spacing:0.08em; font-weight:700; margin-bottom:0.45rem;">
                {title}
            </div>
            <div style="line-height:1.75; color:#D3DDF5;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_bullets(items: list[str]) -> None:
    for item in items:
        st.write(f"- {item}")


def add_vertical_space(lines: int = 1) -> None:
    for _ in range(lines):
        st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)