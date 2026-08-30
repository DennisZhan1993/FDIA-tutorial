# Theory Notes

## 1. Linear DC state estimation

We use

\[
z = Hx + e,
\]

where \(x=[\theta_2,\theta_3]^T\), bus 1 is the reference, and \(e\) is
Gaussian measurement noise.

The weighted least-squares estimate is

\[
\hat{x}=(H^T R^{-1}H)^{-1}H^TR^{-1}z.
\]

## 2. Residual-based bad-data detection

Define

\[
r=z-H\hat{x},
\qquad
J=r^TR^{-1}r.
\]

With standard assumptions, \(J\) can be compared with a chi-square threshold.

## 3. Naive measurement perturbation

A transparent perturbation has the form

\[
z^a=z+a.
\]

If \(a\) does not respect the measurement-model structure, it often causes
the residual statistic to increase.

## 4. Model-consistent teaching attack

For the classical linear-model construction

\[
a=Hc,
\]

the attacked measurement is

\[
z^a=z+Hc.
\]

Then, ideally,

\[
\hat{x}^a=\hat{x}+c
\]

and

\[
r^a=r.
\]

This is the key teaching result of the repository.

## Scope

All experiments in this repository are synthetic and offline. They are
intended for classroom learning, state-estimation research, and defensive
algorithm evaluation.
