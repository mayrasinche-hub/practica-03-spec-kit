"""Paquete conversor de temperatura CLI y biblioteca reutilizable.

Exporta las funciones y modelos principales para realizar conversiones
termodinámicas exactas entre Celsius, Fahrenheit y Kelvin.
"""

from src.models import (
    AbsoluteZeroViolationError,
    ConversionRequest,
    ConversionResult,
    InvalidTemperatureValueError,
    InvalidUnitError,
    TemperatureConverterError,
    TemperatureReading,
    TemperatureUnit,
    parse_unit,
)
from src.converter import (
    convert,
    convert_temperature,
    execute_conversion,
    from_celsius,
    to_celsius,
    validate_absolute_zero,
    validate_numeric_input,
    validate_unit_string,
)

__all__ = [
    "AbsoluteZeroViolationError",
    "ConversionRequest",
    "ConversionResult",
    "InvalidTemperatureValueError",
    "InvalidUnitError",
    "TemperatureConverterError",
    "TemperatureReading",
    "TemperatureUnit",
    "convert",
    "convert_temperature",
    "execute_conversion",
    "from_celsius",
    "parse_unit",
    "to_celsius",
    "validate_absolute_zero",
    "validate_numeric_input",
    "validate_unit_string",
]
