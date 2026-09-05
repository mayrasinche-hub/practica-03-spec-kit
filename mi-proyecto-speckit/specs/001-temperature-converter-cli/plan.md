# Implementation Plan: Conversor de Temperatura CLI

**Branch**: `001-temperature-converter-cli` | **Date**: 2026-09-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-temperature-converter-cli/spec.md`

## Summary

Desarrollar una herramienta de línea de comandos en Python para convertir valores térmicos bidireccionalmente entre las escalas Celsius, Fahrenheit y Kelvin. La solución utiliza un diseño desacoplado: una biblioteca base con el modelo de dominio y lógica de conversión termodinámica (pivote en Celsius, redondeo a 2 decimales y control estricto del cero absoluto) y un adaptador CLI construido con `argparse` que soporta invocación directa posicional/nombrada y un modo interactivo asistido.

## Technical Context

**Language/Version**: Python 3.11 (compatible con Python >= 3.10)

**Primary Dependencies**: Ninguna dependencia externa requerida (Biblioteca estándar: `argparse`, `dataclasses`, `enum`, `sys`, `math`).

**Storage**: N/A (Herramienta de consola sin estado / stateless).

**Testing**: `unittest` (nativo de Python, compatible con `pytest`).

**Target Platform**: Multiplataforma (Windows, Linux, macOS).

**Project Type**: CLI Application / Modular Library.

**Performance Goals**: Tiempo de inicio y respuesta menor a 100 ms por conversión.

**Constraints**: Ejecución 100% offline, cero dependencias en tiempo de ejecución (`zero dependencies`), rechazo riguroso de temperaturas inferiores al cero absoluto.

**Scale/Scope**: Módulo autocontenido (~300-500 líneas de código totales entre lógica, CLI y pruebas).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Library-First**: PASA. La lógica de conversión se encapsula en `src/converter.py` y `src/models.py`, completamente independiente de la interfaz de consola, haciéndola reusable y testeable por separado.
- **II. CLI Interface**: PASA. Se implementa un protocolo claro con argumentos posicionales, banderas opcionales, modo interactivo, salida de resultados formateados en `stdout`, mensajes de error en `stderr` y códigos de retorno POSIX.
- **III. Test-First**: PASA. Se define suite de pruebas estructurada en `tests/unit/` y `tests/contract/` para cubrir fórmulas, límites físicos de cero absoluto y contratos CLI.
- **IV. Simplicity**: PASA. Se aprovecha la biblioteca estándar de Python sin añadir dependencias externas innecesarias (`YAGNI`).

## Project Structure

### Documentation (this feature)

```text
specs/001-temperature-converter-cli/
├── plan.md              # Plan de implementación (/speckit-plan)
├── research.md          # Decisiones técnicas y análisis (/speckit-plan)
├── data-model.md        # Entidades, tipos y validaciones (/speckit-plan)
├── quickstart.md        # Guía de ejecución y validación (/speckit-plan)
├── contracts/           # Contratos de interfaz (/speckit-plan)
│   └── cli-contract.md
└── tasks.md             # Tareas de implementación (/speckit-tasks - siguiente fase)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models.py            # Enumeraciones y estructuras de datos (TemperatureUnit, TemperatureReading)
├── converter.py         # Fórmulas termodinámicas, validaciones físicas y redondeo
└── cli.py               # Punto de entrada de consola, argparse y modo interactivo

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_converter.py    # Pruebas unitarias de fórmulas y redondeo
│   └── test_validators.py   # Pruebas de cero absoluto, vacíos y tipos no numéricos
└── contract/
    ├── __init__.py
    └── test_cli_contract.py # Pruebas de flags CLI, stdout, stderr y exit codes
```

**Structure Decision**:
Se adopta la arquitectura de proyecto modular estándar (Opción 1: Single project). Se garantiza la separación estricta entre el núcleo de cálculo (`src/converter.py`), el modelo de datos (`src/models.py`) y la capa de transporte/interacción CLI (`src/cli.py`).

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| *Ninguna* | No aplica | El diseño se mantiene minimalista y sin dependencias externas |
