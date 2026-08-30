# Tutorial on False Data Injection Attacks in Power Systems

> **Audience:** Graduate students beginning research on cybersecurity of power sysetems, state estimation, and false-data injection (FDI) attacks
> > **Scope:** Synthetic 3-bus DC state-estimation experiments. This repository is intended for learning how FDI attacks are formulated, how model-consistent FDI attacks can evade conventional residual-based bad-data detection under idealized assumptions, and how residual-based detection is implemented. 
---

## 1. What will you learn?

This repository is a small teaching project for understanding the complete chain


```math
\boxed{
\text{Power-system model}
\rightarrow
\text{State estimation}
\rightarrow
\text{FDI generation}
\rightarrow
\text{Residual}
\rightarrow
\text{Bad-data detection}
}
```


After completing this small experiment, you should be able to:

1. explain the DC measurement model $z=Hx+e$;
2. derive the 3-bus measurement matrix $H$;
3. implement weighted least-squares (WLS) state estimation;
4. understand the residual $r=z-H\hat{x}$;
5. construct a simple single-measurement perturbation;
6. construct the classical model-consistent attack $a=Hc$;
7. prove why $a=Hc$ preserves the WLS residual in the ideal linear model;
8. implement a chi-square residual-based bad-data detector;
9. explain why ordinary data corruption is easy to detect but a model-consistent FDI can evade a residual-only detector under ideal assumptions.

---

## 2. Repository structure

```text
FDIA-tutorial/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_dc_state_estimation.ipynb
│   ├── 02_naive_fdi_attack.ipynb
│   ├── 03_stealthy_fdi_attack.ipynb
│   └── 04_bad_data_detection.ipynb
│
├── src/
│   ├── __init__.py
│   ├── grid_model.py
│   ├── state_estimator.py
│   ├── attack_generator.py
│   ├── metrics.py
│   └── demo.py
│
├── tests/
│   ├── test_estimator.py
│   └── test_attack.py
│
├── docs/
│   ├── theory.md
│   └── exercises.md
│
├── data/
│   └── generated/
│
└── figures/
```

