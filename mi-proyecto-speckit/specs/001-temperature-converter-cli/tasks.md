# Tasks: Conversor de Temperatura CLI

**Feature**: Conversor de Temperatura CLI (`001-temperature-converter-cli`)  
**Input**: Feature specification from `specs/001-temperature-converter-cli/spec.md` and architecture plan from `specs/001-temperature-converter-cli/plan.md`  
**Status**: Implemented & Verified  

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Inicialización del proyecto y estructura base de directorios y módulos.

- [X] T001 Create project directory structure for `src/` and `tests/` (`tests/unit/`, `tests/contract/`)
- [X] T002 Initialize package module files `src/__init__.py`, `tests/__init__.py`, `tests/unit/__init__.py`, and `tests/contract/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Componentes transversales del modelo de datos y validaciones base requeridos por todas las historias de usuario.

**⚠️ CRITICAL**: Ninguna historia de usuario puede implementarse hasta completar esta fase fundacional.

- [X] T003 Define `TemperatureUnit` enum with symbols, canonical names, aliases, and absolute zero constants in `src/models.py`
- [X] T004 [P] Define `TemperatureReading`, `ConversionRequest`, and `ConversionResult` dataclasses in `src/models.py`
- [X] T005 Implement unit alias parsing and normalization function `parse_unit` in `src/models.py`

**Checkpoint**: Base del modelo de datos lista. La implementación de historias de usuario puede comenzar.

---

## Phase 3: User Story 1 - Conversión Bidireccional entre Escalas Térmicas (Priority: P1) 🎯 MVP

**Goal**: Permitir la conversión bidireccional entre Celsius, Fahrenheit y Kelvin (incluyendo conversiones reflexivas de la misma unidad origen y destino), redondeando el resultado a 2 decimales.

**Independent Test**: Ejecutar `python -m unittest tests/unit/test_converter.py` y validar conversiones por consola de C→F (`0 C F` → `32.00 °F`), C→K (`100 C K` → `373.15 K`), F→C (`98.6 F C` → `37.00 °C`), K→F (`300 K F` → `80.33 °F`) y C→C (`25.5 C C` → `25.50 °C`).

### Tests for User Story 1 (Test-First) 🧪

> **NOTE: Escribir estas pruebas primero y verificar que fallen antes de implementar la funcionalidad.**

- [X] T006 [P] [US1] Write unit tests for standard and reflexive conversion formulas with 2 decimal precision in `tests/unit/test_converter.py`
- [X] T007 [P] [US1] Write CLI contract tests for successful conversion invocations in `tests/contract/test_cli_contract.py`

### Implementation for User Story 1

- [X] T008 [US1] Implement core conversion formulas (`to_celsius`, `from_celsius`, `convert_temperature`) with 2 decimal rounding in `src/converter.py`
- [X] T009 [US1] Implement CLI argument parsing and standard output formatting in `src/cli.py`

**Checkpoint**: User Story 1 (MVP) completamente funcional y verificable de manera autónoma.

---

## Phase 4: User Story 2 - Validación de Límites Físicos y Temperaturas Negativas Válidas (Priority: P2)

**Goal**: Rechazar temperaturas por debajo del cero absoluto (Kelvin < 0, Celsius < -273.15, Fahrenheit < -459.67) con mensajes de error explícitos, garantizando al mismo tiempo el cálculo de temperaturas negativas válidas.

**Independent Test**: Ejecutar `python -m unittest tests/unit/test_validators.py` y verificar por CLI conversiones con negativos válidos (`-40 C F` → `-40.00 °F`, `-10 F C` → `-23.33 °C`) y rechazo de valores bajo cero absoluto (`-5 K C`, `-300 C K`) saliendo con código 1 y mensaje en stderr.

### Tests for User Story 2 (Test-First) 🧪

- [X] T010 [P] [US2] Write unit tests for physical limits (Kelvin < 0 rejection, absolute zero boundaries, and valid negative values) in `tests/unit/test_validators.py`
- [X] T011 [P] [US2] Write CLI contract tests verifying error output to stderr and exit code 1 on absolute zero violations in `tests/contract/test_cli_contract.py`

### Implementation for User Story 2

- [X] T012 [US2] Implement physical limit validation (`validate_absolute_zero`) in `src/converter.py`
- [X] T013 [US2] Connect physical limit validation and error reporting to stderr with exit code 1 in `src/cli.py`

**Checkpoint**: User Stories 1 y 2 integradas y funcionando conjuntamente.

---

## Phase 5: User Story 3 - Manejo Resiliente de Entradas Inválidas y Guía de Uso (Priority: P3)

**Goal**: Manejar robustamente entradas no numéricas, cadenas vacías, unidades no reconocidas y proveer modo interactivo cuando no se suministren argumentos.

**Independent Test**: Ejecutar pruebas de validación y comprobar que entradas vacías (`""`), no numéricas (`"abc"`) o unidades desconocidas (`"X"`) emitan mensajes de error legibles en stderr y que la invocación sin argumentos inicie el modo interactivo.

### Tests for User Story 3 (Test-First) 🧪

- [X] T014 [P] [US3] Write unit tests for input parsing errors (empty strings, non-numeric strings, unrecognized unit names) in `tests/unit/test_validators.py`
- [X] T015 [P] [US3] Write contract tests for CLI input error handling and interactive mode prompts in `tests/contract/test_cli_contract.py`

### Implementation for User Story 3

- [X] T016 [US3] Implement input validation logic (`validate_numeric_input`, `validate_unit_string`) in `src/converter.py`
- [X] T017 [US3] Implement interactive prompt fallback (`run_interactive_mode`) and user-friendly error formatting in `src/cli.py`

**Checkpoint**: Todas las historias de usuario implementadas y protegidas contra fallos de entrada.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Mejoras de calidad, documentación interna y validación general end-to-end.

- [X] T018 [P] Add top-level package docstrings and typing annotations across `src/models.py`, `src/converter.py`, and `src/cli.py`
- [X] T019 Run complete test suite and execute validation scenarios from `specs/001-temperature-converter-cli/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias previas; inicia inmediatamente.
- **Foundational (Phase 2)**: Depende de Phase 1; BLOQUEA la implementación de las historias de usuario.
- **User Stories (Phases 3, 4, 5)**: Dependen de la finalización de Foundational (Phase 2).
  - Pueden ejecutarse secuencialmente en orden de prioridad (P1 → P2 → P3) o en paralelo si hay múltiples desarrolladores.
