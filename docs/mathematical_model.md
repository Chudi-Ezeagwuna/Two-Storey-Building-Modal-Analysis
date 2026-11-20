# Mathematical Model and Methodology

## Physical idealisation
The structure is represented as a two-storey shear building with a fixed base. Each floor is represented by a lumped mass, and each storey by a lateral stiffness. The two degrees of freedom are the horizontal floor displacements, u1 and u2.

Illustrative assumed values:
- m1 = 20,000 kg
- m2 = 15,000 kg
- k1 = 20,000,000 N/m
- k2 = 15,000,000 N/m

## Mass matrix
M = [[m1, 0], [0, m2]]

## Stiffness matrix
K = [[k1 + k2, -k2], [-k2, k2]]

The negative off-diagonal terms represent coupling between the floor displacements.

## Equation of motion
For undamped free vibration:

M u_ddot + K u = 0

Assuming harmonic motion u(t) = phi sin(omega t) gives:

(K - omega^2 M) phi = 0

A non-zero mode shape exists when det(K - omega^2 M) = 0. The eigenvalues are lambda = omega^2.

## Modal properties
The approximate eigenvalues are 431.27 and 2318.73 s^-2. The corresponding approximate results are:

| Property | Mode 1 | Mode 2 |
|---|---:|---:|
| Circular frequency (rad/s) | 20.77 | 48.15 |
| Natural frequency (Hz) | 3.305 | 7.664 |
| Natural period (s) | 0.303 | 0.130 |
| Floor 1 relative displacement | 0.569 | -1.319 |
| Floor 2 relative displacement | 1.000 | 1.000 |

Mode 1: both floors move in the same direction in this mode. Mode 2: the floors move in opposite directions. The second-floor component is set to 1 for convenient normalisation. Mode-shape values are relative, not actual floor response amplitudes; multiplying a mode vector by -1 does not change the physical mode.

## Assumptions and limitations
- Fixed foundation.
- Two lateral degrees of freedom and lumped floor masses.
- Linear elastic, constant storey stiffnesses.
- Undamped free vibration.
- No external forcing or earthquake ground motion.
- No torsion, floor rotation, distributed mass, or three-dimensional response.
- Assumed illustrative parameters; no experimental calibration or real-building validation.

This is an educational modal-analysis exercise, not structural design or a building-safety assessment.
