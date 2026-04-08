import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from components.bootstrap import setup_page
from components.tutor_widget import render_tutor_widget
from components.chat_jump import render_floating_chat_jump
setup_page("PCA • BT3017 Visual Learning Studio")
from components.quiz import render_topic_quiz
from components.ui import (
    add_vertical_space,
    render_glass_container,
    render_info_box,
    render_page_header,
    render_section_header,
    render_takeaway_box,
)
from data.pca_datasets import (
    PCA_DATASET_OPTIONS,
    get_pca_dataset,
    get_pca_dataset_metadata,
)
from utils.pca_utils import (
    apply_standardisation,
    compute_reconstruction_error,
    fit_pca,
    get_axis_limits,
    get_pc1_angle_degrees,
    project_onto_pc1,
    reconstruct_from_pc1,
)


TOPIC_NAME = "PCA"


# =========================================================
# Plot helpers
# =========================================================
def plot_original_data(X: np.ndarray, title: str = "Original Dataset"):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(X[:, 0], X[:, 1], alpha=0.8, s=40)
    xmin, xmax, ymin, ymax = get_axis_limits(X)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title(title)
    ax.grid(alpha=0.25)
    return fig


def plot_data_with_pca_axes(
    X: np.ndarray,
    pca,
    color_values: np.ndarray | None = None,
    title: str = "Original Data with PCA Axes",
):
    fig, ax = plt.subplots(figsize=(7, 5.5))

    if color_values is None:
        ax.scatter(X[:, 0], X[:, 1], alpha=0.8, s=40)
    else:
        scatter = ax.scatter(X[:, 0], X[:, 1], c=color_values, alpha=0.85, s=40)
        plt.colorbar(scatter, ax=ax, label="PC1 Score")

    mean = pca.mean_
    comps = pca.components_
    var = pca.explained_variance_

    scale1 = 2.6 * np.sqrt(var[0])
    scale2 = 2.6 * np.sqrt(var[1])

    pc1 = comps[0] * scale1
    pc2 = comps[1] * scale2

    ax.arrow(
        mean[0],
        mean[1],
        pc1[0],
        pc1[1],
        head_width=0.18,
        length_includes_head=True,
        linewidth=2.2,
    )
    ax.text(mean[0] + pc1[0], mean[1] + pc1[1], "PC1", fontsize=11, weight="bold")

    ax.arrow(
        mean[0],
        mean[1],
        pc2[0],
        pc2[1],
        head_width=0.18,
        length_includes_head=True,
        linewidth=2.2,
    )
    ax.text(mean[0] + pc2[0], mean[1] + pc2[1], "PC2", fontsize=11, weight="bold")

    xmin, xmax, ymin, ymax = get_axis_limits(X)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title(title)
    ax.grid(alpha=0.25)

    return fig


def plot_projection(X: np.ndarray, projected: np.ndarray, pca, color_values: np.ndarray | None = None):
    fig, ax = plt.subplots(figsize=(7, 5.5))

    if color_values is None:
        ax.scatter(X[:, 0], X[:, 1], alpha=0.7, s=40, label="Original Points")
    else:
        scatter = ax.scatter(X[:, 0], X[:, 1], c=color_values, alpha=0.8, s=40, label="Original Points")
        plt.colorbar(scatter, ax=ax, label="PC1 Score")

    ax.scatter(projected[:, 0], projected[:, 1], alpha=0.9, s=30, marker="x", label="Projection onto PC1")

    for i in range(len(X)):
        ax.plot(
            [X[i, 0], projected[i, 0]],
            [X[i, 1], projected[i, 1]],
            linestyle="dotted",
            linewidth=0.8,
            alpha=0.5,
        )

    mean = pca.mean_
    comps = pca.components_
    var = pca.explained_variance_

    scale1 = 2.6 * np.sqrt(var[0])
    pc1 = comps[0] * scale1

    ax.arrow(
        mean[0],
        mean[1],
        pc1[0],
        pc1[1],
        head_width=0.18,
        length_includes_head=True,
        linewidth=2.2,
    )
    ax.text(mean[0] + pc1[0], mean[1] + pc1[1], "PC1", fontsize=11, weight="bold")

    xmin, xmax, ymin, ymax = get_axis_limits(X)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title("Projection onto PC1")
    ax.legend(loc="best")
    ax.grid(alpha=0.25)

    return fig


