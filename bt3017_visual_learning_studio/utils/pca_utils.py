import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def apply_standardisation(X: np.ndarray, standardise: bool) -> np.ndarray:
    """Optionally standardise the dataset."""
    if standardise:
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    return X.copy()


def fit_pca(X: np.ndarray) -> tuple[PCA, np.ndarray]:
    """Fit PCA and return the fitted model and transformed data."""
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    return pca, X_pca


def project_onto_pc1(X: np.ndarray, pca: PCA) -> tuple[np.ndarray, np.ndarray]:
    """Project each point onto PC1 and return projected points and PC1 scores."""
    mean = pca.mean_
    pc1 = pca.components_[0]

    centered = X - mean
    scores_pc1 = centered @ pc1
    projected = mean + np.outer(scores_pc1, pc1)

    return projected, scores_pc1


def reconstruct_from_pc1(X_pca: np.ndarray, pca: PCA) -> np.ndarray:
    """Reconstruct original-space points using only the first principal component."""
    X_pc1_only = np.zeros_like(X_pca)
    X_pc1_only[:, 0] = X_pca[:, 0]
    return pca.inverse_transform(X_pc1_only)


def compute_reconstruction_error(X: np.ndarray, X_reconstructed: np.ndarray) -> float:
    """Compute mean squared reconstruction error."""
    return float(np.mean((X - X_reconstructed) ** 2))


def get_axis_limits(X: np.ndarray, margin: float = 1.2) -> tuple[float, float, float, float]:
    """Get clean axis limits for 2D plots."""
    x_min, y_min = X.min(axis=0)
    x_max, y_max = X.max(axis=0)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    x_range = (x_max - x_min) * margin
    y_range = (y_max - y_min) * margin
    max_range = max(x_range, y_range)

    return (
        x_center - max_range / 2,
        x_center + max_range / 2,
        y_center - max_range / 2,
        y_center + max_range / 2,
    )


def get_pc1_angle_degrees(pca: PCA) -> float:
    """Return the angle of PC1 in degrees."""
    return float(np.degrees(np.arctan2(pca.components_[0, 1], pca.components_[0, 0])))