"""Vectors (Vec3), implemented from scratch.

A vector is stored as three coordinates, x, y and z.
In the simulation, the positions of the light source,
slit points, and screen points are all stored as vectors
The distance between them sets each wave's phase

Only Python's ``math`` module is used (for sqrt).
"""


import math
from numbers import Real

from mathlib._validation import _validate_real

class Vector:
    """An immutable vector ``x, y, z``.

    Supports ``+``, ``-`` with other ``Vector`` values
    Supports ``*`` with other ``float`` values
    Supports cross product and dot product with other ``Vector`` values
    plus ``==`` and unary ``-``.

    Example:
        >>> v = Vector(2.0, 3.0, 6.0)
        >>> v.norm()
        7.0
        >>> v * 2.0
        Vector(4.0, 6.0, 12.0)
    """

    __slots__ = ['_x','_y','_z']

    def __init__(self,x=0.0,y=0.0,z=0.0):
        """Create a vector.

        Args:
            x: x-coordinate
            y: y-coordinate
            z: z-coordinate

        Raises:
            TypeError: If a part is not a real number.
            ValueError: If a part is NaN or infinite.
        """
        self._x = _validate_real(x, 'x')
        self._y = _validate_real(y, 'y')
        self._z = _validate_real(z, 'z')

    @classmethod
    def zero(cls):
        """
        Creates an empty vector (the zero vector).

        Returns:
            The vector with all coordinates equal to zero.
        """
        return cls(0,0,0)

    @property
    def x(self) -> float:
        """Return the x coordinate of the vector"""
        return self._x

    @property
    def y(self) -> float:
        """Return the y coordinate of the vector"""
        return self._y

    @property
    def z(self) -> float:
        """Return the z coordinate of the vector"""
        return self._z

    def __add__(self,other):
        if not isinstance(other,Vector):
            return NotImplemented
        return Vector(self._x+other._x,self._y+other._y,self._z+other._z)

    def __sub__(self,other):
        if not isinstance(other,Vector):
            return NotImplemented
        return Vector(self._x-other._x,self._y-other._y,self._z-other._z)

    def __neg__(self):
        return Vector(-self._x,-self._y,-self._z)

    def __mul__(self,other):
        if isinstance(other, bool) or not isinstance(other, Real):
            return NotImplemented
        other = _validate_real(other, "scalar")
        return Vector(self._x*other,self._y*other,self._z*other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self,other):
        if isinstance(other, bool) or not isinstance(other, Real):
            return NotImplemented
        other = _validate_real(other, "scalar")
        if other == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector(self._x/other,self._y/other,self._z/other)

    def norm_squared(self):
        """
        Calculates the squared norm of the vector.

        Returns:
            the squared norm of the vector.
        """
        return self._x*self._x + self._y*self._y + self._z*self._z

    def norm(self):
        """
        Calculates the norm of the vector.

        Returns:
            the norm of the vector.
        """
        return math.sqrt(self.norm_squared())

    def normalize(self):
        """
        Calculates the normalized vector.

        Returns:
            the normalized vector.

        Raises:
            ValueError: If the norm is zero.
        """
        n = self.norm()
        if n == 0:
            raise ValueError("Cannot normalize a vector with zero norm")
        return Vector(self._x/n,self._y/n,self._z/n)

    def dot(self, other):
        """
        Calculates the dot product between two vectors.
        Args:
            other: the other vector to dot product with.

        Returns:
            the dot product between the two vectors.

        Raises:
            TypeError: If other is not a Vector.
        """
        if not isinstance(other,Vector):
            raise TypeError(f"other must be Vector, got {type(other).__name__}")
        return (self._x*other._x) + (self._y*other._y) + (self._z*other._z)

    def cross(self,other):
        """
        Calculates the cross product between two vectors.
        Args:
            other: the other vector to cross product with.

        Returns:
            the cross product between the two vectors.

        Raises:
            TypeError: If other is not a Vector.
        """
        if not isinstance(other,Vector):
            raise TypeError(f"other must be Vector, got {type(other).__name__}")
        return Vector(self._y*other._z - self._z*other._y, self._z*other._x - self._x*other._z, self._x*other._y - self._y*other._x)

    def distance(self,other):
        """
        Calculates the distance between two vectors.
        Args:
            other: the other vector to calculate the distance from.

        Returns:
            the distance between the two vectors.

        Raises:
            TypeError: If other is not a Vector.
        """
        if not isinstance(other,Vector):
            raise TypeError(f"other must be Vector, got {type(other).__name__}")
        return (self-other).norm()

    def __eq__(self,other):
        if not isinstance(other,Vector):
            return NotImplemented
        return self._x == other._x and self._y == other._y and self._z == other._z

    def  __hash__(self):
        return hash((self._x,self._y,self._z))

    def is_close(self, other, tol=1e-9):
        """
        Checks if two vectors are close to each other.

        Args:
            other: the other vector to compare to.
            tol: the tolerance to compare to.

        Returns:
            true if both vectors are close to each other (within tol), false otherwise.

        Raises:
            TypeError: If other is not a Vector.
            ValueError: If tol is not non-negative.
        """
        if not isinstance(other,Vector):
            raise TypeError(f"other must be Vector, got {type(other).__name__}")
        tol = _validate_real(tol, "tol")
        if tol < 0:
            raise ValueError(f"tol must be non-negative, got {tol}")
        return self.distance(other) <= tol

    def __repr__(self):
        return f"Vector({self._x},{self._y},{self._z})"

    def __str__(self):
        return f"({self._x},{self._y},{self._z})"

