"""Pruebas unitarias para las fórmulas de conversión de temperatura."""

import unittest
from src.models import TemperatureReading, TemperatureUnit, ConversionResult
from src.converter import convert_temperature, to_celsius, from_celsius


class TestTemperatureConverter(unittest.TestCase):
    """Casos de prueba para conversiones entre Celsius, Fahrenheit y Kelvin."""

    def test_celsius_to_fahrenheit(self):
        reading = TemperatureReading(value=0.0, unit=TemperatureUnit.CELSIUS)
        result = convert_temperature(reading, TemperatureUnit.FAHRENHEIT)
        self.assertEqual(result.converted_value, 32.00)
        self.assertEqual(result.formatted_result, "32.00 °F")
        self.assertFalse(result.is_reflexive)

        reading_100 = TemperatureReading(value=100.0, unit=TemperatureUnit.CELSIUS)
        result_100 = convert_temperature(reading_100, TemperatureUnit.FAHRENHEIT)
        self.assertEqual(result_100.converted_value, 212.00)
        self.assertEqual(result_100.formatted_result, "212.00 °F")

    def test_celsius_to_kelvin(self):
        reading = TemperatureReading(value=100.0, unit=TemperatureUnit.CELSIUS)
        result = convert_temperature(reading, TemperatureUnit.KELVIN)
        self.assertEqual(result.converted_value, 373.15)
        self.assertEqual(result.formatted_result, "373.15 K")

        reading_zero = TemperatureReading(value=0.0, unit=TemperatureUnit.CELSIUS)
        result_zero = convert_temperature(reading_zero, TemperatureUnit.KELVIN)
        self.assertEqual(result_zero.converted_value, 273.15)

    def test_fahrenheit_to_celsius(self):
        reading = TemperatureReading(value=98.6, unit=TemperatureUnit.FAHRENHEIT)
        result = convert_temperature(reading, TemperatureUnit.CELSIUS)
        self.assertEqual(result.converted_value, 37.00)
        self.assertEqual(result.formatted_result, "37.00 °C")

        reading_32 = TemperatureReading(value=32.0, unit=TemperatureUnit.FAHRENHEIT)
        result_32 = convert_temperature(reading_32, TemperatureUnit.CELSIUS)
        self.assertEqual(result_32.converted_value, 0.00)

    def test_kelvin_to_fahrenheit(self):
        reading = TemperatureReading(value=300.0, unit=TemperatureUnit.KELVIN)
        result = convert_temperature(reading, TemperatureUnit.FAHRENHEIT)
        self.assertEqual(result.converted_value, 80.33)
        self.assertEqual(result.formatted_result, "80.33 °F")

    def test_kelvin_to_celsius(self):
        reading = TemperatureReading(value=273.15, unit=TemperatureUnit.KELVIN)
        result = convert_temperature(reading, TemperatureUnit.CELSIUS)
        self.assertEqual(result.converted_value, 0.00)
        self.assertEqual(result.formatted_result, "0.00 °C")

    def test_reflexive_conversions(self):
        reading_c = TemperatureReading(value=25.5, unit=TemperatureUnit.CELSIUS)
        result_c = convert_temperature(reading_c, TemperatureUnit.CELSIUS)
        self.assertEqual(result_c.converted_value, 25.50)
        self.assertEqual(result_c.formatted_result, "25.50 °C")
        self.assertTrue(result_c.is_reflexive)

        reading_f = TemperatureReading(value=72.4, unit=TemperatureUnit.FAHRENHEIT)
        result_f = convert_temperature(reading_f, TemperatureUnit.FAHRENHEIT)
        self.assertEqual(result_f.converted_value, 72.40)
        self.assertTrue(result_f.is_reflexive)

        reading_k = TemperatureReading(value=310.2, unit=TemperatureUnit.KELVIN)
        result_k = convert_temperature(reading_k, TemperatureUnit.KELVIN)
        self.assertEqual(result_k.converted_value, 310.20)
        self.assertTrue(result_k.is_reflexive)


if __name__ == "__main__":
    unittest.main()
