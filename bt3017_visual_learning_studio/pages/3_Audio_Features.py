import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from components.bootstrap import setup_page
from components.quiz import render_topic_quiz
from components.tutor_widget import render_tutor_widget
from components.chat_jump import render_floating_chat_jump
from components.ui import (
    add_vertical_space,
    render_glass_container,
    render_info_box,
    render_page_header,
    render_section_header,
    render_takeaway_box,
)
from utils.audio_utils import (
    add_noise,
    compute_fft,
    compute_spectrogram,
    generate_mixed_tone,
    generate_sine_wave,
    get_dominant_frequency,
)

setup_page("Audio Features • BT3017 Visual Learning Studio")

TOPIC_NAME = "Audio Features"


# =========================================================
# Plot helpers
# =========================================================
def style_dark_axes(fig, ax):
    fig.patch.set_facecolor("#120E1D")
    ax.set_facecolor("#120E1D")
    ax.tick_params(colors="#E8DFFB")
    ax.xaxis.label.set_color("#F3EAFE")
    ax.yaxis.label.set_color("#F3EAFE")
    ax.title.set_color("#FFF4FD")
    for spine in ax.spines.values():
        spine.set_color("#6B3FA0")
    ax.grid(alpha=0.22, color="#B05CFF")


def plot_waveform(t: np.ndarray, signal: np.ndarray, title: str = "Waveform"):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t, signal, linewidth=1.8, color="#FF6FEA")
    ax.set_title(title)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    style_dark_axes(fig, ax)
    return fig


