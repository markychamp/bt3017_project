import numpy as np
from sklearn.datasets import load_iris


PCA_DATASET_OPTIONS = [
    "Elongated Diagonal Cloud",
    "Circular Cloud",
    "Clustered Correlated Data",
    "Different Feature Scales",
    "Iris (2 Features)",
]


def generate_elongated_diagonal_cloud(n_samples: int = 120, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    mean = [0, 0]
    cov = [[3.0, 2.4], [2.4, 2.2]]
    return rng.multivariate_normal(mean, cov, size=n_samples)


def generate_circular_cloud(n_samples: int = 120, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(0, 1, size=(n_samples, 2))


def generate_clustered_correlated_data(n_samples: int = 120, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)

    cluster_1 = rng.multivariate_normal(
        mean=[-3, -2],
        cov=[[0.8, 0.5], [0.5, 0.8]],
        size=n_samples // 2,
    )
    cluster_2 = rng.multivariate_normal(
        mean=[3, 2],
        cov=[[1.0, 0.7], [0.7, 1.0]],
        size=n_samples - n_samples // 2,
    )
    return np.vstack([cluster_1, cluster_2])


def generate_different_feature_scales(n_samples: int = 120, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x1 = rng.normal(0, 1.2, size=n_samples)
    x2 = 8 * x1 + rng.normal(0, 8, size=n_samples)
    return np.column_stack([x1, x2])


def load_iris_two_features() -> np.ndarray:
    iris = load_iris()
    return iris.data[:, [0, 2]]


def get_pca_dataset(name: str, n_samples: int = 120, seed: int = 42) -> np.ndarray:
    if name == "Elongated Diagonal Cloud":
        return generate_elongated_diagonal_cloud(n_samples=n_samples, seed=seed)
    if name == "Circular Cloud":
        return generate_circular_cloud(n_samples=n_samples, seed=seed)
    if name == "Clustered Correlated Data":
        return generate_clustered_correlated_data(n_samples=n_samples, seed=seed)
    if name == "Different Feature Scales":
        return generate_different_feature_scales(n_samples=n_samples, seed=seed)
    if name == "Iris (2 Features)":
        return load_iris_two_features()

    raise ValueError(f"Unknown PCA dataset: {name}")


def get_pca_dataset_metadata(name: str) -> dict:
    metadata = {
        "Elongated Diagonal Cloud": {
            "title": "Elongated Diagonal Cloud",
            "brief": "A synthetic 2D dataset stretched along a diagonal direction.",
            "why_useful": "This is the clearest dataset for showing how PCA identifies the direction of maximum variance.",
            "what_to_observe": [
                "The points form a long tilted cloud.",
                "PC1 should align closely with the diagonal spread.",
                "PC1 usually explains most of the variance here."
            ],
        },
        "Circular Cloud": {
            "title": "Circular Cloud",
            "brief": "A synthetic dataset with roughly equal spread in all directions.",
            "why_useful": "This shows a case where PCA is less dramatic because there is no strongly dominant direction.",
            "what_to_observe": [
                "The data looks more evenly spread.",
                "PC1 is still chosen, but not as strongly as in elongated data.",
                "Explained variance is likely more balanced between PC1 and PC2."
            ],
        },
        "Clustered Correlated Data": {
            "title": "Clustered Correlated Data",
            "brief": "Two correlated clusters spread across a tilted overall direction.",
            "why_useful": "This helps show that PCA captures overall structure even when the data contains multiple groups.",
            "what_to_observe": [
                "There are two visible clusters.",
                "The whole dataset still has a dominant overall direction.",
                "PCA captures the main global spread, not cluster labels."
            ],
        },
        "Different Feature Scales": {
            "title": "Different Feature Scales",
            "brief": "A synthetic dataset where one feature has a much larger numerical scale than the other.",
            "why_useful": "This is ideal for demonstrating why standardisation matters before PCA.",
            "what_to_observe": [
                "Without standardisation, one feature can dominate PCA.",
                "With standardisation, PCA becomes more balanced.",
                "Try toggling standardisation on and off."
            ],
        },
        "Iris (2 Features)": {
            "title": "Iris (2 Features)",
            "brief": "A real dataset using two features from the Iris flower dataset.",
            "why_useful": "This gives a simple real-world example of PCA on tabular data instead of only synthetic clouds.",
            "what_to_observe": [
                "The points come from real measured data.",
                "PCA still finds the dominant direction of spread.",
                "This helps connect PCA to practical datasets."
            ],
        },
    }

    if name not in metadata:
        raise ValueError(f"Unknown PCA dataset metadata: {name}")

    return metadata[name]