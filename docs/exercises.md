# Exercises

## Exercise 1 — Verify the measurement matrix

Derive every row of the 3-bus measurement matrix from the DC power-flow
equations.

## Exercise 2 — Change the measurement noise

Try \(\sigma=0.005, 0.01, 0.02, 0.05\). Explain how the residual statistic and
chi-square alarm behavior change.

## Exercise 3 — Change the naive attack location

Apply the same perturbation to P12, P13, P23, P2, and P3 separately. Which
measurement locations are easier to detect in this small system?

## Exercise 4 — Verify residual invariance

Choose several vectors \(c\), construct \(a=Hc\), and numerically verify

\[
\|r^a-r\|_2 \approx 0.
\]

## Exercise 5 — Model mismatch

Let the attacker construct an approximate matrix

\[
\tilde{H}=H+\Delta H
\]

and use \(a=\tilde{H}c\). Study how model mismatch changes the residual.
