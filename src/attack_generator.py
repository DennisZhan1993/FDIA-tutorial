"""Attack generators for offline synthetic teaching experiments."""

import numpy as np


def naive_attack(
    z: np.ndarray,
    measurement_index: int = 0,
    magnitude: float = 0.10,
) -> tuple[np.ndarray, np.ndarray]:
    """Add a simple single-measurement perturbation.

    This is intentionally transparent for teaching purposes.
    """
    z = np.asarray(z, dtype=float)
    if not 0 <= measurement_index < z.size:
        raise IndexError("measurement_index is out of range.")

    a = np.zeros_like(z)
    a[measurement_index] = float(magnitude)
    return z + a, a


def structured_fdi_attack(
    z: np.ndarray,
    H: np.ndarray,
    c: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Construct the classical model-consistent teaching attack a = H c.

    In the ideal linear model with full model knowledge, this changes the
    estimated state while preserving the residual of the WLS estimator.
    """
    z = np.asarray(z, dtype=float)
    H = np.asarray(H, dtype=float)
    c = np.asarray(c, dtype=float)

    if H.shape[1] != c.size:
        raise ValueError("Length of c must equal the number of system states.")

    a = H @ c
    return z + a, a