def plot_pca_space(X_pca: np.ndarray):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.8, s=40)
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.axvline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("Data in PCA Space")
    ax.grid(alpha=0.25)
    return fig


def plot_explained_variance(pca):
    ratios = pca.explained_variance_ratio_
    cumulative = np.cumsum(ratios)
    labels = ["PC1", "PC2"]

    fig, ax = plt.subplots(figsize=(7, 4.8))
    bars = ax.bar(labels, ratios, alpha=0.85, label="Explained Variance Ratio")
    ax.plot(labels, cumulative, marker="o", linewidth=2.0, label="Cumulative Explained Variance")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Proportion of Variance")
    ax.set_title("Explained Variance")
    ax.legend(loc="best")
    ax.grid(axis="y", alpha=0.25)

    for bar, ratio in zip(bars, ratios):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{ratio:.2f}",
            ha="center",
            va="bottom",
        )

    return fig


def plot_reconstruction(X: np.ndarray, X_reconstructed: np.ndarray):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(X[:, 0], X[:, 1], alpha=0.7, s=40, label="Original")
    ax.scatter(
        X_reconstructed[:, 0],
        X_reconstructed[:, 1],
        alpha=0.85,
        s=30,
        marker="x",
        label="Reconstructed from PC1",
    )

    for i in range(len(X)):
        ax.plot(
            [X[i, 0], X_reconstructed[i, 0]],
            [X[i, 1], X_reconstructed[i, 1]],
            linestyle="dotted",
            linewidth=0.8,
            alpha=0.4,
        )

    xmin, xmax, ymin, ymax = get_axis_limits(np.vstack([X, X_reconstructed]))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.set_title("Reconstruction from 1 Component")
    ax.legend(loc="best")
    ax.grid(alpha=0.25)
    return fig


def plot_rotation_demo(X: np.ndarray, angle_deg: float):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(X[:, 0], X[:, 1], alpha=0.8, s=40)

    xmin, xmax, ymin, ymax = get_axis_limits(X)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    center = X.mean(axis=0)
    length = max(xmax - xmin, ymax - ymin) * 0.35
    angle = np.deg2rad(angle_deg)

    vec1 = np.array([np.cos(angle), np.sin(angle)]) * length
    vec2 = np.array([-np.sin(angle), np.cos(angle)]) * length

    ax.arrow(
        center[0],
        center[1],
        vec1[0],
        vec1[1],
        head_width=0.18,
        length_includes_head=True,
        linewidth=2.2,
    )
    ax.text(center[0] + vec1[0], center[1] + vec1[1], "Axis 1", fontsize=10, weight="bold")

    ax.arrow(
        center[0],
        center[1],
        vec2[0],
        vec2[1],
        head_width=0.18,
        length_includes_head=True,
        linewidth=2.2,
    )
    ax.text(center[0] + vec2[0], center[1] + vec2[1], "Axis 2", fontsize=10, weight="bold")

    ax.set_title(f"Axis Rotation Demo ({angle_deg:.0f}°)")
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.grid(alpha=0.25)
    return fig


# =========================================================
# Page Header
# =========================================================
render_page_header(
    title="Principal Component Analysis (PCA)",
    subtitle=(
        "Learn how PCA finds the directions of greatest variation, projects data "
        "onto new axes, and reduces dimensionality while preserving important structure."
    ),
    icon="📉",
)
render_floating_chat_jump()
render_info_box(
    "Learning objectives",
    (
        "By the end of this page, you should be able to explain <span class='accent-text'>PCA</span> "
        "in simple language, identify <b>PC1</b> and <b>PC2</b>, understand <i>projection</i> and "
        "<i>explained variance</i>, and see why <b>standardisation</b> can affect the result."
    ),
)

