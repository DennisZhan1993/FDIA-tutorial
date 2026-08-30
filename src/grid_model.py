"""Simple three-bus DC measurement model for teaching state estimation and FDI."""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ThreeBusModel:
    """Container for the 3-bus DC measurement model."""

    H: np.ndarray
    x_true: np.ndarray
    measurement_names: tuple[str, ...]
    sigma: float

    @property
    def R(self) -> np.ndarray:
        """Measurement-noise covariance matrix."""
        return (self.sigma ** 2) * np.eye(self.H.shape[0])


def build_three_bus_model(sigma: float = 0.01) -> ThreeBusModel:
    """Return the teaching 3-bus DC measurement model.

    State:
        x = [theta_2, theta_3]^T, with theta_1 = 0 as the reference.

    Measurements:
        z = [P12, P13, P23, P2, P3]^T.

    Line susceptances:
        b12 = 10, b13 = 5, b23 = 8.
    """
    H = np.array(
        [
            [-10.0, 0.0],   # P12 = b12 * (theta1 - theta2)
            [0.0, -5.0],    # P13 = b13 * (theta1 - theta3)
            [8.0, -8.0],    # P23 = b23 * (theta2 - theta3)
            [18.0, -8.0],   # P2  = b12*(theta2-theta1)+b23*(theta2-theta3)
            [-8.0, 13.0],   # P3  = b13*(theta3-theta1)+b23*(theta3-theta2)
        ],
        dtype=float,
    )

    x_true = np.array([-0.04, -0.06], dtype=float)

    return ThreeBusModel(
        H=H,
        x_true=x_true,
        measurement_names=("P12", "P13", "P23", "P2", "P3"),
        sigma=float(sigma),
    )


def generate_measurement(
    model: ThreeBusModel,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate one noisy measurement vector z = H x + e."""
    if rng is None:
        rng = np.random.default_rng()
    noise = rng.normal(loc=0.0, scale=model.sigma, size=model.H.shape[0])
    z = model.H @ model.x_true + noise
    return z, noise
