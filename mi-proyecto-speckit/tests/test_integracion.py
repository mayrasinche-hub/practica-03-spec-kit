"""Test de integración generado según lo especificado en test-spec.md."""

import subprocess
import sys


def test_cli_flow_celsius_to_fahrenheit():
    """El flujo completo desde la linea de comandos (python -m src.cli 25 C F) hasta la salida final debe imprimir el resultado convertido en stdout y devolver codigo de salida 0."""
    result = subprocess.run(
        [sys.executable, "-m", "src.cli", "25", "C", "F"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "77.00" in result.stdout
    assert "°F" in result.stdout
