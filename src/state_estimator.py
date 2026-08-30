"""Weighted least-squares state estimator and residual-based bad-data detector."""

from dataclasses import dataclass
import numpy as np
from scipy.stats import chi2


@dataclass(frozen=True)
class EstimationResult:
    x_hat: np.ndarray
    residual: np.ndarray
    J: float


def wls_estimate(z: np.ndarray, H: np.ndarray, R: np.ndarray) -> EstimationResult:
    """Compute the weighted least-squares (WLS) state estimate.

    x_hat = (H^T R^{-1} H)^{-1} H^T R^{-1} z

    The implementation avoids explicit inversion of the gain matrix.
    """
    z = np.asarray(z, dtype=float)
    H = np.asarray(H, dtype=float)
    R = np.asarray(R, dtype=float)

    W = np.linalg.inv(R)
    G = H.T @ W @ H
    rhs = H.T @ W @ z

    x_hat = np.linalg.solve(G, rhs)
    residual = z - H @ x_hat
    J = float(residual.T @ W @ residual)

    return EstimationResult(x_hat=x_hat, residual=residual, J=J)


def chi_square_threshold(m: int, n: int, false_alarm_rate: float = 0.05) -> float:
    """Return the chi-square threshold for the residual test.

    Degrees of freedom = number of measurements - number of states.
    """
    if not (0.0 < false_alarm_rate < 1.0):
        raise ValueError("false_alarm_rate must be between 0 and 1.")
    dof = m - n
    if dof <= 0:
        raise ValueError("Need more measurements than states for this detector.")
    return float(chi2.ppf(1.0 - false_alarm_rate, dof))


def bad_data_alarm(J: float, threshold: float) -> bool:
    """Return True when the residual statistic exceeds the threshold."""
    return bool(J > threshold)
