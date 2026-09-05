"""Modelos de datos y enumeraciones para el conversor de temperatura."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Set


class TemperatureConverterError(ValueError):
    """Excepción base para errores del conversor de temperatura."""


class InvalidUnitError(TemperatureConverterError):
    """Excepción lanzada cuando una unidad no es válida o reconocida."""


class InvalidTemperatureValueError(TemperatureConverterError):
    """Excepción lanzada cuando el valor de entrada no es numérico o está vacío."""


class AbsoluteZeroViolationError(TemperatureConverterError):
    """Excepción lanzada cuando una temperatura está por debajo del cero absoluto."""


class TemperatureUnit(Enum):
    """Escalas termodinámicas de temperatura soportadas."""

    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    KELVIN = "kelvin"

    @property
    def symbol(self) -> str:
        """Símbolo de la unidad para visualización."""
        if self == TemperatureUnit.CELSIUS:
            return "°C"
        elif self == TemperatureUnit.FAHRENHEIT:
            return "°F"
        return "K"

    @property
    def canonical_name(self) -> str:
        """Nombre canónico en español."""
        if self == TemperatureUnit.CELSIUS:
            return "Celsius"
        elif self == TemperatureUnit.FAHRENHEIT:
            return "Fahrenheit"
        return "Kelvin"

    @property
    def absolute_zero(self) -> float:
        """Límite inferior físico de la escala (cero absoluto)."""
        if self == TemperatureUnit.CELSIUS:
            return -273.15
        elif self == TemperatureUnit.FAHRENHEIT:
            return -459.67
        return 0.0

    @property
    def aliases(self) -> Set[str]:
        """Alias admitidos para reconocer la unidad."""
        if self == TemperatureUnit.CELSIUS:
            return {"c", "celsius", "°c", "centigrado", "centigrados"}
        elif self == TemperatureUnit.FAHRENHEIT:
            return {"f", "fahrenheit", "°f"}
        return {"k", "kelvin"}


def parse_unit(raw: str | None) -> TemperatureUnit:
    """Normaliza y convierte una cadena de texto en una unidad TemperatureUnit."""
    if raw is None or not str(raw).strip():
        raise InvalidUnitError("La unidad de temperatura no puede estar vacía.")

    cleaned = str(raw).strip().lower()

    for unit in TemperatureUnit:
        if cleaned in unit.aliases:
            return unit

    raise InvalidUnitError(
        f"Unidad no reconocida '{raw}'. Unidades válidas: Celsius (C), Fahrenheit (F), Kelvin (K)."
    )


@dataclass(frozen=True)
class TemperatureReading:
    """Representa una lectura de temperatura compuesta por magnitud y unidad."""

    value: float
    unit: TemperatureUnit

    def validate_physical_limit(self) -> None:
        """Valida que la temperatura respete el límite del cero absoluto."""
        if not math.isfinite(self.value):
            raise InvalidTemperatureValueError("El valor de temperatura debe ser un número real finito.")

        if self.unit == TemperatureUnit.KELVIN and self.value < 0.0:
            raise AbsoluteZeroViolationError("La temperatura en Kelvin no puede ser menor a 0.")

        if self.unit == TemperatureUnit.CELSIUS and self.value < -273.15:
            raise AbsoluteZeroViolationError(
                "La temperatura no puede ser inferior al cero absoluto (-273.15 °C)."
            )

        if self.unit == TemperatureUnit.FAHRENHEIT and self.value < -459.67:
            raise AbsoluteZeroViolationError(
                "La temperatura no puede ser inferior al cero absoluto (-459.67 °F)."
            )


@dataclass(frozen=True)
class ConversionRequest:
    """Petición de conversión de temperatura con valores sin procesar."""

    raw_value: str
    source_unit_raw: str
    target_unit_raw: str

    def parse(self) -> tuple[TemperatureReading, TemperatureUnit]:
        """Valida las cadenas de entrada y retorna la lectura de origen y unidad destino."""
        if self.raw_value is None or not str(self.raw_value).strip():
            raise InvalidTemperatureValueError("El valor de temperatura no puede estar vacío.")

        try:
            numeric_value = float(self.raw_value.strip())
        except ValueError as exc:
            raise InvalidTemperatureValueError(
                "El valor de temperatura debe ser un número válido."
            ) from exc

        source_unit = parse_unit(self.source_unit_raw)
        target_unit = parse_unit(self.target_unit_raw)

        reading = TemperatureReading(value=numeric_value, unit=source_unit)
        return reading, target_unit


@dataclass(frozen=True)
class ConversionResult:
    """Resultado final estructurado de una conversión de temperatura."""

    original_reading: TemperatureReading
    target_unit: TemperatureUnit
    converted_value: float
    formatted_result: str
    is_reflexive: bool
