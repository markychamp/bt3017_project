import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from components.tutor_widget import render_tutor_widget
from components.bootstrap import setup_page
from components.quiz import render_topic_quiz
from components.chat_jump import render_floating_chat_jump
from components.ui import (
    add_vertical_space,
    render_glass_container,
    render_info_box,
    render_page_header,
    render_section_header,
    render_takeaway_box,
)
from utils.graph_utils import (
    compute_degree_matrix,
    compute_laplacian,
    compute_laplacian_eigendecomposition,
    compute_node_degrees,
    get_fiedler_vector,
    get_sample_graph,
    get_simple_spectral_partition,
)

setup_page("Graph Learning • BT3017 Visual Learning Studio")

TOPIC_NAME = "Graph Learning"


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


def plot_graph(adjacency: np.ndarray, positions: dict[int, tuple[float, float]], node_colors=None, title="Graph"):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor("#120E1D")
    ax.set_facecolor("#120E1D")

    num_nodes = adjacency.shape[0]

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if adjacency[i, j] == 1:
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                ax.plot([x1, x2], [y1, y2], linewidth=2.2, color="#D085FF", alpha=0.9)

    for i in range(num_nodes):
        x, y = positions[i]
        color = "#FF6FEA" if node_colors is None else node_colors[i]
        ax.scatter(x, y, s=700, c=[color], edgecolors="#FFF4FD", linewidths=1.2)
        ax.text(x, y, str(i), ha="center", va="center", color="white", weight="bold")

    ax.set_title(title, color="#FFF4FD")
    ax.axis("off")
    return fig


def plot_matrix(matrix: np.ndarray, title: str, cmap: str = "magma"):
    fig, ax = plt.subplots(figsize=(5, 4.2))
    fig.patch.set_facecolor("#120E1D")
    ax.set_facecolor("#120E1D")

    im = ax.imshow(matrix, cmap=cmap)
    ax.set_title(title, color="#FFF4FD")
    ax.tick_params(colors="#E8DFFB")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, f"{matrix[i, j]:.0f}", ha="center", va="center", color="white")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.label.set_color("#F3EAFE")
    cbar.ax.tick_params(colors="#E8DFFB")
    cbar.outline.set_edgecolor("#6B3FA0")

    for spine in ax.spines.values():
        spine.set_color("#6B3FA0")

    return fig


def plot_eigenvalues(eigenvalues: np.ndarray):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(eigenvalues))
    ax.plot(x, eigenvalues, marker="o", linewidth=2, color="#00E7FF")
    ax.set_title("Laplacian Eigenvalues")
    ax.set_xlabel("Eigenvalue Index")
    ax.set_ylabel("Value")
    style_dark_axes(fig, ax)
    return fig


def plot_fiedler_vector(fiedler_vector: np.ndarray):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(fiedler_vector))
    ax.bar(x, fiedler_vector, alpha=0.9, color="#FF6FEA")
    ax.axhline(0, linestyle="--", linewidth=1, color="#E8DFFB")
    ax.set_title("Fiedler Vector (Second Eigenvector)")
    ax.set_xlabel("Node Index")
    ax.set_ylabel("Value")
    style_dark_axes(fig, ax)
    return fig


# =========================================================
# Page header and teaching intro
# =========================================================
render_page_header(
    title="Graph Learning",
    subtitle=(
        "Learn how connected data can be represented using graphs, matrices, and the graph Laplacian, "
        "and build intuition for spectral clustering."
    ),
    icon="🕸️",
)
render_floating_chat_jump()
render_info_box(
    "Learning objectives",
    (
        "By the end of this page, you should be able to explain what <span class='accent-text'>nodes</span> "
        "and <span class='accent-text'>edges</span> represent, interpret the <b>adjacency matrix</b> and "
        "<b>degree matrix</b>, describe the <b>graph Laplacian</b>, and understand the basic intuition behind "
        "<i>spectral clustering</i>."
    ),
)

render_section_header(
    "What is graph learning?",
    "A visual and intuitive introduction before the interactive exploration."
)

render_glass_container(
    "Graph learning in one sentence",
    (
        "Graph learning studies data where the <span class='accent-text'>relationships between items</span> "
        "are just as important as the items themselves."
    ),
)

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