def plot_fft(freqs: np.ndarray, magnitude: np.ndarray, max_freq: int = 2000):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(freqs, magnitude, linewidth=1.8, color="#00E7FF")
    ax.set_xlim(0, max_freq)
    ax.set_title("FFT Spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    style_dark_axes(fig, ax)
    return fig


def plot_spectrogram(f: np.ndarray, t: np.ndarray, mag: np.ndarray, max_freq: int = 2000):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    mesh = ax.pcolormesh(t, f, mag, shading="gouraud", cmap="magma")
    ax.set_ylim(0, max_freq)
    ax.set_title("Spectrogram")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Frequency (Hz)")
    style_dark_axes(fig, ax)

    cbar = fig.colorbar(mesh, ax=ax, label="Magnitude")
    cbar.ax.yaxis.label.set_color("#F3EAFE")
    cbar.ax.tick_params(colors="#E8DFFB")
    cbar.outline.set_edgecolor("#6B3FA0")

    return fig


# =========================================================
# Page header and teaching intro
# =========================================================
render_page_header(
    title="Audio Features",
    subtitle=(
        "Learn how sound can be represented in the time domain, transformed into frequency components, "
        "and visualised across time using a spectrogram."
    ),
    icon="🎵",
)
render_floating_chat_jump()
render_info_box(
    "Learning objectives",
    (
        "By the end of this page, you should be able to explain the difference between the "
        "<span class='accent-text'>time domain</span> and <span class='accent-text'>frequency domain</span>, "
        "interpret a waveform, understand what an <b>FFT</b> shows, and explain why a "
        "<b>spectrogram</b> is useful."
    ),
)

render_section_header(
    "What are audio features?",
    "A visual and intuitive introduction before the interactive exploration."
)

render_glass_container(
    "Audio features in one sentence",
    (
        "Audio features are useful representations of sound that make it easier to analyse, compare, "
        "and use audio signals in <i>machine learning</i>."
    ),
)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

col_intro1, col_intro2 = st.columns([1.15, 1])

with col_intro1:
    render_info_box(
        "Core intuition",
        (
            "Raw audio is a signal that changes over time. If we only look at the raw signal, it can be hard to "
            "see the important patterns inside it. Audio features help reveal the hidden structure of sound."
        ),
    )

    render_glass_container(
        "What audio feature extraction is really doing",
        (
            "Instead of treating audio as just a long list of amplitude values, we transform it into "
            "<span class='accent-text'>more meaningful views</span> such as time patterns, frequency content, "
            "and how those frequencies change over time."
        ),
    )

with col_intro2:
    render_takeaway_box(
        "Key intuition",
        (
            "A waveform shows <span class='inline-emphasis'>what the signal looks like over time</span>, "
            "but FFT and spectrograms reveal the <span class='inline-emphasis'>frequency structure</span> inside it."
        ),
    )

    render_glass_container(
        "Important views of sound",
        """
        <div class='term-block'>
            <div class='term-title'>Waveform</div>
            <div class='soft-text'>Amplitude over time.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>FFT Spectrum</div>
            <div class='soft-text'>Which frequencies are present in the signal.</div>
        </div>

        <div class='term-block' style='margin-bottom:0;'>
            <div class='term-title'>Spectrogram</div>
            <div class='soft-text'>How frequency content changes across time.</div>
        </div>
        """,
    )

add_vertical_space()

render_section_header(
    "Why do we use audio features?",
    "Audio becomes much easier to interpret when we choose the right representation."
)

col_why1, col_why2 = st.columns(2)

with col_why1:
    render_glass_container(
        "What problem they solve",
        (
            "A raw audio signal can be difficult to interpret directly because important patterns are often hidden "
            "inside the waveform. Audio features help reveal structure such as pitch, frequency mixtures, and timing."
        ),
    )

with col_why2:
    render_glass_container(
        "Why this matters in machine learning",
        (
            "Useful audio features can make sound easier to classify, compare, and analyse. "
            "They are often used in tasks such as <b>speech recognition</b>, <b>music analysis</b>, "
            "and <b>audio event detection</b>."
        ),
    )

add_vertical_space()

st.markdown(
    """
    <div class="example-box">
        <div class="example-label">Simple example</div>
        <div style="line-height:1.8; color:#D6E1FB;">
            A pure tone at <b>440 Hz</b> produces a clean single frequency peak. A mixed tone produces
            <span class="accent-text">multiple peaks</span>. A spectrogram shows <i>when</i> those
            frequencies are active over time.
        </div>
        <div style="margin-top:0.8rem;">
            <span class="highlight-pill">time view</span>
            <span class="highlight-pill">frequency view</span>
            <span class="highlight-pill">time-frequency view</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Sidebar controls
# =========================================================
st.sidebar.markdown("## 🎵 Audio Controls")

signal_type = st.sidebar.selectbox(
    "Signal type",
    ["Pure Tone", "Mixed Tone"],
)

sample_rate = st.sidebar.selectbox(
    "Sample rate",
    [4000, 8000, 16000],
    index=1,
)

duration = st.sidebar.slider(
    "Duration (seconds)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1,
)

noise_level = st.sidebar.slider(
    "Noise level",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
)

freq1 = st.sidebar.slider(
    "Frequency 1 (Hz)",
    min_value=100,
    max_value=1200,
    value=440,
    step=10,
)

amp1 = st.sidebar.slider(
    "Amplitude 1",
    min_value=0.1,
    max_value=2.0,
    value=1.0,
    step=0.1,
)

if signal_type == "Mixed Tone":
    freq2 = st.sidebar.slider(
        "Frequency 2 (Hz)",
        min_value=100,
        max_value=2000,
        value=880,
        step=10,
    )
    amp2 = st.sidebar.slider(
        "Amplitude 2",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
        step=0.1,
    )
else:
    freq2 = None
    amp2 = None

# =========================================================
# Generate signal
# =========================================================
if signal_type == "Pure Tone":
    t_axis, signal = generate_sine_wave(
        frequency=freq1,
        amplitude=amp1,
        sample_rate=sample_rate,
        duration=duration,
    )
else:
    t_axis, signal = generate_mixed_tone(
        freq1=freq1,
        freq2=freq2,
        amp1=amp1,
        amp2=amp2,
        sample_rate=sample_rate,
        duration=duration,
    )

if noise_level > 0:
    signal = add_noise(signal, noise_level=noise_level)

freqs, magnitude = compute_fft(signal, sample_rate)
spec_f, spec_t, spec_mag = compute_spectrogram(signal, sample_rate)
dominant_frequency = get_dominant_frequency(freqs, magnitude)
add_vertical_space()

# =========================================================
# Lesson tabs
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "1. Waveform",
        "2. FFT",
        "3. Spectrogram",
        "4. Compare & Interpret",
        "5. Quiz",
    ]
)

# =========================================================
# Tab 1
# =========================================================
with tab1:
    render_section_header(
        "Waveform: the time-domain view",
        "The waveform shows how the signal amplitude changes over time."
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_waveform(t_axis, signal)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "What to notice",
            (
                "The waveform shows the raw signal directly. "
                "A <b>pure tone</b> looks smooth and regular, while a mixed or noisy signal usually looks more complex."
            ),
        )

        render_glass_container(
            "Reading the waveform",
            """
            - <b>Time</b> is on the x-axis<br>
            - <b>Amplitude</b> is on the y-axis<br>
            - This view is useful, but it does not clearly show which frequencies are present
            """,
        )

# =========================================================
# Tab 2
# =========================================================
with tab2:
    render_section_header(
        "FFT: the frequency-domain view",
        "FFT shows which frequencies are present in the signal."
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_fft(freqs, magnitude)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "What FFT reveals",
            (
                "FFT breaks the signal into its frequency components. "
                "A pure tone usually gives <span class='accent-text'>one strong peak</span>, "
                "while a mixed tone gives <span class='accent-text'>multiple peaks</span>."
            ),
        )

        st.metric("Dominant frequency", f"{dominant_frequency:.1f} Hz")

        render_glass_container(
            "How to read the FFT",
            """
            - Peaks correspond to strong frequency components<br>
            - Higher peaks mean stronger presence of that frequency<br>
            - FFT is often more informative than the waveform for identifying pitch-like patterns
            """,
        )

# =========================================================
# Tab 3
# =========================================================
with tab3:
    render_section_header(
        "Spectrogram: frequency over time",
        "A spectrogram shows how frequency content changes across time."
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_spectrogram(spec_f, spec_t, spec_mag)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "Why spectrograms matter",
            (
                "FFT over the whole signal tells you what frequencies exist overall, but not "
                "<i>when</i> they occur. A spectrogram adds the missing time dimension."
            ),
        )

        render_glass_container(
            "How to read the spectrogram",
            """
            - <b>x-axis</b>: time<br>
            - <b>y-axis</b>: frequency<br>
            - Brighter regions indicate stronger frequency content<br>
            - This is especially useful for sounds that change over time
            """,
        )

# =========================================================
# Tab 4
# =========================================================
with tab4:
    render_section_header(
        "Compare and interpret",
        "Use all three views together to understand the signal more deeply."
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = plot_waveform(t_axis, signal, title="Waveform Summary")
        st.pyplot(fig, use_container_width=True)

        fig_fft = plot_fft(freqs, magnitude)
        st.pyplot(fig_fft, use_container_width=True)

    with col2:
        fig_spec = plot_spectrogram(spec_f, spec_t, spec_mag)
        st.pyplot(fig_spec, use_container_width=True)

    render_info_box(
        "How to interpret all three together",
        (
            "The waveform shows the raw shape of the signal, the FFT reveals the frequencies present, "
            "and the spectrogram shows <i>when</i> those frequencies occur. These three representations "
            "complement each other."
        ),
    )

    render_takeaway_box(
        "Main learning point",
        (
            "Raw audio alone may be hard to interpret. Feature engineering turns sound into "
            "<span class='accent-text'>more useful representations</span> for analysis and machine learning."
        ),
    )

# =========================================================
# Tab 5
# =========================================================
with tab5:
    render_section_header(
        "Check your understanding",
        "Complete the quiz below to reinforce the key ideas from this topic."
    )

    render_topic_quiz(TOPIC_NAME)

    add_vertical_space()

    render_takeaway_box(
        "Common misconceptions",
        (
            "FFT does not show <i>when</i> a frequency occurs, only that it is present overall. "
            "The waveform is not the same as the spectrum. The spectrogram combines both "
            "<b>time</b> and <b>frequency</b> information."
        ),
    )
add_vertical_space(2)
st.markdown(
    "<div id='bt3017-chatbot' class='chat-anchor-space'></div>",
    unsafe_allow_html=True,
)
render_tutor_widget("Audio Features")