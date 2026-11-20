# Two-Storey Building Modal Analysis Using Python

## Overview
A 2 degree of freedom (2-DOF) lumped-mass shear building model is used to calculate the undamped free-vibration modal properties of a two-storey building. The Python program forms the mass and stiffness matrices, solves the eigenvalue problem, calculates natural frequencies and periods, and plots the two relative mode shapes.

**Scope note:** All input properties are illustrative assumed values, not measurements from a real building. This is an educational modal-analysis exercise, not a structural design or safety assessment.

## Model inputs

| Parameter | Meaning | Value |
| m1 | First floor mass | 20,000 kg |
| m2 | Second floor mass | 15,000 kg |
| k1 | First storey lateral stiffness | 20,000,000 N/m |
| k2 | Second storey lateral stiffness | 15,000,000 N/m |

The degrees of freedom are the horizontal floor displacements, u1 and u2.

## Mathematical formulation

Mass matrix:

M = [[m1, 0], [0, m2]]

Stiffness matrix:

K = [[k1 + k2, -k2], [-k2, k2]]

Undamped free-vibration equation:

M u_ddot + K u = 0

Assuming harmonic motion gives the generalised eigenvalue problem:

(K - omega^2 M) phi = 0

The eigenvalues are lambda = omega^2. The program calculates:
- circular natural frequency, omega = sqrt(lambda), in rad/s;
- natural frequency, f = omega/(2 pi), in Hz;
- natural period, T = 1/f, in seconds;
- mode shapes, normalised so the second-floor component is 1.

## Expected results

| Property | Mode 1 | Mode 2 |
| Eigenvalue (s^-2) | 431.27 | 2318.73 |
| Circular frequency (rad/s) | 20.77 | 48.15 |
| Natural frequency (Hz) | 3.305 | 7.664 |
| Natural period (s) | 0.303 | 0.130 |
| Floor 1 relative displacement | 0.569 | -1.319 |
| Floor 2 relative displacement | 1.000 | 1.000 |

Mode 1 has both floors moving in the same direction, with greater relative movement at the second floor. Mode 2 has the floors moving in opposite directions. The overall sign of a mode shape is arbitrary.

## Requirements
- Python 3.9+
- NumPy
- Matplotlib

## Run the project

From the project root:

```bash
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
py src/modal_analysis.py
```

The script creates `results/mode_shapes.png` and `results/modal_results.csv`.

 Assumptions and limitations
1. Fixed foundation.
2. Two lateral degrees of freedom and lumped floor masses.
3. Linear elastic, constant storey stiffnesses.
4. Undamped free vibration; no external excitation or earthquake input.
5. Floor rotation, torsion, distributed mass and 3D behaviour are neglected.
6. Parameters are assumed for demonstration; there is no experimental calibration or real-building validation.

This project demonstrates basic matrix formulation and modal analysis. It does not perform seismic response-history analysis, structural design, or code-compliance checking.

## Tools
Python, NumPy and Matplotlib.