col_intro1, col_intro2 = st.columns([1.15, 1])

with col_intro1:
    render_info_box(
        "Core intuition",
        (
            "Some data is best understood not as separate rows in a table, but as connected entities. "
            "Examples include <b>social networks</b>, <b>transport routes</b>, <b>website links</b>, "
            "and <b>molecular structures</b>. Graph learning helps us analyse data where these connections matter."
        ),
    )

    render_glass_container(
        "What graph learning is really doing",
        (
            "Instead of focusing only on the features of individual items, graph learning also uses the "
            "<span class='accent-text'>structure of their connections</span>. This helps reveal patterns such as "
            "communities, hubs, and influence across the network."
        ),
    )

with col_intro2:
    render_takeaway_box(
        "Key intuition",
        (
            "Graphs are useful when the <span class='inline-emphasis'>connections between items</span> "
            "carry important information."
        ),
    )

    render_glass_container(
        "Important terms",
        """
        <div class='term-block'>
            <div class='term-title'>Node</div>
            <div class='soft-text'>An entity, such as a person, station, or webpage.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>Edge</div>
            <div class='soft-text'>A connection between two nodes.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>Adjacency Matrix</div>
            <div class='soft-text'>Records which pairs of nodes are connected.</div>
        </div>

        <div class='term-block'>
            <div class='term-title'>Degree</div>
            <div class='soft-text'>The number of connections a node has.</div>
        </div>

        <div class='term-block' style='margin-bottom:0;'>
            <div class='term-title'>Laplacian</div>
            <div class='soft-text'>A matrix that captures graph structure in a useful mathematical form.</div>
        </div>
        """,
    )

add_vertical_space()

render_section_header(
    "Why do we use graph learning?",
    "Graph learning helps when ordinary tables do not fully capture the structure of the data."
)

col_why1, col_why2 = st.columns(2)

with col_why1:
    render_glass_container(
        "What problem it solves",
        (
            "In many datasets, the most important pattern is not just in the individual values, but in "
            "<b>how the entities are connected</b>. Graph learning helps us model those relationships directly."
        ),
    )

with col_why2:
    render_glass_container(
        "Why it matters in machine learning",
        (
            "Graphs are useful for problems such as <b>community detection</b>, <b>recommendation systems</b>, "
            "<b>link prediction</b>, and <b>network analysis</b>. They provide a richer representation of structured data."
        ),
    )

add_vertical_space()

