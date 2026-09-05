"""Lógica de conversión termodinámica y validación física de temperatura."""

from __future__ import annotations

import math
from src.models import (
    AbsoluteZeroViolationError,
    ConversionRequest,
    ConversionResult,
    InvalidTemperatureValueError,
    InvalidUnitError,
    TemperatureReading,
    TemperatureUnit,
    parse_unit,
)


def validate_numeric_input(raw_value: str | None) -> float:
    """Valida que la entrada sea una cadena numérica convertible a flotante finito."""
    if raw_value is None or not str(raw_value).strip():
        raise InvalidTemperatureValueError("El valor de temperatura no puede estar vacío.")

    try:
        val = float(str(raw_value).strip())
    except ValueError as exc:
        raise InvalidTemperatureValueError(
            "El valor de temperatura debe ser un número válido."
        ) from exc

    if not math.isfinite(val):
        raise InvalidTemperatureValueError("El valor de temperatura debe ser un número real finito.")

    return val


def validate_unit_string(raw_unit: str | None) -> TemperatureUnit:
    """Valida y normaliza una representación en texto de unidad de temperatura."""
    return parse_unit(raw_unit)


def to_celsius(reading: TemperatureReading) -> float:
    """Convierte una lectura de temperatura a la escala pivote Celsius."""
    if reading.unit == TemperatureUnit.CELSIUS:
        return reading.value
    elif reading.unit == TemperatureUnit.FAHRENHEIT:
        return (reading.value - 32.0) * 5.0 / 9.0
    elif reading.unit == TemperatureUnit.KELVIN:
        return reading.value - 273.15
    raise InvalidUnitError(f"Unidad no soportada: {reading.unit}")


def from_celsius(celsius_value: float, target_unit: TemperatureUnit) -> float:
    """Convierte un valor en grados Celsius a la unidad de destino especificada."""
    if target_unit == TemperatureUnit.CELSIUS:
        return celsius_value
    elif target_unit == TemperatureUnit.FAHRENHEIT:
        return celsius_value * 9.0 / 5.0 + 32.0
    elif target_unit == TemperatureUnit.KELVIN:
        return celsius_value + 273.15
    raise InvalidUnitError(f"Unidad no soportada: {target_unit}")


def validate_absolute_zero(reading: TemperatureReading) -> None:
    """Verifica que la lectura de temperatura no esté por debajo del cero absoluto."""
    reading.validate_physical_limit()


def convert_temperature(
    reading: TemperatureReading, target_unit: TemperatureUnit
) -> ConversionResult:
    """Ejecuta la conversión de temperatura validando límites y redondeando a 2 decimales."""
    validate_absolute_zero(reading)

    is_reflexive = reading.unit == target_unit

    if is_reflexive:
        rounded_value = round(reading.value, 2)
    else:
        celsius_temp = to_celsius(reading)
        target_temp = from_celsius(celsius_temp, target_unit)
        rounded_value = round(target_temp, 2)

    formatted_result = f"{rounded_value:.2f} {target_unit.symbol}"

    return ConversionResult(
        original_reading=reading,
        target_unit=target_unit,
        converted_value=rounded_value,
        formatted_result=formatted_result,
        is_reflexive=is_reflexive,
    )


def execute_conversion(
    raw_value: str, source_unit_raw: str, target_unit_raw: str
) -> ConversionResult:
    """Parsea las entradas del usuario y ejecuta la conversión completa."""
    numeric_value = validate_numeric_input(raw_value)
    source_unit = validate_unit_string(source_unit_raw)
    target_unit = validate_unit_string(target_unit_raw)

    reading = TemperatureReading(value=numeric_value, unit=source_unit)
    return convert_temperature(reading, target_unit)
