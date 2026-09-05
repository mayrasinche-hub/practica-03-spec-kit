"""Pruebas unitarias para validaciones de límites físicos y valores de temperatura."""

import unittest
from src.models import (
    AbsoluteZeroViolationError,
    ConversionRequest,
    InvalidTemperatureValueError,
    InvalidUnitError,
    TemperatureReading,
    TemperatureUnit,
    parse_unit,
)
from src.converter import convert_temperature, validate_absolute_zero


class TestPhysicalLimits(unittest.TestCase):
    """Pruebas para temperaturas negativas válidas y límites del cero absoluto."""

    def test_valid_negative_temperatures(self):
        reading_minus_40 = TemperatureReading(value=-40.0, unit=TemperatureUnit.CELSIUS)
        result_minus_40 = convert_temperature(reading_minus_40, TemperatureUnit.FAHRENHEIT)
        self.assertEqual(result_minus_40.converted_value, -40.00)
        self.assertEqual(result_minus_40.formatted_result, "-40.00 °F")

        reading_minus_10 = TemperatureReading(value=-10.0, unit=TemperatureUnit.FAHRENHEIT)
        result_minus_10 = convert_temperature(reading_minus_10, TemperatureUnit.CELSIUS)
        self.assertEqual(result_minus_10.converted_value, -23.33)
        self.assertEqual(result_minus_10.formatted_result, "-23.33 °C")

    def test_absolute_zero_boundary_exact_values(self):
        reading_0k = TemperatureReading(value=0.0, unit=TemperatureUnit.KELVIN)
        result_0k = convert_temperature(reading_0k, TemperatureUnit.CELSIUS)
        self.assertEqual(result_0k.converted_value, -273.15)

        reading_zero_c = TemperatureReading(value=-273.15, unit=TemperatureUnit.CELSIUS)
        result_zero_c = convert_temperature(reading_zero_c, TemperatureUnit.KELVIN)
        self.assertEqual(result_zero_c.converted_value, 0.00)

        reading_zero_f = TemperatureReading(value=-459.67, unit=TemperatureUnit.FAHRENHEIT)
        result_zero_f = convert_temperature(reading_zero_f, TemperatureUnit.KELVIN)
        self.assertEqual(result_zero_f.converted_value, 0.00)

    def test_rejection_kelvin_below_zero(self):
        reading_minus_1k = TemperatureReading(value=-1.0, unit=TemperatureUnit.KELVIN)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            validate_absolute_zero(reading_minus_1k)
        self.assertIn("Kelvin no puede ser menor a 0", str(ctx.exception))

        reading_minus_5k = TemperatureReading(value=-5.0, unit=TemperatureUnit.KELVIN)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            convert_temperature(reading_minus_5k, TemperatureUnit.CELSIUS)
        self.assertIn("Kelvin no puede ser menor a 0", str(ctx.exception))

    def test_rejection_celsius_below_absolute_zero(self):
        reading_invalid_c = TemperatureReading(value=-273.16, unit=TemperatureUnit.CELSIUS)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            validate_absolute_zero(reading_invalid_c)
        self.assertIn("cero absoluto", str(ctx.exception))

        reading_minus_300 = TemperatureReading(value=-300.0, unit=TemperatureUnit.CELSIUS)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            convert_temperature(reading_minus_300, TemperatureUnit.FAHRENHEIT)
        self.assertIn("cero absoluto", str(ctx.exception))

    def test_rejection_fahrenheit_below_absolute_zero(self):
        reading_invalid_f = TemperatureReading(value=-459.68, unit=TemperatureUnit.FAHRENHEIT)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            validate_absolute_zero(reading_invalid_f)
        self.assertIn("cero absoluto", str(ctx.exception))

        reading_minus_500 = TemperatureReading(value=-500.0, unit=TemperatureUnit.FAHRENHEIT)
        with self.assertRaises(AbsoluteZeroViolationError) as ctx:
            convert_temperature(reading_minus_500, TemperatureUnit.KELVIN)
        self.assertIn("cero absoluto", str(ctx.exception))


class TestInputValidation(unittest.TestCase):
    """Pruebas para validación de formatos de entrada, cadenas vacías y tipos de datos."""

    def test_empty_temperature_value(self):
        req_empty = ConversionRequest(raw_value="", source_unit_raw="C", target_unit_raw="F")
        with self.assertRaises(InvalidTemperatureValueError) as ctx:
            req_empty.parse()
        self.assertIn("no puede estar vacío", str(ctx.exception))

        req_spaces = ConversionRequest(raw_value="   ", source_unit_raw="C", target_unit_raw="F")
        with self.assertRaises(InvalidTemperatureValueError):
            req_spaces.parse()

    def test_non_numeric_temperature_value(self):
        invalid_inputs = ["abc", "12a", "cien", "12,50", "!@#"]
        for val in invalid_inputs:
            with self.subTest(val=val):
                req = ConversionRequest(raw_value=val, source_unit_raw="C", target_unit_raw="F")
                with self.assertRaises(InvalidTemperatureValueError) as ctx:
                    req.parse()
                self.assertIn("número válido", str(ctx.exception))

    def test_empty_unit_string(self):
        with self.assertRaises(InvalidUnitError) as ctx:
            parse_unit("")
        self.assertIn("no puede estar vacía", str(ctx.exception))

        with self.assertRaises(InvalidUnitError):
            parse_unit(None)

    def test_unrecognized_unit(self):
        with self.assertRaises(InvalidUnitError) as ctx:
            parse_unit("Rankine")
        self.assertIn("Unidad no reconocida 'Rankine'", str(ctx.exception))

        with self.assertRaises(InvalidUnitError) as ctx:
            parse_unit("X")
        self.assertIn("Unidad no reconocida 'X'", str(ctx.exception))

    def test_unit_normalization_and_aliases(self):
        self.assertEqual(parse_unit("c"), TemperatureUnit.CELSIUS)
        self.assertEqual(parse_unit("C"), TemperatureUnit.CELSIUS)
        self.assertEqual(parse_unit("Celsius"), TemperatureUnit.CELSIUS)
        self.assertEqual(parse_unit("  celsius  "), TemperatureUnit.CELSIUS)
        self.assertEqual(parse_unit("°c"), TemperatureUnit.CELSIUS)

        self.assertEqual(parse_unit("f"), TemperatureUnit.FAHRENHEIT)
        self.assertEqual(parse_unit("F"), TemperatureUnit.FAHRENHEIT)
        self.assertEqual(parse_unit("Fahrenheit"), TemperatureUnit.FAHRENHEIT)
        self.assertEqual(parse_unit("°f"), TemperatureUnit.FAHRENHEIT)

        self.assertEqual(parse_unit("k"), TemperatureUnit.KELVIN)
        self.assertEqual(parse_unit("K"), TemperatureUnit.KELVIN)
        self.assertEqual(parse_unit("kelvin"), TemperatureUnit.KELVIN)


if __name__ == "__main__":
    unittest.main()
