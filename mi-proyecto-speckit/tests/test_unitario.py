"""Tests unitarios generados según lo especificado en test-spec.md."""

import pytest
from src.converter import convert
from src.models import (
    AbsoluteZeroViolationError,
    InvalidTemperatureValueError,
)


def test_convert_celsius_to_fahrenheit():
    """convert: dado 25 en Celsius a Fahrenheit, debe devolver 77.00"""
    result = convert(25, "Celsius", "Fahrenheit")
    assert result == 77.00


def test_convert_celsius_to_kelvin():
    """convert: dado 100 en Celsius a Kelvin, debe devolver 373.15"""
    result = convert(100, "Celsius", "Kelvin")
    assert result == 373.15


def test_convert_same_unit_celsius():
    """convert: con la misma unidad de origen y destino (25 C a C), debe devolver 25.00"""
    result = convert(25, "C", "C")
    assert result == 25.00


def test_convert_invalid_text_input():
    """convert: con texto en vez de numero (por ejemplo 'abc'), debe dar un error claro y controlado, no una excepcion sin manejar"""
    with pytest.raises(InvalidTemperatureValueError) as exc_info:
        convert("abc", "C", "F")
    assert "número válido" in str(exc_info.value).lower()


def test_convert_kelvin_below_zero():
    """convert: con una temperatura en Kelvin menor a 0, debe rechazarla con un mensaje de error"""
    with pytest.raises(AbsoluteZeroViolationError) as exc_info:
        convert(-1, "K", "C")
    assert "kelvin no puede ser menor a 0" in str(exc_info.value).lower()


def test_convert_negative_forty_celsius_to_fahrenheit():
    """convert: con -40 en Celsius a Fahrenheit, debe devolver -40.00"""
    result = convert(-40, "Celsius", "Fahrenheit")
    assert result == -40.00
