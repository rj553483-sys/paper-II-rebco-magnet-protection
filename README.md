# Paper II: A Spacetime Algebra Framework for Passive Quench Protection and Radial Shunting in Non-Insulated REBCO High-Field Fusion Magnets

**Author:** Jacob James Rasmussen  
**ORCID:** 0009-0009-7084-6523  
**Target Journal:** *Superconductor Science and Technology* (SuST), IOP Publishing  
**License:** MIT License  

---

## 📌 Executive Overview

This repository contains the numerical solver, mathematical formulations, simulation datasets, and publication-ready assets for **Paper II**:  
*"A Spacetime Algebra Framework for Passive Quench Protection and Radial Shunting in Non-Insulated REBCO High-Field Fusion Magnets"*, targeted for ***Superconductor Science and Technology* (SuST)**.

The study bridges spacetime algebra physics ($Cl_{1,3}$ multivector rotors) with electro-thermal engineering for non-insulated REBCO high-field fusion magnets ($B = 20\text{ T}, T = 4.2\text{ K}$). By eliminating quench singularities through rotor transformation and leveraging turn-to-turn contact resistivity ($\rho_{\text{ct}} = 15.0 \ \mu\Omega\cdot\text{cm}^2$), the system achieves unconditional passive protection bounding peak hotspot temperatures at $T_{\text{max}} \le 200\text{ K}$ while maintaining the conductor strictly within its reversible elastic strain window ($-0.30\% \le e_{\text{ax}} \le +0.35\%$).

---

## 📐 Mathematical & Physics Formulations

### 1. $Cl_{1,3}$ Spacetime Algebra (STA) Multivector Rotor Transformation
Electrodynamic field equations over $Cl_{1,3}$ spacetime algebra eliminate coordinate singularities during quench transients via multivector rotors $R$:
$$\mathbf{F}' = R \mathbf{F} \widetilde{R}, \quad R = \exp\left(-\frac{1}{2}\theta \mathbf{B}\right) = \cos\left(\frac{\theta}{2}\right) - \mathbf{B}\sin\left(\frac{\theta}{2}\right)$$
where $\mathbf{B}$ is the unit spatial bivector.

### 2. Current Conservation & Divergence Condition
Current continuity across turn-to-turn contact interfaces obeys:
$$\nabla \cdot \mathbf{J} = 0 \quad \text{or in geometric calculus: } \partial \cdot J = 0$$

### 3. REBCO Strain Scaling Law $J_c(e_{\text{ax}}, B, T)$
Critical current degradation under strain follows the unified scaling law:
$$J_c(e_{\text{ax}}, B, T) = J_{c0}(B, T) \left[1 - a \vert e_{\text{ax}} - \epsilon_m \vert^b\right]$$
where $a = 7000.0$, $\epsilon_m = +0.05\%$ ($0.0005$), and $b = 2.2$.

### 4. Radial Current Shunting & Time Constant
The $L/R$ time constant governing passive radial current shunting across $\rho_{\text{ct}} = 15.0 \ \mu\Omega\cdot\text{cm}^2$ is:
$$\tau_{L/R} = \frac{L_{\text{pancake}}}{R_{\text{radial}}} \approx 1.0 - 3.0 \text{ s}$$

---

## 📊 Physical Benchmark Matrix

| Parameter / Metric | Symbol / Notation | Benchmark Value | Units / Constraints |
| :--- | :--- | :--- | :--- |
| **Spacetime Algebra Signature** | $Cl_{1,3}$ | Lorentzian $\text{diag}(+,-,-,-)$ | Multivector Rotor Field |
| **Turn-to-Turn Contact Resistivity** | $\rho_{\text{ct}}$ | **$15.0$** | $\mu\Omega\cdot\text{cm}^2$ ($1.5\times 10^{-11} \ \Omega\cdot\text{m}^2$) |
| **Peak Hotspot Temperature Limit** | $T_{\text{max}}$ | **$\le 200.0$** | $\text{K}$ (Passive Bounding) |
| **Circuit Decay Time Constant** | $\tau_{L/R}$ | **$1.0 - 3.0$** | $\text{seconds}$ |
| **Reversible Elastic Strain Window** | $e_{\text{ax}}$ | **$-0.30\% \le e_{\text{ax}} \le +0.35\%$** | Dimensionless Elastic Operating Range |
| **Baseline Magnetic Field** | $B_0$ | **$20.0$** | $\text{Tesla}$ |
| **Operating Temperature** | $T_{\text{op}}$ | **$4.2$** | $\text{Kelvin}$ |
| **Buckingham Pi Scale Invariance** | $\Pi_1$ | **$1.0000$** | Dimensionless Scale Invariance |

---

## 📁 Modular Directory Structure

```
paper-II-github-repository/
├── LICENSE                                # MIT License
├── README.md                              # Main landing page documentation
├── CITATION.cff                           # Citation File Format for SuST / IOP Publishing
├── requirements.txt                       # Python dependencies
├── .github/
│   └── workflows/
│       └── python-test.yml               # Automated CI/CD build & test workflow
├── docs/
│   ├── Main_Manuscript.pdf                # Full manuscript v3.0 for SuST
│   ├── Cover_Letter.pdf                   # Cover letter to SuST Editor
│   ├── Highlights.pdf                     # Core submission highlights
│   └── Supplementary_Information.pdf      # ESI: STA derivations & proofs
├── src/
│   ├── __init__.py                        # Package initialization
│   ├── utils.py                           # REBCO scaling & STA rotor parameters
│   └── solver.py                          # Numerical solver & plot generator
├── data/
│   ├── raw_simulation_data.csv            # 500-point strain-current & thermal matrix
│   └── benchmark_summary.json             # Structured benchmark values & parameters
└── figures/
    ├── figure1_300dpi.png                 # High-resolution raster figure (300 DPI)
    └── figure1_vector.svg                 # Scalable vector graphic figure
```

---

## 🚀 Quickstart Installation & Execution

### 1. Environment Setup
```bash
pip install -r requirements.txt
```

### 2. Execute Numerical Solver & Re-generate Figures
```bash
python src/solver.py
```

Execution will verify parameters, output `data/raw_simulation_data.csv` (500 data points), write `data/benchmark_summary.json`, and produce high-resolution figures in `figures/`.

---

## ✒️ Citation

If you use this repository or mathematical framework in your research, please cite it as:

```bibtex
@article{rasmussen2026paper2,
  author    = {Jacob James Rasmussen},
  title     = {A Spacetime Algebra Framework for Passive Quench Protection and Radial Shunting in Non-Insulated REBCO High-Field Fusion Magnets},
  journal   = {Superconductor Science and Technology},
  year      = {2026},
  publisher = {IOP Publishing},
  note      = {ORCID: 0009-0009-7084-6523}
}
```
