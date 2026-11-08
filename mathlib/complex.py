"""Complex numbers, implemented from scratch.

A complex number z = a + bi is stored as two real numbers: the real part
``a`` and the imaginary part ``b``. In the simulation, every wave is a
complex number: its modulus is the wave's amplitude and its argument is the
wave's phase. Adding waves = adding complex numbers.

Only Python's ``math`` module is used (for sqrt, sin, cos, atan2).
The built-in ``complex`` type is deliberately not used.
"""

from __future__ import annotations

import math
from numbers import Real

__all__ = ["Complex"]


def _validate_real(value: object, name: str) -> float:
    """Check that ``value`` is a finite real number and return it as float.

    Args:
        value: The value to check.
        name: Parameter name, used in the error message.

    Returns:
        The value converted to ``float``.

    Raises:
        TypeError: If ``value`` is not a real number (bools are rejected too).
        ValueError: If ``value`` is NaN or infinite.
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite, got {result}")
    return result


class Complex:
    """An immutable complex number ``re + im*i``.

    Supports ``+``, ``-``, ``*``, ``/`` with other ``Complex`` values and with
    plain real numbers (on either side), plus ``==`` and unary ``-``.

    Example:
        >>> z = Complex(3, 4)
        >>> z.modulus()
        5.0
        >>> z * Complex(0, 1)
        Complex(-4.0, 3.0)
    """

    __slots__ = ("_re", "_im")

    def __init__(self, re: float = 0.0, im: float = 0.0) -> None:
        """Create a complex number.

        Args:
            re: Real part. Must be a finite real number.
            im: Imaginary part. Must be a finite real number.

        Raises:
            TypeError: If a part is not a real number.
            ValueError: If a part is NaN or infinite.
        """
        self._re = _validate_real(re, "re")
        self._im = _validate_real(im, "im")

    # ------------------------------------------------------------------ #
    # Construction helpers
    # ------------------------------------------------------------------ #
    @classmethod
    def from_polar(cls, r: float, theta: float) -> Complex:
        """Build ``r * (cos(theta) + i*sin(theta))``.

        Args:
            r: Modulus (amplitude). Must be >= 0.
            theta: Argument (phase) in radians.

        Returns:
            The complex number with the given modulus and argument.

        Raises:
            ValueError: If ``r`` is negative.
        """
        r = _validate_real(r, "r")
        theta = _validate_real(theta, "theta")
        if r < 0:
            raise ValueError(f"r must be non-negative, got {r}")
        return cls(r * math.cos(theta), r * math.sin(theta))

    @classmethod
    def exp_i(cls, theta: float) -> Complex:
        """Return ``e^(i*theta)``, the unit complex number at angle ``theta``.

        This is Euler's formula: ``e^(i*theta) = cos(theta) + i*sin(theta)``.
        It is the building block of every wave in the simulation.

        Args:
            theta: Angle in radians.

        Returns:
            A complex number with modulus 1 and argument ``theta``.
        """
        return cls.from_polar(1.0, theta)

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #
    @property
    def re(self) -> float:
        """The real part."""
        return self._re

    @property
    def im(self) -> float:
        """The imaginary part."""
        return self._im

    def conjugate(self) -> Complex:
        """Return the complex conjugate ``re - im*i``."""
        return Complex(self._re, -self._im)

    def modulus_squared(self) -> float:
        """Return ``|z|^2 = re^2 + im^2``.

        For a wave, this is its intensity (brightness on the screen).
        Cheaper than ``modulus()`` because it avoids a square root.
        """
        return self._re * self._re + self._im * self._im

    def modulus(self) -> float:
        """Return ``|z|``, the distance from the origin (the amplitude)."""
        return math.sqrt(self.modulus_squared())

    def argument(self) -> float:
        """Return the angle of ``z`` in radians, in the range ``(-pi, pi]``.

        By convention, the argument of zero is ``0.0``.
        """
        return math.atan2(self._im, self._re)

    def is_close(self, other: Complex, tol: float = 1e-9) -> bool:
        """Return True if ``self`` and ``other`` differ by at most ``tol``.

        Floating-point results are rarely exactly equal, so tests should
        compare with this instead of ``==``.

        Args:
            other: The complex number to compare against.
            tol: Maximum allowed distance. Must be >= 0.

        Raises:
            TypeError: If ``other`` is not a ``Complex``.
            ValueError: If ``tol`` is negative.
        """
        if not isinstance(other, Complex):
            raise TypeError(f"other must be Complex, got {type(other).__name__}")
        tol = _validate_real(tol, "tol")
        if tol < 0:
            raise ValueError(f"tol must be non-negative, got {tol}")
        return (self - other).modulus() <= tol

    # ------------------------------------------------------------------ #
    # Arithmetic
    # ------------------------------------------------------------------ #
    @staticmethod
    def _coerce(value: object) -> Complex | None:
        """Turn a real number into a ``Complex``; return None if unsupported."""
        if isinstance(value, Complex):
            return value
        if isinstance(value, Real) and not isinstance(value, bool):
            return Complex(value, 0.0)
        return None

    def __add__(self, other: object) -> Complex:
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(self._re + o._re, self._im + o._im)

    __radd__ = __add__

    def __neg__(self) -> Complex:
        return Complex(-self._re, -self._im)

    def __sub__(self, other: object) -> Complex:
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(self._re - o._re, self._im - o._im)

    def __rsub__(self, other: object) -> Complex:
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return o - self

    def __mul__(self, other: object) -> Complex:
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Complex(
            self._re * o._re - self._im * o._im,
            self._re * o._im + self._im * o._re,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> Complex:
        # z / w = z * conj(w) / |w|^2
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        denom = o.modulus_squared()
        if denom == 0.0:
            raise ZeroDivisionError("division by zero complex number")
        num = self * o.conjugate()
        return Complex(num._re / denom, num._im / denom)

    def __rtruediv__(self, other: object) -> Complex:
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return o / self

    # ------------------------------------------------------------------ #
    # Comparison and display
    # ------------------------------------------------------------------ #
    def __eq__(self, other: object) -> bool:
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self._re == o._re and self._im == o._im

    def __hash__(self) -> int:
        return hash((self._re, self._im))

    def __repr__(self) -> str:
        return f"Complex({self._re!r}, {self._im!r})"

    def __str__(self) -> str:
        sign = "+" if self._im >= 0 else "-"
        return f"{self._re:g} {sign} {abs(self._im):g}i"
