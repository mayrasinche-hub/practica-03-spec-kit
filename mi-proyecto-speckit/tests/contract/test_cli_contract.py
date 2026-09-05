"""Pruebas de contrato para la interfaz de línea de comandos (CLI)."""

import os
import subprocess
import sys
import unittest


class TestCliContract(unittest.TestCase):
    """Verifica los contratos de argumentos, salida estándar y códigos de salida de la CLI."""

    def run_cli(self, args, input_data=None):
        """Ejecuta el módulo CLI en un subproceso y captura código de salida, stdout y stderr."""
        cmd = [sys.executable, "-m", "src.cli"] + args
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        return result

    def test_successful_positional_conversions(self):
        cases = [
            (["0", "C", "F"], "32.00 °F"),
            (["100", "C", "K"], "373.15 K"),
            (["98.6", "F", "C"], "37.00 °C"),
            (["300", "K", "F"], "80.33 °F"),
            (["25.5", "C", "C"], "25.50 °C"),
        ]
        for args, expected_output in cases:
            with self.subTest(args=args):
                res = self.run_cli(args)
                self.assertEqual(res.returncode, 0, f"Error ejecutando {args}: {res.stderr}")
                self.assertEqual(res.stdout.strip(), expected_output)

    def test_successful_flag_conversions(self):
        res = self.run_cli(["--value", "0", "--from", "C", "--to", "F"])
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout.strip(), "32.00 °F")

        res_short = self.run_cli(["-v", "100", "-f", "celsius", "-t", "kelvin"])
        self.assertEqual(res_short.returncode, 0)
        self.assertEqual(res_short.stdout.strip(), "373.15 K")

    def test_valid_negative_temperatures_cli(self):
        res_c = self.run_cli(["-40", "C", "F"])
        self.assertEqual(res_c.returncode, 0)
        self.assertEqual(res_c.stdout.strip(), "-40.00 °F")

        res_f = self.run_cli(["-10", "F", "C"])
        self.assertEqual(res_f.returncode, 0)
        self.assertEqual(res_f.stdout.strip(), "-23.33 °C")

    def test_absolute_zero_violations_cli(self):
        # Kelvin < 0
        res_k = self.run_cli(["-5", "K", "C"])
        self.assertEqual(res_k.returncode, 1)
        self.assertIn("Kelvin no puede ser menor a 0", res_k.stderr)

        # Celsius < -273.15
        res_c = self.run_cli(["-300", "C", "F"])
        self.assertEqual(res_c.returncode, 1)
        self.assertIn("cero absoluto", res_c.stderr)

        # Fahrenheit < -459.67
        res_f = self.run_cli(["-500", "F", "K"])
        self.assertEqual(res_f.returncode, 1)
        self.assertIn("cero absoluto", res_f.stderr)

    def test_invalid_and_empty_inputs_cli(self):
        # Entrada no numérica
        res_nan = self.run_cli(["abc", "C", "F"])
        self.assertEqual(res_nan.returncode, 1)
        self.assertIn("número válido", res_nan.stderr)

        # Entrada vacía
        res_empty = self.run_cli(["", "C", "F"])
        self.assertEqual(res_empty.returncode, 1)
        self.assertIn("no puede estar vacío", res_empty.stderr)

        # Unidad no reconocida
        res_unit = self.run_cli(["100", "X", "F"])
        self.assertEqual(res_unit.returncode, 1)
        self.assertIn("Unidad no reconocida 'X'", res_unit.stderr)

    def test_missing_cli_arguments(self):
        res_missing = self.run_cli(["100", "C"])
        self.assertEqual(res_missing.returncode, 2)
        self.assertIn("Debe proporcionar el valor", res_missing.stderr)

    def test_interactive_mode_success(self):
        input_data = "100\nC\nF\n"
        res = self.run_cli([], input_data=input_data)
        self.assertEqual(res.returncode, 0)
        self.assertIn("212.00 °F", res.stdout)

    def test_interactive_mode_error(self):
        input_data = "abc\nC\nF\n"
        res = self.run_cli([], input_data=input_data)
        self.assertEqual(res.returncode, 1)
        self.assertIn("número válido", res.stderr)


if __name__ == "__main__":
    unittest.main()
