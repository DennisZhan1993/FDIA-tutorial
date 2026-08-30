import numpy as np

from src.grid_model import build_three_bus_model
from src.state_estimator import wls_estimate


def test_wls_recovers_noiseless_state():
    model = build_three_bus_model()
    z = model.H @ model.x_true
    result = wls_estimate(z, model.H, model.R)
    assert np.allclose(result.x_hat, model.x_true, atol=1e-12)
    assert np.linalg.norm(result.residual) < 1e-12
