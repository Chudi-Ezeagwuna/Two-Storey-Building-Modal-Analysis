"""
Two-storey shear building: undamped free-vibration modal analysis.

Run from the repository root:
    py src/modal_analysis.py

The model parameters are illustrative assumed values.
"""
from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np

# Illustrative input parameters
M1 = 20_000.0       # first-floor mass (kg)
M2 = 15_000.0       # second-floor mass (kg)
K1 = 20_000_000.0   # first-storey lateral stiffness (N/m)
K2 = 15_000_000.0   # second-storey lateral stiffness (N/m)


def build_mass_matrix(m1, m2):
    """Construct the diagonal 2-DOF lumped-mass matrix."""
    return np.array([[m1, 0.0], [0.0, m2]], dtype=float)


def build_stiffness_matrix(k1, k2):
    """Construct the fixed-base two-storey shear-building stiffness matrix."""
    return np.array([[k1 + k2, -k2], [-k2, k2]], dtype=float)


def modal_analysis(mass_matrix, stiffness_matrix):
    """Solve K phi = lambda M phi and return sorted modal properties."""
    if mass_matrix.shape != (2, 2) or stiffness_matrix.shape != (2, 2):
        raise ValueError("This implementation requires 2-by-2 matrices.")
    if not np.allclose(mass_matrix, mass_matrix.T):
        raise ValueError("Mass matrix must be symmetric.")
    if not np.allclose(stiffness_matrix, stiffness_matrix.T):
        raise ValueError("Stiffness matrix must be symmetric.")
    if np.any(np.linalg.eigvalsh(mass_matrix) <= 0):
        raise ValueError("Mass matrix must be positive definite.")
    if np.any(np.linalg.eigvalsh(stiffness_matrix) <= 0):
        raise ValueError("Stiffness matrix must be positive definite.")

    # Solve M A = K for A (equivalent to A = M^(-1) K),
    # then solve the standard eigenvalue problem A phi = lambda phi.
    eigenvalues, eigenvectors = np.linalg.eig(
        np.linalg.solve(mass_matrix, stiffness_matrix)
    )
    eigenvalues = np.real_if_close(eigenvalues).astype(float)
    eigenvectors = np.real_if_close(eigenvectors).astype(float)

    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    if np.any(eigenvalues <= 0):
        raise ValueError("Positive eigenvalues are required for this model.")

    omega = np.sqrt(eigenvalues)          # rad/s
    frequency_hz = omega / (2 * np.pi)   # cycles/s
    period_s = 1 / frequency_hz          # s

    # Scale each eigenvector so its second-floor component is +1.
    mode_shapes = eigenvectors / eigenvectors[1, :]
    return eigenvalues, omega, frequency_hz, period_s, mode_shapes


def plot_mode_shapes(mode_shapes, output_file):
    """Save a schematic plot of the two relative mode shapes."""
    levels = np.array([0.0, 1.0, 2.0])
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

    for j, ax in enumerate(axes):
        shape = mode_shapes[:, j]
        profile = np.array([0.0, shape[0], shape[1]])

        ax.plot([0, 0, 0], levels, "--", linewidth=1.5,
                label="Undeformed reference")
        ax.plot(profile, levels, "-o", linewidth=2,
                label="Relative mode shape")
        ax.set_title(f"Mode {j + 1}")
        ax.set_xlabel("Relative horizontal displacement")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
        ax.set_ylim(-0.15, 2.15)
        ax.text(0.03, 1, "Floor 1", va="center", fontsize=8)
        ax.text(0.03, 2, "Floor 2", va="center", fontsize=8)
        ax.text(0.03, 0, "Fixed base", va="bottom", fontsize=8)

    axes[0].set_ylabel("Building level")
    fig.suptitle("Relative Mode Shapes of a Two-Storey Shear Building")
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_results(output_file, values):
    """Write modal properties and mode-shape components to a CSV file."""
    eigenvalues, omega, frequency_hz, period_s, modes = values
    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Mode", "Eigenvalue_s-2", "Circular_frequency_rad_s",
            "Natural_frequency_Hz", "Natural_period_s",
            "Floor_1_relative_displacement", "Floor_2_relative_displacement"
        ])
        for i in range(2):
            writer.writerow([
                i + 1, f"{eigenvalues[i]:.6f}", f"{omega[i]:.6f}",
                f"{frequency_hz[i]:.6f}", f"{period_s[i]:.6f}",
                f"{modes[0, i]:.6f}", f"{modes[1, i]:.6f}"
            ])


def main():
    root = Path(__file__).resolve().parents[1]
    results_dir = root / "results"
    results_dir.mkdir(exist_ok=True)

    M = build_mass_matrix(M1, M2)
    K = build_stiffness_matrix(K1, K2)
    values = modal_analysis(M, K)
    eigenvalues, omega, frequency_hz, period_s, modes = values

    print("=" * 58)
    print("TWO-STOREY SHEAR BUILDING: MODAL ANALYSIS")
    print("=" * 58)
    print("\nMASS MATRIX, M (kg):")
    print(M)
    print("\nSTIFFNESS MATRIX, K (N/m):")
    print(K)
    print("\nMODAL RESULTS:")
    for i in range(2):
        print(f"\nMODE {i + 1}")
        print(f"Eigenvalue:          {eigenvalues[i]:.4f} s^-2")
        print(f"Circular frequency:  {omega[i]:.4f} rad/s")
        print(f"Natural frequency:   {frequency_hz[i]:.4f} Hz")
        print(f"Natural period:      {period_s[i]:.4f} s")
        print(f"Mode shape [u1, u2]: {modes[:, i]}")

    plot_mode_shapes(modes, results_dir / "mode_shapes.png")
    save_results(results_dir / "modal_results.csv", values)
    print("\nGenerated:")
    print("  results/mode_shapes.png")
    print("  results/modal_results.csv")


if __name__ == "__main__":
    main()
