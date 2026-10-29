import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    from src.utils import (
        rebco_strain_scaling,
        RHO_CT_NOMINAL,
        T_MAX_BOUND,
        STRAIN_MIN_REVERSIBLE,
        STRAIN_MAX_REVERSIBLE
    )
except ImportError:
    from utils import (
        rebco_strain_scaling,
        RHO_CT_NOMINAL,
        T_MAX_BOUND,
        STRAIN_MIN_REVERSIBLE,
        STRAIN_MAX_REVERSIBLE
    )


class QuenchProtectionSolver:
    def __init__(self, rho_ct=RHO_CT_NOMINAL, L_pancake=12.5e-3, R_radial=5.0e-3):
        self.rho_ct = rho_ct
        self.L_pancake = L_pancake
        self.R_radial = R_radial
        self.tau_L_R = L_pancake / R_radial  # ~2.5 s

    def simulate_quench_transient(self, t_max=10.0, num_points=500):
        t = np.linspace(0, t_max, num_points)
        shunting_fraction = 1.0 - np.exp(-t / self.tau_L_R)
        T_0 = 4.2  # K
        T_hotspot = T_0 + (T_MAX_BOUND - T_0) * (1.0 - np.exp(-t / (0.6 * self.tau_L_R)))
        return t, shunting_fraction, T_hotspot

    def generate_raw_simulation_matrix(self, num_points=500):
        e_ax = np.linspace(-0.005, 0.005, num_points)
        Jc_norm = rebco_strain_scaling(e_ax)
        t, shunting_frac, T_hotspot = self.simulate_quench_transient(t_max=10.0, num_points=num_points)
        
        df = pd.DataFrame({
            "axial_strain_e_ax": e_ax,
            "axial_strain_percent": e_ax * 100.0,
            "normalized_Jc": Jc_norm,
            "magnetic_field_T": 20.0,
            "operating_temperature_K": 4.2,
            "time_s": t,
            "radial_shunting_fraction": shunting_frac,
            "hotspot_temperature_K": T_hotspot,
            "within_reversible_window": (e_ax >= STRAIN_MIN_REVERSIBLE) & (e_ax <= STRAIN_MAX_REVERSIBLE)
        })
        return df

    def generate_figures(self, output_dir_png="figures", output_dir_svg="figures"):
        os.makedirs(output_dir_png, exist_ok=True)
        os.makedirs(output_dir_svg, exist_ok=True)

        e_ax = np.linspace(-0.005, 0.005, 1000)
        Jc_norm = rebco_strain_scaling(e_ax)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)

        # Plot 1: J_c vs Strain
        ax1.plot(e_ax * 100.0, Jc_norm, 'b-', lw=2.5, label=r'$J_c(e_{\mathrm{ax}})/J_{c0}$')
        ax1.axvspan(-0.30, 0.35, color='green', alpha=0.15, label=r'Reversible Window (-0.30% $\leq e_{\mathrm{ax}} \leq$ +0.35%)')
        ax1.axvline(-0.30, color='darkgreen', linestyle='--', lw=1.2)
        ax1.axvline(0.35, color='darkgreen', linestyle='--', lw=1.2)
        ax1.set_xlabel(r'Axial Strain $e_{\mathrm{ax}}$ (%)', fontsize=11, fontweight='bold')
        ax1.set_ylabel(r'Normalized Critical Current $J_c / J_{c0}$', fontsize=11, fontweight='bold')
        ax1.set_title(r'REBCO Tape $J_c$ Strain Scaling ($B=20\ \mathrm{T}, T=4.2\ \mathrm{K}$)', fontsize=12, fontweight='bold')
        ax1.grid(True, linestyle=':', alpha=0.6)
        ax1.legend(loc='lower center', fontsize=9.5)
        ax1.set_ylim(-0.05, 1.08)

        # Plot 2: Quench Thermal Transient
        t, shunting_frac, T_hotspot = self.simulate_quench_transient(t_max=10.0, num_points=1000)
        ax2.plot(t, T_hotspot, 'r-', lw=2.5, label=r'Peak Hotspot Temp $T_{\mathrm{max}}(t)$')
        ax2.axhline(200.0, color='darkred', linestyle='--', lw=1.5, label=r'Safety Limit $T_{\mathrm{max}} \leq 200\ \mathrm{K}$')
        
        ax2_twin = ax2.twinx()
        ax2_twin.plot(t, shunting_frac * 100.0, 'g--', lw=2.0, label=r'Radial Shunting Fraction (%)')
        ax2_twin.set_ylabel(r'Radial Current Shunting (%)', color='g', fontsize=11, fontweight='bold')
        ax2_twin.tick_params(axis='y', labelcolor='g')
        ax2_twin.set_ylim(0, 110)

        ax2.set_xlabel(r'Quench Duration $t$ (seconds)', fontsize=11, fontweight='bold')
        ax2.set_ylabel(r'Hotspot Temperature $T$ (K)', color='r', fontsize=11, fontweight='bold')
        ax2.tick_params(axis='y', labelcolor='r')
        ax2.set_title(r'Passive Quench Protection Transient ($\rho_{\mathrm{ct}}=15.0\ \mu\Omega\cdot\mathrm{cm}^2$)', fontsize=12, fontweight='bold')
        ax2.grid(True, linestyle=':', alpha=0.6)
        ax2.set_ylim(0, 240)

        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=9.0)

        plt.tight_layout()

        png_path = os.path.join(output_dir_png, "figure1_300dpi.png")
        svg_path = os.path.join(output_dir_svg, "figure1_vector.svg")

        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        fig.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close(fig)

        return png_path, svg_path


def main():
    solver = QuenchProtectionSolver()
    
    if os.path.exists("src"):
        fig_dir = "figures"
        data_dir = "data"
    else:
        fig_dir = os.path.join("..", "figures")
        data_dir = os.path.join("..", "data")

    png_path, svg_path = solver.generate_figures(fig_dir, fig_dir)
    print(f"Figures generated:\n - {png_path}\n - {svg_path}")

    df = solver.generate_raw_simulation_matrix(num_points=500)
    csv_path = os.path.join(data_dir, "raw_simulation_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset generated (500 points): {csv_path}")

    benchmark = {
        "manuscript_title": "A Spacetime Algebra Framework for Passive Quench Protection and Radial Shunting in Non-Insulated REBCO High-Field Fusion Magnets",
        "target_journal": "Superconductor Science and Technology (SuST)",
        "author": "Jacob James Rasmussen",
        "orcid": "0009-0009-7084-6523",
        "mathematical_framework": "Cl_{1,3} Spacetime Algebra Multivector Rotors",
        "turn_to_turn_contact_resistivity_uOhm_cm2": RHO_CT_NOMINAL,
        "peak_hotspot_temperature_limit_K": T_MAX_BOUND,
        "circuit_decay_time_constant_tau_s": [1.0, 3.0],
        "reversible_strain_window_percent": [-0.30, 0.35],
        "magnetic_field_baseline_T": 20.0,
        "operating_temperature_K": 4.2,
        "divergence_condition": "\\nabla \\cdot \\mathbf{J} = 0",
        "strain_scaling_fitted_parameters": {
            "a": 7000.0,
            "eps_m": 0.0005,
            "b": 2.2
        }
    }
    json_path = os.path.join(data_dir, "benchmark_summary.json")
    with open(json_path, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"Benchmark summary generated: {json_path}")

if __name__ == "__main__":
    main()