render_section_header(
    "What is PCA?",
    "A visual and intuitive introduction before the interactive exploration."
)

render_glass_container(
    "PCA in one sentence",
    (
        "Principal Component Analysis (PCA) is a method that finds the "
        "<span class='accent-text'>most important directions</span> in a dataset and uses them "
        "to describe the data <i>more compactly</i>."
    ),
)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

col_intro1, col_intro2 = st.columns([1.15, 1])

with col_intro1:
    render_info_box(
        "Core intuition",
        (
            "Imagine your data points form a long tilted cloud. Even though the data is stored using "
            "<b>Feature 1</b> and <b>Feature 2</b>, the strongest pattern may actually lie along that "
            "<span class='inline-emphasis'>tilted direction</span>. PCA finds that direction first."
        ),
    )

    render_glass_container(
        "What PCA is really doing",
        (
            "Instead of keeping the original axes exactly as they are, PCA creates "
            "<span class='accent-text'>new axes</span> that better match the way the data is spread out. "
            "This makes it easier to summarise the <b>most important variation</b>."
        ),
    )

with col_intro2:
    render_takeaway_box(
        "Key intuition",
        (
            "PCA is like <span class='inline-emphasis'>rotating the coordinate system</span> so that the "
            "new axes line up with the shape of the data."
        ),
    )

    render_glass_container(
        "Important terms",
        """
        <div class='term-block'>
            <div class='term-title'>PC1</div>
            <div class='soft-text'>The direction of <b>greatest variance</b>.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>PC2</div>
            <div class='soft-text'>The next most important direction, <i>perpendicular</i> to PC1.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>Projection</div>
            <div class='soft-text'>Representing data using the new PCA axes.</div>
        </div>

        <div class='term-block' style='margin-bottom:0;'>
            <div class='term-title'>Explained Variance</div>
            <div class='soft-text'>How much information each component keeps.</div>
        </div>
        """,
    )

add_vertical_space()

render_section_header(
    "Why do we use PCA?",
    "PCA is useful when the original features overlap in meaning or contain redundancy."
)

col_why1, col_why2 = st.columns(2)

with col_why1:
    render_glass_container(
        "What problem it solves",
        (
            "In many datasets, some features are <b>correlated</b> or partially repetitive. "
            "That means we may be storing <span class='accent-text'>more dimensions than we really need</span>. "
            "PCA helps reduce that redundancy while keeping the main structure of the data."
        ),
    )

with col_why2:
    render_glass_container(
        "Why it matters in machine learning",
        (
            "A lower-dimensional representation can make data easier to "
            "<b>visualise</b>, easier to <b>interpret</b>, and sometimes easier for models to "
            "<b>learn from</b>. PCA is often used as a compact summary of a dataset."
        ),
    )

add_vertical_space()