- **Polish (Phase 6)**: Depende de la finalización de todas las historias de usuario deseadas.

### User Story Dependencies

- **User Story 1 (P1)**: Puede iniciar inmediatamente tras la Fase Fundacional. Define el núcleo de conversión y CLI.
- **User Story 2 (P2)**: Extiende la lógica de conversión agregando validación del cero absoluto. No bloquea US1.
- **User Story 3 (P3)**: Extiende la capa CLI y el parseo de entrada para brindar resiliencia y modo interactivo.

### Within Each User Story

- Las pruebas unitarias y de contrato (`[P]`) deben crearse primero y fallar antes de escribir la implementación (TDD).
- Las funciones de dominio en `src/converter.py` se implementan antes de la integración en la interfaz CLI en `src/cli.py`.
- Cada historia de usuario debe quedar validada de forma autónoma antes de pasar a la siguiente.

---

## Parallel Execution Examples

### Parallel Example: User Story 1
```bash
# Ejecución en paralelo de pruebas iniciales TDD:
Task: "T006 [P] [US1] Write unit tests for standard and reflexive conversion formulas with 2 decimal precision in tests/unit/test_converter.py"
Task: "T007 [P] [US1] Write CLI contract tests for successful conversion invocations in tests/contract/test_cli_contract.py"
```

### Parallel Example: User Story 2
```bash
# Ejecución en paralelo de pruebas de límites físicos:
Task: "T010 [P] [US2] Write unit tests for physical limits (Kelvin < 0 rejection, absolute zero boundaries, and valid negative values) in tests/unit/test_validators.py"
Task: "T011 [P] [US2] Write CLI contract tests verifying error output to stderr and exit code 1 on absolute zero violations in tests/contract/test_cli_contract.py"
```

---

## Implementation Strategy

### 1. MVP First (Foco en User Story 1)
1. Completar **Phase 1: Setup** (T001, T002).
2. Completar **Phase 2: Foundational** (T003, T004, T005).
3. Implementar y validar **Phase 3: User Story 1** (T006 a T009).
4. **Validar MVP**: Comprobar conversiones básicas redondeadas a 2 decimales.

### 2. Entrega Incremental
1. Base funcional lista (MVP).
2. Incorporar **User Story 2**: Validación de cero absoluto y negativos válidos (T010 a T013).
3. Incorporar **User Story 3**: Resiliencia de entrada y modo interactivo (T014 a T017).
4. **Fase de Pulido** y verificación global con `quickstart.md` (T018, T019).