The **Notebook files** are used for step-by-step teaching.  
The **src/** directory contains reusable Python implementations.  
The **tests/** directory verifies the main mathematical properties of the estimator and attack model.

---

# Part I. Power-system state-estimation model

## 3. Three-bus DC power-system model

We begin with a deliberately small 3-bus network:

```text
          Bus 1
         /     \
        /       \
     Bus 2 ---- Bus 3
```

The three transmission lines are


```math
(1,2),\qquad (1,3),\qquad (2,3).
```


The line susceptances are set to


```math
b_{12}=10,\qquad
b_{13}=5,\qquad
b_{23}=8.
```


Bus 1 is selected as the reference bus:


```math
\theta_1=0.
```


Therefore, only two voltage phase angles need to be estimated:


```math
\boxed{
x=
\begin{bmatrix}
\theta_2\\
\theta_3
\end{bmatrix}
}
```


and the number of states is


```math
n=2.
```


In this teaching example, the simulated true state is


```math
x_{\text{true}}
=
\begin{bmatrix}
-0.04\\
-0.06
\end{bmatrix}.
```


---

## 4. Measurement vector

Five active-power measurements are used:


```math
\boxed{
z=
\begin{bmatrix}
P_{12}\\
P_{13}\\
P_{23}\\
P_2\\
P_3
\end{bmatrix}
}
```


where

- $P_{12}$: active-power flow from bus 1 to bus 2;
- $P_{13}$: active-power flow from bus 1 to bus 3;
- $P_{23}$: active-power flow from bus 2 to bus 3;
- $P_2$: active-power injection at bus 2;
- $P_3$: active-power injection at bus 3.

Thus,


```math
m=5
```


measurements are used to estimate


```math
n=2
```


states.

---

## 5. Derivation of the measurement matrix $H$

Under the DC power-flow approximation,


```math
P_{ij}=b_{ij}(\theta_i-\theta_j).
```


### 5.1 Measurement $P_{12}$

Because $\theta_1=0$,


```math
P_{12}
=
10(\theta_1-\theta_2)
=
-10\theta_2.
```


Hence the first row of $H$ is


```math
[-10,\;0].
```


### 5.2 Measurement $P_{13}$


```math
P_{13}
=
5(\theta_1-\theta_3)
=
-5\theta_3,
```


so the second row is


```math
[0,\;-5].
```


### 5.3 Measurement $P_{23}$


```math
P_{23}
=
8(\theta_2-\theta_3)
=
8\theta_2-8\theta_3,
```


so the third row is


```math
[8,\;-8].
```


### 5.4 Injection $P_2$

Bus 2 is connected to buses 1 and 3:


```math
P_2=P_{21}+P_{23}.
```


Therefore,


```math
P_2
=
10(\theta_2-\theta_1)
+
8(\theta_2-\theta_3),
```


and since $\theta_1=0$,


```math
P_2
=
18\theta_2-8\theta_3.
```


Thus the fourth row is


```math
[18,\;-8].
```


### 5.5 Injection $P_3$

Similarly,


```math
P_3=P_{31}+P_{32},
```


so


```math
P_3
=
5(\theta_3-\theta_1)
+
8(\theta_3-\theta_2),
```


which gives


```math
P_3
=
-8\theta_2+13\theta_3.
```


Therefore, the fifth row is


```math
[-8,\;13].
```


Combining the five measurements,


```math
\boxed{
H=
\begin{bmatrix}
-10 & 0\\
0 & -5\\
8 & -8\\
18 & -8\\
-8 & 13
\end{bmatrix}
}
```


and the measurement model becomes


```math
\boxed{
z=Hx+e
}
```


where $e$ is the measurement noise.

---

## 6. Measurement noise

The teaching model assumes independent zero-mean Gaussian noise:


```math
e\sim\mathcal N(0,R).
```


For V0.1,


```math
\sigma=0.01
```


and


```math
\boxed{
R=\sigma^2 I.
}
```


Therefore, one synthetic measurement sample is generated by


```math
\boxed{
z=Hx_{\text{true}}+e.
}
```


Without noise,


```math
Hx_{\text{true}}
=
\begin{bmatrix}
0.40\\
0.30\\
0.16\\
-0.24\\
-0.46
\end{bmatrix}.
```


Using the fixed random seed in the Notebook gives a reproducible noisy sample.

---

# Part II. Weighted least-squares state estimation

## 7. WLS estimator

Because measurement noise prevents the five equations from being satisfied exactly by a single state vector, we estimate the state by minimizing the weighted residual:


```math
\boxed{
\hat{x}
=
\arg\min_x
(z-Hx)^T R^{-1}(z-Hx).
}
```


Define


```math
J(x)
=
(z-Hx)^TR^{-1}(z-Hx).
```


Setting the gradient to zero gives


```math
\frac{\partial J(x)}{\partial x}=0,
```


which yields the normal equation


```math
H^TR^{-1}H\hat{x}
=
H^TR^{-1}z.
```


If $H$ has full column rank,


```math
\boxed{
\hat{x}
=
(H^TR^{-1}H)^{-1}
H^TR^{-1}z.
}
```


The implementation in `src/state_estimator.py` uses a linear solver rather than explicitly inverting the gain matrix.

---

## 8. Residual

After estimating the state, the reconstructed measurement is


```math
H\hat{x}.
```


The residual is


```math
\boxed{
r=z-H\hat{x}.
}
```


Do not confuse the residual $r$ with the original measurement noise $e$:


```math
e=z-Hx_{\text{true}},
```


whereas


```math
r=z-H\hat{x}.
```


The estimator absorbs part of the measurement noise into the estimated state, so generally


```math
r\neq e.
```


---

# Part III. Residual-based bad-data detection

## 9. Chi-square residual statistic

The conventional residual-based test statistic is


```math
\boxed{
J=r^TR^{-1}r.
}
```


Under the assumptions of the linear Gaussian measurement model and a correctly specified covariance matrix, the normal residual statistic follows a chi-square distribution with


```math
\nu=m-n
```


degrees of freedom.

For this tutorial,


```math
m=5,\qquad n=2,
```


so


```math
\nu=3.
```


For a false-alarm significance level


```math
\alpha=0.05,
```


the detection threshold is


```math
\boxed{
\tau=
F^{-1}_{\chi^2_3}(0.95)
\approx7.815.
}
```


The detector uses


```math
\boxed{
J>\tau
\quad\Rightarrow\quad
\text{Alarm}.
}
```


A normal sample can still exceed the threshold with probability approximately $\alpha$. Therefore, “normal” does **not** mean that an alarm is mathematically impossible.

---

# Part IV. Naive false-data injection

## 10. Single-measurement perturbation

The first attack experiment intentionally uses a very simple perturbation:


```math
\boxed{
z^a=z+a
}
```


with


```math
a=
\begin{bmatrix}
0.1\\
0\\
0\\
0\\
0
\end{bmatrix}.
```


Only $P_{12}$ is changed.

This attack is intentionally naive: if $P_{12}$ truly changed because the system state changed, other measurements depending on $\theta_2$ should generally change as well. Changing only one measurement breaks the consistency imposed by $H$.

For the reproducible V0.1 example,


```math
J_{\text{normal}}\approx2.871,
```


whereas


```math
J_{\text{naive}}\approx71.198.
```


Thus,


```math
J_{\text{naive}}>\tau
```


and the residual-based detector raises an alarm.

---

# Part V. Structured FDI

## 11. Classical construction $a=Hc$

Instead of arbitrarily modifying one measurement, choose a desired state-estimation offset


```math
c=
\begin{bmatrix}
0.005\\
-0.004
\end{bmatrix}.
```


Construct the attack vector as


```math
\boxed{
a=Hc.
}
```


For the 3-bus model,


```math
a=
\begin{bmatrix}
-0.05\\
0.02\\
0.072\\
0.122\\
-0.092
\end{bmatrix}.
```


The attacked measurement is


```math
z^a=z+a=z+Hc.
```


Because


```math
z\approx Hx,
```


the attacked data have the model-consistent form


```math
z^a
=
H(x+c)+e.
```


Therefore, in the ideal linear WLS model,


```math
\boxed{
\hat{x}^a=\hat{x}+c.
}
```


In the V0.1 numerical experiment,


```math
\hat{x}^a-\hat{x}
=
\begin{bmatrix}
0.005\\
-0.004
\end{bmatrix},
```


exactly matching the selected state offset $c$ up to numerical precision.

---

## 12. Why does the structured attack preserve the residual?

The normal residual is


```math
r=z-H\hat{x}.
```


After the attack,


```math
r^a
=
z^a-H\hat{x}^a.
```


Using


```math
z^a=z+Hc
```


and


```math
\hat{x}^a=\hat{x}+c,
```


we obtain


```math
\begin{aligned}
r^a
&=
(z+Hc)-H(\hat{x}+c)\\
&=
z+Hc-H\hat{x}-Hc\\
&=
z-H\hat{x}\\
&=
r.
\end{aligned}
```


Hence,


```math
\boxed{
r^a=r.
}
```


Consequently,


```math
\boxed{
J^a
=
(r^a)^TR^{-1}r^a
=
r^TR^{-1}r
=
J.
}
```


The numerical experiment gives


```math
\|r^a-r\|_2
\approx1.5\times10^{-16},
```


which is numerical round-off error.

Thus,


```math
J_{\text{structured}}
\approx
J_{\text{normal}}
\approx2.871.
```


Since


```math
2.871<7.815,
```


the residual-only detector does not distinguish this attacked sample from the corresponding normal sample.

---

## 13. Linear-algebra interpretation

The WLS estimator can be written as


```math
\hat{x}=Kz,
```


where


```math
K=
(H^TR^{-1}H)^{-1}H^TR^{-1}.
```


The residual can therefore be expressed as


```math
r=(I-HK)z.
```


Define


```math
S=I-HK.
```


Then


```math
r=Sz.
```


Under an attack,


```math
r^a
=
S(z+a)
=
r+Sa.
```


If


```math
a=Hc,
```


then


```math
Sa=SHc.
```


For full-column-rank $H$,


```math
KH=I,
```


so


```math
SH=(I-HK)H=0.
```


Therefore,


```math
\boxed{
Sa=0
}
```


and


```math
\boxed{
r^a=r.
}
```


Geometrically, the attack lies in the column space of $H$:


```math
\boxed{
a\in\operatorname{Col}(H).
}
```


This is the key mathematical reason why a model-consistent attack can evade this ideal residual-only detector.

---

# Part VI. Experiments

## 14. Notebook 01 — DC State Estimation

Open:

```text
notebooks/01_dc_state_estimation.ipynb
```

Learning objectives:

- inspect $H$;
- inspect $x_{\text{true}}$;
- generate $z=Hx+e$;
- compute the WLS estimate;
- compare $\hat{x}$ with $x_{\text{true}}$;
- inspect the residual and $J$.

Expected reproducible values include approximately

```text
x_hat = [-0.03988588 -0.06093575]
J = 2.871034
```

---

## 15. Notebook 02 — Naive FDI Attack

Open:

```text
notebooks/02_naive_fdi_attack.ipynb
```

The attack is


```math
a=[0.1,\;0,\;0,\;0,\;0]^T.
```


Expected result:

```text
Normal J   = 2.871034
Attacked J = 71.198096
```

The naive perturbation is therefore detected by the residual test.

---

## 16. Notebook 03 — Structured FDI Attack

Open:

```text
notebooks/03_stealthy_fdi_attack.ipynb
```

Choose


```math
c=[0.005,\;-0.004]^T
```


and construct


```math
a=Hc.
```


Expected result:

```text
x_hat_attack - x_hat = [ 0.005 -0.004]
||r_attack - r_normal||_2 ≈ 1.5e-16
Normal J   ≈ 2.871034
Attacked J ≈ 2.871034
```

---

## 17. Notebook 04 — Bad-Data Detection

Open:

```text
notebooks/04_bad_data_detection.ipynb
```

The three cases are compared under the same chi-square detector:

| Case | $J$ | Alarm |
|---|---:|:---:|
| Normal | 2.871034 | False |
| Naive FDI | 71.198096 | True |
| Structured FDI | 2.871034 | False |

The result illustrates the central teaching point of V0.1:


```math
\boxed{
\text{A residual-only BDD can detect inconsistent corruption,}
}
```


but under the ideal model assumptions,


```math
\boxed{
a=Hc
}
```


can change the estimated state without changing the WLS residual.

---

# Part VII. How to run the tutorial

## 18. Recommended Python version

The tutorial has been tested with Python 3.12.

Check your Python version:

```bash
python --version
```

---

## 19. Create a virtual environment on Windows

From the directory containing the project:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

When activation succeeds, the command prompt begins with

```text
(.venv)
```

---

## 20. Install dependencies

Enter the repository root and run:

```bash
python -m pip install -r requirements.txt
```

The main dependencies are:

- NumPy;
- SciPy;
- Matplotlib;
- Jupyter;
- pytest.

Quick package check:

```bash
python -c "import numpy, scipy, matplotlib; print('Packages OK')"
```

---

## 21. Start Jupyter Notebook

From the repository root:

```bash
jupyter notebook
```

Open the notebooks in this order:

```text
01_dc_state_estimation.ipynb
        ↓
02_naive_fdi_attack.ipynb
        ↓
03_stealthy_fdi_attack.ipynb
        ↓
04_bad_data_detection.ipynb
```

Run a Notebook cell with:

```text
Shift + Enter
```

---

## 22. Run the complete command-line demo

From the repository root:

```bash
python -m src.demo
```

This runs the normal, naive-attack, and structured-attack cases in one command.

---

## 23. Run automated tests

```bash
pytest -q
```

Expected output:

```text
2 passed
```

The tests verify:

1. WLS exactly recovers the state for noiseless measurements;
2. the structured $a=Hc$ attack shifts the estimated state by $c$;
3. the structured attack preserves the residual and $J$ to numerical precision.

---

# Part VIII. Source-code map

## `src/grid_model.py`

Defines:

- the 3-bus measurement matrix $H$;
- the true state $x_{\text{true}}$;
- measurement names;
- covariance matrix $R$;
- synthetic measurement generation.

## `src/state_estimator.py`

Implements:

- WLS state estimation;
- residual computation;
- chi-square threshold;
- bad-data alarm.

## `src/attack_generator.py`

Implements:

- a transparent single-measurement perturbation;
- the model-consistent construction $a=Hc$.

## `src/demo.py`

Runs the complete V0.1 experiment from the command line.

## `tests/`

Contains automated checks of the estimator and the structured-attack property.

---

# Part IX. Important assumptions and limitations

The structured-attack result in this tutorial is an **idealized teaching result**. It should not be interpreted as “all FDI attacks are undetectable.”

The equality


```math
r^a=r
```


depends on assumptions including:

1. a linear DC measurement model;
2. exact knowledge of $H$;
3. consistent network topology and parameters;
4. the ability to modify the measurements required by $a=Hc$;
5. a conventional residual-only detector;
6. no additional trusted measurements, temporal models, or independent physics-based checks.

In practical research, these assumptions may be relaxed. Examples include:

- imperfect attacker knowledge $\tilde H\neq H$;
- limited measurement access;
- protected measurements;
- topology uncertainty;
- AC state estimation;
- PMU measurements;
- dynamic or temporal consistency checks;
- physics-informed detection;
- trusted-state reconstruction and cyber-resilient estimation.

These topics are intentionally left for later versions.

---

# Part X. Suggested questions

Students should be able to answer the following after V0.1:

1. Why is the state dimension two rather than three?
2. Why is $H$ a $5\times2$ matrix?
3. Why are the residual $r$ and measurement noise $e$ not identical?
4. Why does changing only $P_{12}$ create physical inconsistency?
5. What does $a\in\operatorname{Col}(H)$ mean?
6. Why does $a=Hc$ imply $\hat{x}^a-\hat{x}=c$?
7. Under which assumptions does $r^a=r$ hold?
8. Why does $\alpha=0.05$ not mean that a normal sample can never trigger an alarm?
9. What would happen if the attacker used an inaccurate matrix $\tilde H$?
10. What assumptions of this 3-bus model become unrealistic in a real control center?

Additional exercises are available in:

```text
docs/exercises.md
```

---

# References

1. Y. Liu, P. Ning, and M. K. Reiter, “False Data Injection Attacks against State Estimation in Electric Power Grids,” *Proceedings of the 16th ACM Conference on Computer and Communications Security (CCS)*, pp. 21–32, 2009. DOI: `10.1145/1653662.1653666`.

2. A. Abur and A. Gómez Expósito, *Power System State Estimation: Theory and Implementation*, CRC Press, 2004.

---

# Academic and safety note

This repository uses only a synthetic, offline 3-bus model and is intended for education and defensive cyber-security research. It does not provide interfaces to operational SCADA/EMS systems, field devices, or real infrastructure.

If you use or extend this repository for academic work, please cite the original literature relevant to the methods you use.

---

## License

See `LICENSE`.
