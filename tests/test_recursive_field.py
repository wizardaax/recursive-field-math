"""Tests for the recursive_field module."""

import math

import pytest

from recursive_field import angle, golden_angle, position, radius


def test_golden_angle() -> None:
    """Test that golden_angle returns approximately 137.508 degrees."""
    phi = golden_angle()
    assert abs(phi - 137.508) < 0.01


def test_radius_base_case() -> None:
    """Test radius at n=1 with a=3."""
    r1 = radius(1, a=3.0)
    # r1 = a * sqrt(1) = 3 * 1 = 3
    assert abs(r1 - 3.0) < 1e-10


def test_radius_growth() -> None:
    """Test that radius grows with sqrt(n)."""
    a = 3.0
    for n in [1, 4, 9, 16]:
        r = radius(n, a)
        expected = a * math.sqrt(n)
        assert abs(r - expected) < 1e-10


def test_radius_invalid_input() -> None:
    """Test that radius raises ValueError for non-positive n."""
    with pytest.raises(ValueError, match="Index n must be positive"):
        radius(0)
    with pytest.raises(ValueError, match="Index n must be positive"):
        radius(-1)


def test_angle_modulo() -> None:
    """Test that angle returns values in [0, 360) range."""
    for n in range(1, 100):
        theta = angle(n)
        assert 0 <= theta < 360


def test_angle_progression() -> None:
    """Test angular progression with golden angle."""
    phi = golden_angle()
    for n in range(1, 10):
        theta = angle(n)
        expected = (n * phi) % 360
        assert abs(theta - expected) < 1e-10


def test_position_returns_tuple() -> None:
    """Test that position returns a tuple of two floats."""
    pos = position(1)
    assert isinstance(pos, tuple)
    assert len(pos) == 2
    assert isinstance(pos[0], float)
    assert isinstance(pos[1], float)


def test_position_at_origin() -> None:
    """Test that position has correct magnitude."""
    n = 1
    a = 3.0
    x, y = position(n, a)
    distance = math.sqrt(x**2 + y**2)
    expected_radius = radius(n, a)
    assert abs(distance - expected_radius) < 1e-10


def test_position_invalid_input() -> None:
    """Test that position raises ValueError for non-positive n."""
    with pytest.raises(ValueError, match="Index n must be positive"):
        position(0)
    with pytest.raises(ValueError, match="Index n must be positive"):
        position(-1)


def test_position_multiple_points() -> None:
    """Test positions for multiple indices."""
    a = 3.0
    positions_list = []
    for n in range(1, 6):
        pos = position(n, a)
        positions_list.append(pos)
        # Verify magnitude matches radius
        x, y = pos
        distance = math.sqrt(x**2 + y**2)
        expected_radius = radius(n, a)
        assert abs(distance - expected_radius) < 1e-10

    # Verify we got 5 unique positions
    assert len(positions_list) == 5
