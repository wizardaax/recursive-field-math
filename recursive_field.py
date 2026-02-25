"""
Recursive Field: Mathematical formulas for phyllotaxis patterns.

This module implements the mathematical relationships described in the
"Recursive Field" scientific math song, including radius growth and
angular progression based on the golden angle.
"""

import math
from typing import Any, Optional


def golden_angle() -> float:
    """
    Return the golden angle in degrees.

    The golden angle is approximately 137.508 degrees and is derived from
    the golden ratio.

    Returns:
        float: The golden angle in degrees
    """
    return 180.0 * (3.0 - math.sqrt(5.0))


def radius(n: int, a: float = 3.0) -> float:
    """
    Calculate the radius for a given index.

    Args:
        n: The index (must be positive)
        a: Scale factor (default: 3.0)

    Returns:
        float: The radius value r_n = a * sqrt(n)

    Raises:
        ValueError: If n is not positive
    """
    if n <= 0:
        raise ValueError("Index n must be positive")
    return a * math.sqrt(n)


def angle(n: int) -> float:
    """
    Calculate the angle for a given index.

    Args:
        n: The index

    Returns:
        float: The angle in degrees, θ_n = n * φ (mod 360)
    """
    phi = golden_angle()
    return (n * phi) % 360.0


def position(n: int, a: float = 3.0) -> tuple[float, float]:
    """
    Calculate the Cartesian position for a given index.

    Args:
        n: The index (must be positive)
        a: Scale factor (default: 3.0)

    Returns:
        tuple: (x, y) coordinates in Cartesian space

    Raises:
        ValueError: If n is not positive
    """
    r = radius(n, a)
    theta_deg = angle(n)
    theta_rad = math.radians(theta_deg)
    x = r * math.cos(theta_rad)
    y = r * math.sin(theta_rad)
    return (x, y)


class ParameterSweep:
    """Grid search over parameter combinations for the recursive field model.

    Evaluates radius, angle, and position for every combination of *n*,
    scale factor *a*, and locked-radius *r_lock* supplied at construction
    time and exposes the results as a ``pandas.DataFrame`` via
    :meth:`run_grid`.
    """

    def __init__(
        self,
        n_values: list[int],
        a_values: Optional[list[float]] = None,
        r_lock_values: Optional[list[float]] = None,
    ) -> None:
        """
        Initialise the sweep.

        Args:
            n_values: Sequence of positive integer indices to evaluate.
            a_values: Scale factors to sweep over (default: ``[3.0]``).
            r_lock_values: Reference radii for ratio/delta columns
                (default: ``[sqrt(3)]``).
        """
        self.n_values = n_values
        self.a_values = a_values if a_values is not None else [3.0]
        self.r_lock_values = (
            r_lock_values if r_lock_values is not None else [math.sqrt(3.0)]
        )

    def run_grid(self) -> Any:
        """Run the parameter grid and return results as a ``pandas.DataFrame``.

        Columns
        -------
        n           : int   – index value
        a           : float – scale factor
        r_lock      : float – reference (locked) radius
        radius      : float – r_n = a * sqrt(n)
        angle_deg   : float – θ_n = n * golden_angle (mod 360)
        x           : float – Cartesian x coordinate
        y           : float – Cartesian y coordinate
        phi_ratio   : float – radius / r_lock  (ratio to locked radius)
        delta_r     : float – radius − r_lock  (signed difference)

        Returns:
            pandas.DataFrame with one row per (n, a, r_lock) combination.
        """
        import pandas as pd  # noqa: PLC0415

        rows = []
        for n in self.n_values:
            for a in self.a_values:
                for r_lock in self.r_lock_values:
                    r = radius(n, a)
                    theta = angle(n)
                    x, y = position(n, a)
                    phi_ratio = r / r_lock if r_lock != 0.0 else float("nan")
                    delta_r = r - r_lock
                    rows.append(
                        {
                            "n": n,
                            "a": a,
                            "r_lock": r_lock,
                            "radius": r,
                            "angle_deg": theta,
                            "x": x,
                            "y": y,
                            "phi_ratio": phi_ratio,
                            "delta_r": delta_r,
                        }
                    )
        return pd.DataFrame(rows)
