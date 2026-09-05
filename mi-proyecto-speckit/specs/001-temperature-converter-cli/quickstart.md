# Quickstart & Validation Guide: Conversor de Temperatura CLI

**Feature**: Conversor de Temperatura CLI (`001-temperature-converter-cli`)  
**Purpose**: Guía de ejecución y validación rápida end-to-end de la herramienta CLI.  

---

## Prerrequisitos

- Python 3.10 o superior instalado (`python --version`).
- Ninguna dependencia externa requerida (usa biblioteca estándar).

---

## 1. Validación de Pruebas Automatizadas

Ejecutar la suite completa de pruebas unitarias y de contrato utilizando el ejecutor nativo `unittest`:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

**Resultado esperado**:
- Todas las pruebas deben finalizar en estado `OK` (conversiones, límites físicos de cero absoluto, errores de validación y contratos CLI).

---

## 2. Escenarios de Validación Manual End-to-End

### Escenario 1: Conversiones Estándar (C, F, K)
Probar la conversión bidireccional entre escalas y la misma unidad de origen y destino:

```bash
# Celsius a Fahrenheit
python -m src.cli 0 C F
# Esperado: 32.00 °F

# Celsius a Kelvin
python -m src.cli 100 C K
# Esperado: 373.15 K

# Fahrenheit a Celsius
python -m src.cli 98.6 F C
# Esperado: 37.00 °C

# Kelvin a Fahrenheit
python -m src.cli 300 K F
# Esperado: 80.33 °F

# Misma unidad (reflexivo)
python -m src.cli 25.5 C C
# Esperado: 25.50 °C
```

### Escenario 2: Temperaturas Negativas Válidas y Límite Físico de Cero Absoluto
Verificar el soporte de negativos válidos y el rechazo estricto de valores bajo cero absoluto:

```bash
# Negativo válido (C a F)
python -m src.cli -40 C F
# Esperado: -40.00 °F

# Negativo válido (F a C)
python -m src.cli -10 F C
# Esperado: -23.33 °C

# Rechazo de Kelvin < 0
python -m src.cli -5 K C
# Esperado (stderr): Error: La temperatura en Kelvin no puede ser menor a 0.
# Código de salida: 1

# Rechazo de Celsius < -273.15
python -m src.cli -300 C K
# Esperado (stderr): Error: La temperatura no puede ser inferior al cero absoluto (-273.15 °C).
# Código de salida: 1
```

### Escenario 3: Manejo de Entradas Inválidas
Verificar la resiliencia ante errores tipográficos o entradas vacías:

```bash
# Entrada no numérica
python -m src.cli abc C F
# Esperado (stderr): Error: El valor de temperatura debe ser un número válido.
# Código de salida: 1

# Unidad desconocida
python -m src.cli 100 X F
# Esperado (stderr): Error: Unidad no reconocida 'X'. Unidades válidas: Celsius (C), Fahrenheit (F), Kelvin (K).
# Código de salida: 1
```

### Escenario 4: Modo Interactivo
Ejecutar la herramienta sin argumentos e interactuar paso a paso con los prompts en consola:

```bash
python -m src.cli
```

---

## Referencias

- [spec.md](./spec.md) - Especificación de Requerimientos y Criterios de Éxito.
- [data-model.md](./data-model.md) - Entidades y Reglas del Dominio.
- [contracts/cli-contract.md](./contracts/cli-contract.md) - Especificación técnica formal de la interfaz CLI.
