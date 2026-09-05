# Resultados Bloque 3.B — Spec Kit

Proyecto: Conversor de temperatura (mismo de la Parte A)
Framework: GitHub Spec Kit (specify-cli 1.0.5.dev0), integracion agy
Feature: 001-temperature-converter-cli
Comando de invocacion: python -m src.cli <valor> <origen> <destino>

## Los 3 casos de prueba (los mismos del Bloque 3.A)

| Tipo de caso | Comando | Resultado obtenido | Correcto |
|---|---|---|---|
| Normal | python -m src.cli 25 C F | 77.00 grados F | Si |
| Borde de mi spec (Kelvin < 0) | python -m src.cli -5 K C | Error: La temperatura en Kelvin no puede ser menor a 0. | Si |
| No contemplado (Rankine) | python -m src.cli 100 C R | Error: Unidad no reconocida 'R'. Unidades validas: Celsius (C), Fahrenheit (F), Kelvin (K). | Manejado |

## Artefactos generados por el flujo

| Comando | Artefactos |
|---|---|
| /speckit-specify | spec.md, checklists/requirements.md, feature.json |
| /speckit-plan | research.md, data-model.md, contracts/cli-contract.md, quickstart.md, plan.md |
| /speckit-tasks | tasks.md con 19 tareas (T001-T019) en 6 fases con prioridades P1/P2/P3 |
| /speckit-implement | src/models.py, src/converter.py, src/cli.py, src/__init__.py, 3 suites de tests, .gitignore |

## Resultado de la implementacion

- 19 de 19 tareas completadas
- 24 pruebas ejecutadas (unitarias y de contrato CLI), 100% de exito
- Estructura src/ + tests/unit/ + tests/contract/

## Observaciones

1. Aplico TDD: escribio los tests antes de la implementacion y verifico que fallaran primero.
2. Detecto y corrigio por su cuenta un error de codificacion de Windows con los simbolos de grado, reescribiendo cli.py y el test de contrato.
3. Definio un contrato formal de la CLI antes de programar: codigos de salida POSIX, stdout para resultados y stderr para errores.
4. Genero un diagrama de clases Mermaid y un documento de investigacion tecnica para un programa de conversion aritmetica simple.
5. Formato de salida distinto al Bloque 3.A: 77.00 grados F en lugar de 77.0, porque el contrato de interfaz lo definio explicitamente.