st.markdown(
    """
    <div class="example-box">
        <div class="example-label">Simple example</div>
        <div style="line-height:1.8; color:#D6E1FB;">
            If two groups of nodes are strongly connected internally but weakly connected to each other,
            the graph structure suggests that they may form
            <span class="accent-text">two different communities</span>.
        </div>
        <div style="margin-top:0.8rem;">
            <span class="highlight-pill">connected structure</span>
            <span class="highlight-pill">communities</span>
            <span class="highlight-pill">spectral intuition</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Sidebar controls
# =========================================================
st.sidebar.markdown("## 🕸️ Graph Controls")

graph_name = st.sidebar.selectbox(
    "Choose a graph example",
    ["Two Communities", "Chain Graph", "Star Graph"],
)

show_partition = st.sidebar.checkbox("Show simple spectral partition", value=True)

adjacency, positions, graph_description = get_sample_graph(graph_name)
degree = compute_degree_matrix(adjacency)
laplacian = compute_laplacian(adjacency)
node_degrees = compute_node_degrees(adjacency)
eigenvalues, eigenvectors = compute_laplacian_eigendecomposition(laplacian)
fiedler_vector = get_fiedler_vector(eigenvectors)
partition = get_simple_spectral_partition(fiedler_vector)

if show_partition:
    node_colors = ["#7B5CFF" if label == 0 else "#FF6FEA" for label in partition]
else:
    node_colors = ["#FF6FEA"] * adjacency.shape[0]
add_vertical_space()

# =========================================================
# Lesson tabs
# =========================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "1. Graph View",
        "2. Matrices",
        "3. Laplacian",
        "4. Spectral Intuition",
        "5. Quiz",
    ]
)

# =========================================================
# Tab 1
# =========================================================
with tab1:
    render_section_header(
        "See the graph structure",
        "Start by looking directly at the nodes and edges."
    )

    col1, col2 = st.columns([1.35, 1])

    with col1:
        fig = plot_graph(adjacency, positions, node_colors=node_colors, title=graph_name)
        st.pyplot(fig, use_container_width=True)

    with col2:
        render_info_box(
            "Graph selected",
            graph_description,
        )

        render_glass_container(
            "What to notice",
            """
            - Which nodes seem tightly connected?<br>
            - Are there hubs or central nodes?<br>
            - Do you see one group or multiple communities?
            """,
        )

# =========================================================
# Tab 2
# =========================================================
with tab2:
    render_section_header(
        "Matrix representations",
        "Graphs can be converted into matrices so that algorithms can work with them."
    )

    col1, col2 = st.columns(2)

    with col1:
        fig_adj = plot_matrix(adjacency, "Adjacency Matrix", cmap="magma")
        st.pyplot(fig_adj, use_container_width=True)

    with col2:
        fig_deg = plot_matrix(degree, "Degree Matrix", cmap="plasma")
        st.pyplot(fig_deg, use_container_width=True)

    render_info_box(
        "How to read these matrices",
        (
            "The <b>adjacency matrix</b> tells us which pairs of nodes are connected. "
            "The <b>degree matrix</b> places each node's degree on the diagonal."
        ),
    )

    degree_html = "<br>".join([f"- Node {idx}: degree {int(deg)}" for idx, deg in enumerate(node_degrees)])
    render_glass_container(
        "Node degrees",
        degree_html,
    )

# =========================================================
# Tab 3
# =========================================================
with tab3:
    render_section_header(
        "The graph Laplacian",
        "The Laplacian is one of the most important matrices in graph learning."
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        fig_lap = plot_matrix(laplacian, "Graph Laplacian (L = D - A)", cmap="inferno")
        st.pyplot(fig_lap, use_container_width=True)

    with col2:
        render_info_box(
            "Why the Laplacian matters",
            (
                "The Laplacian combines <b>node degree information</b> and <b>connectivity information</b>. "
                "It is widely used in <i>spectral clustering</i> and graph-based learning methods."
            ),
        )

        render_glass_container(
            "Simple formula",
            """
            - <b>L = D - A</b><br>
            - <b>D</b> = degree matrix<br>
            - <b>A</b> = adjacency matrix
            """,
        )

    add_vertical_space()

    render_takeaway_box(
        "Main idea",
        (
            "The Laplacian captures how each node differs from its neighbours, which makes it useful for "
            "understanding <span class='accent-text'>structure</span> and <span class='accent-text'>communities</span>."
        ),
    )

# =========================================================
# Tab 4
# =========================================================
with tab4:
    render_section_header(
        "Spectral intuition",
        "Eigenvalues and eigenvectors of the Laplacian can reveal community structure."
    )

    col1, col2 = st.columns(2)

    with col1:
        fig_eig = plot_eigenvalues(eigenvalues)
        st.pyplot(fig_eig, use_container_width=True)

    with col2:
        fig_fiedler = plot_fiedler_vector(fiedler_vector)
        st.pyplot(fig_fiedler, use_container_width=True)

    render_info_box(
        "What the Fiedler vector tells us",
        (
            "The <b>second eigenvector</b> of the Laplacian is often used in spectral clustering intuition. "
            "Nodes with similar values in this vector often belong to the same group."
        ),
    )

    if show_partition:
        partition_html = "<br>".join([f"- Node {idx}: Group {int(label)}" for idx, label in enumerate(partition)])
        render_glass_container(
            "Simple partition based on Fiedler vector sign",
            partition_html,
        )

    render_takeaway_box(
        "Key idea",
        (
            "Spectral clustering uses eigenvectors of the Laplacian to find structure that may not be obvious "
            "from raw coordinates alone."
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
            "The adjacency matrix does not tell you everything by itself. The degree matrix and Laplacian add "
            "important structural information. Spectral clustering does not simply draw circles around nodes — "
            "it uses <b>eigenvectors of the Laplacian</b>."
        ),
    )
add_vertical_space(2)
st.markdown(
    "<div id='bt3017-chatbot' class='chat-anchor-space'></div>",
    unsafe_allow_html=True,
)
render_tutor_widget("Audio Features")