"""Tests for mathlib.complex.Complex."""

import math

import pytest

from mathlib.complex import Complex


# --------------------------------------------------------------------- #
# Construction and validation
# --------------------------------------------------------------------- #
class TestConstruction:
    def test_default_is_zero(self):
        z = Complex()
        assert z.re == 0.0 and z.im == 0.0

    def test_parts_are_stored_as_floats(self):
        z = Complex(3, 4)
        assert isinstance(z.re, float) and isinstance(z.im, float)

    @pytest.mark.parametrize("bad", ["1", None, [1], True, Complex(1, 0)])
    def test_rejects_non_real(self, bad):
        with pytest.raises(TypeError):
            Complex(bad, 0)
        with pytest.raises(TypeError):
            Complex(0, bad)

    @pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
    def test_rejects_non_finite(self, bad):
        with pytest.raises(ValueError):
            Complex(bad, 0)

    def test_from_polar(self):
        z = Complex.from_polar(2, math.pi / 2)
        assert z.is_close(Complex(0, 2))

    def test_from_polar_rejects_negative_r(self):
        with pytest.raises(ValueError):
            Complex.from_polar(-1, 0)

    def test_from_polar_validates_theta(self):
        with pytest.raises(TypeError):
            Complex.from_polar(1, "pi")

    @pytest.mark.parametrize("theta", [0, 0.5, math.pi, -2.0, 10.0])
    def test_exp_i_has_unit_modulus(self, theta):
        assert math.isclose(Complex.exp_i(theta).modulus(), 1.0)

    def test_euler_identity(self):
        # e^(i*pi) + 1 = 0
        assert (Complex.exp_i(math.pi) + 1).is_close(Complex(0, 0))


# --------------------------------------------------------------------- #
# Properties
# --------------------------------------------------------------------- #
class TestProperties:
    def test_conjugate(self):
        assert Complex(3, 4).conjugate() == Complex(3, -4)

    def test_modulus_and_squared(self):
        z = Complex(3, 4)
        assert z.modulus() == 5.0
        assert z.modulus_squared() == 25.0

    @pytest.mark.parametrize(
        "z, expected",
        [
            (Complex(1, 0), 0.0),
            (Complex(0, 1), math.pi / 2),
            (Complex(-1, 0), math.pi),
            (Complex(0, -1), -math.pi / 2),
            (Complex(0, 0), 0.0),
        ],
    )
    def test_argument(self, z, expected):
        assert math.isclose(z.argument(), expected, abs_tol=1e-12)

    def test_polar_round_trip(self):
        z = Complex(-2.5, 1.5)
        back = Complex.from_polar(z.modulus(), z.argument())
        assert back.is_close(z)

    def test_is_close_tolerance(self):
        assert Complex(1, 1).is_close(Complex(1, 1 + 1e-12))
        assert not Complex(1, 1).is_close(Complex(1, 1.1))
        assert Complex(1, 1).is_close(Complex(1, 1.1), tol=0.2)

    def test_is_close_validation(self):
        with pytest.raises(TypeError):
            Complex(1, 1).is_close(1)
        with pytest.raises(ValueError):
            Complex(1, 1).is_close(Complex(1, 1), tol=-1)


# --------------------------------------------------------------------- #
# Arithmetic
# --------------------------------------------------------------------- #
class TestArithmetic:
    def test_add(self):
        assert Complex(1, 2) + Complex(3, 4) == Complex(4, 6)

    def test_add_real_both_sides(self):
        assert Complex(1, 2) + 3 == Complex(4, 2)
        assert 3 + Complex(1, 2) == Complex(4, 2)

    def test_neg(self):
        assert -Complex(1, -2) == Complex(-1, 2)

    def test_sub(self):
        assert Complex(5, 5) - Complex(2, 3) == Complex(3, 2)

    def test_sub_real_both_sides(self):
        assert Complex(5, 5) - 2 == Complex(3, 5)
        assert 2 - Complex(5, 5) == Complex(-3, -5)

    def test_mul(self):
        # (1 + 2i)(3 + 4i) = 3 + 4i + 6i - 8 = -5 + 10i
        assert Complex(1, 2) * Complex(3, 4) == Complex(-5, 10)

    def test_i_squared_is_minus_one(self):
        i = Complex(0, 1)
        assert i * i == Complex(-1, 0)

    def test_mul_real_both_sides(self):
        assert Complex(1, 2) * 2 == Complex(2, 4)
        assert 2 * Complex(1, 2) == Complex(2, 4)

    def test_div(self):
        z, w = Complex(-5, 10), Complex(3, 4)
        assert (z / w).is_close(Complex(1, 2))

    def test_div_real_both_sides(self):
        assert (Complex(2, 4) / 2).is_close(Complex(1, 2))
        # 1 / i = -i
        assert (1 / Complex(0, 1)).is_close(Complex(0, -1))

    def test_div_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            Complex(1, 1) / Complex(0, 0)
        with pytest.raises(ZeroDivisionError):
            Complex(1, 1) / 0

    @pytest.mark.parametrize("bad", ["x", None, [1], True])
    def test_unsupported_operands_raise_type_error(self, bad):
        z = Complex(1, 1)
        for op in (
            lambda: z + bad,
            lambda: bad + z,
            lambda: z - bad,
            lambda: bad - z,
            lambda: z * bad,
            lambda: bad * z,
            lambda: z / bad,
            lambda: bad / z,
        ):
            with pytest.raises(TypeError):
                op()

    def test_waves_cancel_when_out_of_phase(self):
        # Two equal waves half a cycle apart cancel: the dark fringe.
        assert (Complex.exp_i(0) + Complex.exp_i(math.pi)).is_close(Complex(0, 0))

    def test_waves_double_when_in_phase(self):
        # Two equal waves in phase: amplitude 2, intensity 4: the bright fringe.
        total = Complex.exp_i(1.0) + Complex.exp_i(1.0)
        assert math.isclose(total.modulus_squared(), 4.0)


# --------------------------------------------------------------------- #
# Comparison and display
# --------------------------------------------------------------------- #
class TestComparisonAndDisplay:
    def test_eq_with_real(self):
        assert Complex(2, 0) == 2
        assert Complex(2, 1) != 2

    def test_eq_with_unsupported_type(self):
        assert Complex(1, 0) != "1"

    def test_hash_consistent_with_eq(self):
        assert hash(Complex(1, 2)) == hash(Complex(1, 2))
        assert len({Complex(1, 2), Complex(1, 2), Complex(2, 1)}) == 2

    def test_repr(self):
        assert repr(Complex(1, -2)) == "Complex(1.0, -2.0)"

    def test_str(self):
        assert str(Complex(1, -2)) == "1 - 2i"
        assert str(Complex(1.5, 2)) == "1.5 + 2i"

    def test_immutable(self):
        z = Complex(1, 2)
        with pytest.raises(AttributeError):
            z.re = 5
        with pytest.raises(AttributeError):
            z.extra = 5
