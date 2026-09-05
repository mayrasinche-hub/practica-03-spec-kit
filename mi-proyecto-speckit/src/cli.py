"""Módulo de interfaz de línea de comandos (CLI) para el conversor de temperatura."""

from __future__ import annotations

import argparse
import io
import sys

# Asegurar codificación UTF-8 para símbolos como °C y °F en cualquier plataforma
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, io.UnsupportedOperation):
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, io.UnsupportedOperation):
        pass

from src.converter import execute_conversion
from src.models import TemperatureConverterError


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos para la línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="tempconv",
        description="Conversor de temperatura entre Celsius, Fahrenheit y Kelvin.",
    )

    # Argumentos posicionales opcionales
    parser.add_argument(
        "pos_value",
        nargs="?",
        default=None,
        metavar="VALOR",
        help="Valor numérico de la temperatura a convertir.",
    )
    parser.add_argument(
        "pos_from_unit",
        nargs="?",
        default=None,
        metavar="ORIGEN",
        help="Unidad de origen (C, F, K o Celsius, Fahrenheit, Kelvin).",
    )
    parser.add_argument(
        "pos_to_unit",
        nargs="?",
        default=None,
        metavar="DESTINO",
        help="Unidad de destino (C, F, K o Celsius, Fahrenheit, Kelvin).",
    )

    # Argumentos nombrados alternativos
    parser.add_argument(
        "-v",
        "--value",
        dest="opt_value",
        default=None,
        help="Valor numérico de la temperatura.",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="opt_from_unit",
        default=None,
        help="Unidad de origen.",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="opt_to_unit",
        default=None,
        help="Unidad de destino.",
    )

    return parser


def run_interactive_mode() -> int:
    """Ejecuta el flujo interactivo solicitando los datos paso a paso."""
    try:
        raw_val = input("Ingrese el valor de temperatura: ")
        raw_from = input("Ingrese la unidad de origen (C/F/K): ")
        raw_to = input("Ingrese la unidad de destino (C/F/K): ")

        result = execute_conversion(raw_val, raw_from, raw_to)
        print(result.formatted_result)
        return 0
    except (TemperatureConverterError, ValueError) as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1
    except (KeyboardInterrupt, EOFError):
        sys.stderr.write("\nOperación cancelada por el usuario.\n")
        return 1


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada principal para la aplicación de consola."""
    if argv is None:
        argv = sys.argv[1:]

    # Si no se proporcionan argumentos y la entrada estándar está conectada a una terminal o interactivo
    if not argv:
        return run_interactive_mode()

    parser = build_parser()
    args = parser.parse_args(argv)

    value_str = args.pos_value if args.pos_value is not None else args.opt_value
    from_unit_str = args.pos_from_unit if args.pos_from_unit is not None else args.opt_from_unit
    to_unit_str = args.pos_to_unit if args.pos_to_unit is not None else args.opt_to_unit

    # Si se especificaron argumentos parciales de forma posicional o con flags
    if value_str is None or from_unit_str is None or to_unit_str is None:
        sys.stderr.write(
            "Error: Debe proporcionar el valor, la unidad de origen y la unidad de destino.\n"
        )
        parser.print_usage(sys.stderr)
        return 2

    try:
        result = execute_conversion(value_str, from_unit_str, to_unit_str)
        print(result.formatted_result)
        return 0
    except (TemperatureConverterError, ValueError) as err:
        sys.stderr.write(f"Error: {err}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
