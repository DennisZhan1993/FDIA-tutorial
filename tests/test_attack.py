import numpy as np

from src.grid_model import build_three_bus_model, generate_measurement
from src.state_estimator import wls_estimate
from src.attack_generator import structured_fdi_attack


def test_structured_attack_preserves_residual():
    rng = np.random.default_rng(7)
    model = build_three_bus_model()

    z, _ = generate_measurement(model, rng)
    normal = wls_estimate(z, model.H, model.R)

    c = np.array([0.005, -0.004])
    z_attack, _ = structured_fdi_attack(z, model.H, c)
    attacked = wls_estimate(z_attack, model.H, model.R)

    assert np.allclose(attacked.residual, normal.residual, atol=1e-10)
    assert np.allclose(attacked.x_hat - normal.x_hat, c, atol=1e-10)
    assert np.isclose(attacked.J, normal.J, atol=1e-10)
