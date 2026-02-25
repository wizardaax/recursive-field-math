"""Tests for ParameterSweep in the recursive_field module."""

import math

import pytest

from recursive_field import ParameterSweep

# Golden ratio – used as a local constant to avoid coupling with library internals.
PHI = (1 + math.sqrt(5)) / 2

# Consecutive Lucas numbers L(3), L(4), L(5): each term is the sum of the two
# preceding ones (4 + 7 = 11).
LUCAS_N = [4, 7, 11]


# ---------------------------------------------------------------------------
# Lucas sequence invariants
# ---------------------------------------------------------------------------


def test_lucas_additive_property() -> None:
    """Verify that the chosen Lucas indices satisfy L(n+2) = L(n+1) + L(n)."""
    a, b, c = LUCAS_N
    assert a + b == c


def test_lucas_radius_square_additivity() -> None:
    """radius(n, a)^2 / a^2 == n, so Lucas additive property propagates to radii."""
    scale = 3.0
    sweep = ParameterSweep(
        n_values=LUCAS_N,
        a_values=[scale],
        r_lock_values=[math.sqrt(3.0)],
    )
    df = sweep.run_grid()

    r4 = df.loc[df["n"] == 4, "radius"].values[0]
    r7 = df.loc[df["n"] == 7, "radius"].values[0]
    r11 = df.loc[df["n"] == 11, "radius"].values[0]

    # (r_n / a)^2 = n, so (r4/a)^2 + (r7/a)^2 == (r11/a)^2
    assert abs((r4 / scale) ** 2 + (r7 / scale) ** 2 - (r11 / scale) ** 2) < 1e-10


# ---------------------------------------------------------------------------
# Baseline sweep
# ---------------------------------------------------------------------------


def test_baseline_sweep_row_count() -> None:
    """Baseline sweep with a=3 and r_lock=sqrt(3) yields one row per index."""
    sweep = ParameterSweep(
        n_values=LUCAS_N,
        a_values=[3.0],
        r_lock_values=[math.sqrt(3.0)],
    )
    df = sweep.run_grid()
    assert len(df) == len(LUCAS_N)


def test_baseline_radius_values() -> None:
    """Spot-check radii for the baseline parameter combination."""
    scale = 3.0
    sweep = ParameterSweep(
        n_values=LUCAS_N,
        a_values=[scale],
        r_lock_values=[math.sqrt(3.0)],
    )
    df = sweep.run_grid()

    for n in LUCAS_N:
        r_actual = df.loc[df["n"] == n, "radius"].values[0]
        r_expected = scale * math.sqrt(n)
        assert (
            abs(r_actual - r_expected) < 1e-10
        ), f"radius mismatch at n={n}: got {r_actual}, expected {r_expected}"


# ---------------------------------------------------------------------------
# Schema-stable invariant (replaces brittle df.shape[1] == 9)
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = [
    "n",
    "a",
    "r_lock",
    "radius",
    "angle_deg",
    "x",
    "y",
    "phi_ratio",
    "delta_r",
]


def test_consistent_output_schema() -> None:
    """run_grid output must contain all required columns with no null values."""
    sweep = ParameterSweep(n_values=LUCAS_N)
    df = sweep.run_grid()

    for col in REQUIRED_COLUMNS:
        assert col in df.columns, f"Missing required column: '{col}'"

    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    assert (
        null_counts.sum() == 0
    ), f"Unexpected null values in output:\n{null_counts[null_counts > 0]}"


# ---------------------------------------------------------------------------
# Rounding / floating-point effects
# ---------------------------------------------------------------------------


def test_phi_ratio_precision() -> None:
    """phi_ratio = radius / r_lock is within floating-point tolerance."""
    r_lock = math.sqrt(3.0)
    sweep = ParameterSweep(
        n_values=[1],
        a_values=[3.0],
        r_lock_values=[r_lock],
    )
    df = sweep.run_grid()

    # radius(1, 3) = 3.0; phi_ratio = 3.0 / sqrt(3) = sqrt(3)
    phi_ratio = df["phi_ratio"].values[0]
    expected = 3.0 / r_lock
    assert abs(phi_ratio - expected) < 1e-10


def test_delta_r_precision() -> None:
    """delta_r = radius − r_lock is computed without unexpected precision loss."""
    r_lock = math.sqrt(3.0)
    sweep = ParameterSweep(
        n_values=[1],
        a_values=[3.0],
        r_lock_values=[r_lock],
    )
    df = sweep.run_grid()

    delta_r = df["delta_r"].values[0]
    expected = 3.0 - r_lock
    assert abs(delta_r - expected) < 1e-10


# ---------------------------------------------------------------------------
# PHI (golden ratio) logic
# ---------------------------------------------------------------------------


def test_phi_identity() -> None:
    """PHI satisfies the defining identity φ² = φ + 1."""
    assert abs(PHI**2 - PHI - 1) < 1e-10


def test_phi_ratio_increases_with_n() -> None:
    """phi_ratio must be strictly increasing in n for fixed a and r_lock."""
    sweep = ParameterSweep(
        n_values=LUCAS_N,
        a_values=[3.0],
        r_lock_values=[math.sqrt(3.0)],
    )
    df = sweep.run_grid().sort_values("n").reset_index(drop=True)
    phi_ratios = df["phi_ratio"].tolist()

    for i in range(len(phi_ratios) - 1):
        assert phi_ratios[i] < phi_ratios[i + 1], (
            f"phi_ratio not increasing at position {i}: "
            f"{phi_ratios[i]} >= {phi_ratios[i + 1]}"
        )


def test_grid_expands_over_multiple_parameters() -> None:
    """run_grid produces len(n) * len(a) * len(r_lock) rows."""
    n_vals = LUCAS_N
    a_vals = [2.0, 3.0]
    r_vals = [math.sqrt(3.0), math.sqrt(5.0)]
    sweep = ParameterSweep(n_values=n_vals, a_values=a_vals, r_lock_values=r_vals)
    df = sweep.run_grid()
    assert len(df) == len(n_vals) * len(a_vals) * len(r_vals)


@pytest.mark.parametrize("n", LUCAS_N)
def test_angle_within_range(n: int) -> None:
    """angle_deg output must stay in [0, 360) for all Lucas indices."""
    sweep = ParameterSweep(n_values=[n])
    df = sweep.run_grid()
    theta = df["angle_deg"].values[0]
    assert 0.0 <= theta < 360.0
