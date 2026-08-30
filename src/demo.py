"""Command-line demo for the complete V0.1 experiment."""

import numpy as np

from .grid_model import build_three_bus_model, generate_measurement
from .state_estimator import wls_estimate, chi_square_threshold, bad_data_alarm
from .attack_generator import naive_attack, structured_fdi_attack


def main() -> None:
    rng = np.random.default_rng(42)
    model = build_three_bus_model(sigma=0.01)

    z, _ = generate_measurement(model, rng)
    normal = wls_estimate(z, model.H, model.R)

    threshold = chi_square_threshold(
        m=model.H.shape[0],
        n=model.H.shape[1],
        false_alarm_rate=0.05,
    )

    z_naive, a_naive = naive_attack(z, measurement_index=0, magnitude=0.10)
    naive = wls_estimate(z_naive, model.H, model.R)

    c = np.array([0.005, -0.004])
    z_structured, a_structured = structured_fdi_attack(z, model.H, c)
    structured = wls_estimate(z_structured, model.H, model.R)

    print("=== Normal ===")
    print("x_hat:", normal.x_hat)
    print("J:", normal.J)
    print("Alarm:", bad_data_alarm(normal.J, threshold))

    print("\n=== Naive attack ===")
    print("a:", a_naive)
    print("x_hat:", naive.x_hat)
    print("J:", naive.J)
    print("Alarm:", bad_data_alarm(naive.J, threshold))

    print("\n=== Structured FDI ===")
    print("a = Hc:", a_structured)
    print("x_hat:", structured.x_hat)
    print("J:", structured.J)
    print("Alarm:", bad_data_alarm(structured.J, threshold))

    print("\nResidual invariance check")
    print("||r_structured - r_normal||_2 =",
          np.linalg.norm(structured.residual - normal.residual))


if __name__ == "__main__":
    main()
