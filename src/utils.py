"""
Core mathematical utilities for Paper II:
- Spacetime Algebra (Cl_{1,3}) multivector rotor operations
- REBCO strain-scaling law J_c(e_ax, B, T)
- Turn-to-turn contact resistivity rho_ct and electro-thermal shunting constants
"""

import numpy as np

RHO_CT_NOMINAL = 15.0  # uOhm.cm^2
RHO_CT_SI = 15.0 * 1e-6 * 1e-4  # 1.5e-11 Ohm.m^2
T_MAX_BOUND = 200.0  # Kelvin
STRAIN_MIN_REVERSIBLE = -0.0030  # -0.30%
STRAIN_MAX_REVERSIBLE = 0.0035   # +0.35%

def rebco_strain_scaling(e_ax, Jc0=1.0, a=7000.0, eps_m=0.0005, b=2.2):
    """
    Evaluates normalized critical current density under axial strain e_ax:
    J_c(e_ax) / J_c0 = [1 - a |e_ax - eps_m|^b]
    """
    e_ax = np.asarray(e_ax)
    scaling = 1.0 - a * np.power(np.abs(e_ax - eps_m), b)
    return np.clip(scaling, 0.0, 1.0) * Jc0

def sta_multivector_rotor(theta, b_vector):
    """
    Constructs a Cl_{1,3} Spacetime Algebra multivector rotor:
    R = exp(-0.5 * theta * B) = cos(0.5*theta) - B * sin(0.5*theta)
    """
    cos_half = np.cos(0.5 * theta)
    sin_half = np.sin(0.5 * theta)
    return cos_half, -sin_half * b_vector

def is_within_reversible_window(e_ax):
    return (e_ax >= STRAIN_MIN_REVERSIBLE) & (e_ax <= STRAIN_MAX_REVERSIBLE)
