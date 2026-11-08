from math import isfinite
from numbers import Real

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
    if not isfinite(result):
        raise ValueError(f"{name} must be finite, got {result}")
    return result
