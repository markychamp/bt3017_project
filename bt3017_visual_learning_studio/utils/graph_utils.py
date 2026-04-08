import numpy as np


def get_sample_graph(graph_name: str) -> tuple[np.ndarray, dict[int, tuple[float, float]], str]:
    """
    Return adjacency matrix, node positions, and a short description
    for a predefined sample graph.
    """
    if graph_name == "Two Communities":
        adjacency = np.array([
            [0, 1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 1, 1, 0],
        ])
        positions = {
            0: (0.0, 1.0),
            1: (1.0, 1.2),
            2: (0.8, 0.2),
            3: (2.2, 0.2),
            4: (3.0, 1.2),
            5: (3.0, 0.0),
        }
        description = (
            "This graph has two tightly connected groups with a weaker bridge between them. "
            "It is useful for building intuition about communities and spectral clustering."
        )
        return adjacency, positions, description

    if graph_name == "Chain Graph":
        adjacency = np.array([
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0],
        ])
        positions = {
            0: (0.0, 0.0),
            1: (1.0, 0.0),
            2: (2.0, 0.0),
            3: (3.0, 0.0),
            4: (4.0, 0.0),
            5: (5.0, 0.0),
        }
        description = (
            "This is a simple chain where each middle node connects to two neighbours. "
            "It is useful for understanding local connectivity and node degree."
        )
        return adjacency, positions, description

    if graph_name == "Star Graph":
        adjacency = np.array([
            [0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
        ])
        positions = {
            0: (0.0, 0.0),
            1: (-1.2, 1.0),
            2: (1.2, 1.0),
            3: (-1.2, -1.0),
            4: (1.2, -1.0),
            5: (0.0, 1.6),
        }
        description = (
            "This graph has one central hub connected to all other nodes. "
            "It is useful for showing how degree can vary greatly across nodes."
        )
        return adjacency, positions, description

    raise ValueError(f"Unknown graph name: {graph_name}")


def compute_degree_matrix(adjacency: np.ndarray) -> np.ndarray:
    """Compute the diagonal degree matrix."""
    degrees = adjacency.sum(axis=1)
    return np.diag(degrees)


def compute_laplacian(adjacency: np.ndarray) -> np.ndarray:
    """Compute the unnormalised graph Laplacian L = D - A."""
    degree = compute_degree_matrix(adjacency)
    return degree - adjacency


def compute_node_degrees(adjacency: np.ndarray) -> np.ndarray:
    """Return degree of each node."""
    return adjacency.sum(axis=1)


def compute_laplacian_eigendecomposition(laplacian: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return sorted eigenvalues and eigenvectors of the Laplacian."""
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
    order = np.argsort(eigenvalues)
    return eigenvalues[order], eigenvectors[:, order]


def get_fiedler_vector(eigenvectors: np.ndarray) -> np.ndarray:
    """
    Return the second eigenvector (Fiedler vector),
    which is commonly used in spectral clustering intuition.
    """
    if eigenvectors.shape[1] < 2:
        return eigenvectors[:, 0]
    return eigenvectors[:, 1]


def get_simple_spectral_partition(fiedler_vector: np.ndarray) -> np.ndarray:
    """
    Partition nodes into two groups using the sign of the Fiedler vector.
    """
    return (fiedler_vector >= 0).astype(int)