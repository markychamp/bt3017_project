def get_topic_context(page_key: str) -> str:
    contexts = {
        "PCA": """
PCA:
- PCA finds new axes that better match the spread of the data.
- PC1 is the direction of maximum variance.
- PC2 is perpendicular to PC1 and captures the next largest variance.
- Projection onto PC1 reduces dimensionality.
- Explained variance tells us how much information each component keeps.
- Standardisation matters when features are on different scales.
""",
        "Audio Features": """
Audio Features:
- Waveform shows amplitude over time.
- FFT shows which frequencies are present in a signal.
- Spectrogram shows how frequencies change over time.
- FFT alone loses timing information.
- Audio features help represent sound for machine learning tasks.
""",
        "Graph Learning": """
Graph Learning:
- A graph consists of nodes and edges.
- Adjacency matrix records which nodes are connected.
- Degree is the number of connections a node has.
- Graph Laplacian is L = D - A.
- Spectral clustering uses eigenvectors of the Laplacian.
- The Fiedler vector is the second eigenvector and helps reveal community structure.
""",
    }

    if page_key in contexts:
        return contexts[page_key]

    all_context = "\n\n".join(contexts.values())
    return all_context