st.markdown(
    """
    <div class="example-box">
        <div class="example-label">Simple real-life example</div>
        <div style="line-height:1.8; color:#D6E1FB;">
            Suppose one feature is <b>hours studied</b> and another is <b>number of practice papers done</b>. 
            These may be strongly related. PCA can combine them into a new direction that roughly captures 
            <span class="accent-text">overall study effort</span>, instead of treating them as completely separate.
        </div>
        <div style="margin-top:0.8rem;">
            <span class="highlight-pill">reduces redundancy</span>
            <span class="highlight-pill">captures main pattern</span>
            <span class="highlight-pill">simplifies representation</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Sidebar Controls
# =========================================================
st.sidebar.markdown("## 📉 PCA Controls")

dataset_name = st.sidebar.selectbox(
    "Choose a dataset",
    PCA_DATASET_OPTIONS,
)

n_samples = st.sidebar.slider("Number of samples", min_value=60, max_value=250, value=120, step=10)
seed = st.sidebar.slider("Random seed", min_value=1, max_value=100, value=42, step=1)
standardise = st.sidebar.checkbox("Standardise features before PCA", value=False)
color_by_pc1 = st.sidebar.checkbox("Color points by PC1 score", value=False)

# Iris should ignore sample count
if dataset_name == "Iris (2 Features)":
    X_raw = get_pca_dataset(dataset_name, n_samples=150, seed=seed)
else:
    X_raw = get_pca_dataset(dataset_name, n_samples=n_samples, seed=seed)

dataset_meta = get_pca_dataset_metadata(dataset_name)

X = apply_standardisation(X_raw, standardise)
pca, X_pca = fit_pca(X)
projected, scores_pc1 = project_onto_pc1(X, pca)
X_reconstructed = reconstruct_from_pc1(X_pca, pca)
reconstruction_error = compute_reconstruction_error(X, X_reconstructed)
pc1_angle = get_pc1_angle_degrees(pca)

point_colors = scores_pc1 if color_by_pc1 else None
add_vertical_space()

# =========================================================
# Lesson Tabs
# =========================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "1. Observe",
        "2. Predict",
        "3. Reveal PCA",
        "4. Project & Reduce",
        "5. Evaluate",
        "6. Quiz",
    ]
)

# =========================================================
# Tab 1 - Observe
# =========================================================
with tab1:
    render_section_header(
        "Observe the data first",
        "Before using PCA, first look at the overall shape of the dataset.",
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_original_data(X)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            f"Dataset: {dataset_meta['title']}",
            (
                f"<b>What it is:</b> {dataset_meta['brief']}<br><br>"
                f"<b>Why it is useful for PCA:</b> {dataset_meta['why_useful']}"
            ),
        )

        observe_html = "<br>".join([f"- {point}" for point in dataset_meta["what_to_observe"]])

        render_glass_container(
            "What to observe",
            observe_html,
        )

        if standardise:
            st.success("Standardisation is ON. The features are now on a comparable scale.")
        else:
            st.warning("Standardisation is OFF. Large-scale features may dominate PCA.")
        add_vertical_space()

        render_takeaway_box(
            "Dataset learning focus",
            (
                f"For <b>{dataset_meta['title']}</b>, pay attention to whether the data has "
                f"a strong dominant direction and how that affects PC1, explained variance, "
                f"and projection."
            ),
        )
# =========================================================
# Tab 2 - Predict
# =========================================================
with tab2:
    render_section_header(
        "Guess before reveal",
        "Try predicting the direction PCA will choose before seeing the result.",
    )

    guess = st.radio(
        "Which direction do you think PCA will choose as PC1?",
        ["Horizontal", "Vertical", "Diagonal"],
        key="pca_guess_direction",
    )

    if st.button("Reveal the likely answer", key="reveal_pca_guess"):
        if dataset_name == "Circular Cloud":
            st.info(
                "This dataset is more evenly spread, so there is no strongly dominant direction. "
                "PCA still chooses one, but the result is less dramatic."
            )
        elif dataset_name in ["Elongated Diagonal Cloud", "Clustered Correlated Data", "Different Feature Scales", "Iris (2 Features)"]:
            st.success(
                "PCA chooses the direction of maximum variance. In these datasets, that is usually diagonal or tilted."
            )

        if guess == "Diagonal":
            st.caption("Your guess matches the most common PCA outcome for correlated or elongated datasets.")
        else:
            st.caption("That guess is understandable, but PCA usually follows the strongest spread in the data.")

    add_vertical_space()

    render_takeaway_box(
        "Why this step matters",
        (
            "This encourages active learning. Instead of passively reading the answer, "
            "you first form an intuition about the shape of the data."
        ),
    )

# =========================================================
# Tab 3 - Reveal PCA
# =========================================================
with tab3:
    render_section_header(
        "Reveal the principal components",
        "Now see the new axes that PCA creates.",
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_data_with_pca_axes(X, pca, color_values=point_colors)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "What PCA is doing",
            (
                "PCA rotates the coordinate system so that the new axes align with the main spread of the data. "
                "PC1 captures the most variance, while PC2 captures the next most variance and is perpendicular to PC1."
            ),
        )

        st.metric("Explained variance by PC1", f"{pca.explained_variance_ratio_[0] * 100:.1f}%")
        st.metric("Explained variance by PC2", f"{pca.explained_variance_ratio_[1] * 100:.1f}%")

    add_vertical_space()

    render_section_header(
        "Axis rotation demo",
        "Use the slider to simulate the idea that PCA rotates the axes to better match the data.",
    )

    angle_slider = st.slider(
        "Rotate axes manually (degrees)",
        min_value=-90,
        max_value=90,
        value=int(round(pc1_angle)),
        step=1,
    )
    fig_rotate = plot_rotation_demo(X, angle_slider)
    st.pyplot(fig_rotate, use_container_width=True)

# =========================================================
# Tab 4 - Project & Reduce
# =========================================================
with tab4:
    render_section_header(
        "Projection and dimensionality reduction",
        "PCA reduces dimensions by projecting data onto the most important direction.",
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = plot_projection(X, projected, pca, color_values=point_colors)
        st.pyplot(fig, use_container_width=True)

    with col2:
        fig = plot_pca_space(X_pca)
        st.pyplot(fig, use_container_width=True)

    render_info_box(
        "What changed?",
        (
            "The plot on the left shows the original points being projected onto PC1. "
            "The plot on the right shows the same data rewritten in PCA coordinates. "
            "This is how PCA turns the data into a new, often more meaningful representation."
        ),
    )

    render_takeaway_box(
        "Key idea",
        (
            "Reducing from 2D to 1D means keeping only the coordinate along PC1. "
            "This preserves the strongest structure, but some smaller details are lost."
        ),
    )

# =========================================================
# Tab 5 - Evaluate
# =========================================================
with tab5:
    render_section_header(
        "Evaluate what PCA keeps and what it loses",
        "Use explained variance and reconstruction to judge the trade-off.",
    )

    col1, col2 = st.columns([1.25, 1])

    with col1:
        fig = plot_explained_variance(pca)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "Explained variance",
            (
                "Explained variance tells us how much of the dataset's variation is captured by each component. "
                "If PC1 has a very high explained variance ratio, then keeping only PC1 may still preserve most of the information."
            ),
        )
        render_glass_container(
            "Variance summary",
            (
                f"- PC1 keeps <b>{pca.explained_variance_ratio_[0] * 100:.1f}%</b> of the variance<br>"
                f"- PC1 + PC2 keep <b>{np.sum(pca.explained_variance_ratio_) * 100:.1f}%</b> of the variance"
            ),
        )

    add_vertical_space()

    col3, col4 = st.columns([1.25, 1])

    with col3:
        fig = plot_reconstruction(X, X_reconstructed)
        st.pyplot(fig, use_container_width=True)

    with col4:
        st.metric("Reconstruction error", f"{reconstruction_error:.4f}")
        render_info_box(
            "Reconstruction intuition",
            (
                "This compares the original data with the approximation reconstructed using only PC1. "
                "A smaller reconstruction error means the 1-component representation still resembles the original data well."
            ),
        )

    add_vertical_space()

    render_takeaway_box(
        "Why standardisation matters",
        (
            "If features are on very different scales, PCA can be dominated by the larger-scale feature. "
            "Try the 'Different Feature Scales' dataset and toggle standardisation on and off."
        ),
    )

# =========================================================
# Tab 6 - Quiz
# =========================================================
with tab6:
    render_section_header(
        "Check your understanding",
        "Complete the quiz below to reinforce the main ideas from this topic.",
    )

    render_topic_quiz(TOPIC_NAME)

    add_vertical_space()

    render_takeaway_box(
        "Common misconceptions",
        (
            "PCA does not simply choose one original feature. "
            "It creates new axes that are combinations of the original features. "
            "It is also a linear method, so it may not capture strongly nonlinear structure."
        ),
    )
    
add_vertical_space(2)
st.markdown(
    "<div id='bt3017-chatbot' class='chat-anchor-space'></div>",
    unsafe_allow_html=True,
)
render_tutor_widget("Audio Features")