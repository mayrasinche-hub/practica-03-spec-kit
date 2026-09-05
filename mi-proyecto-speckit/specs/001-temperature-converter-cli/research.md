# Technical Research: Conversor de Temperatura CLI

**Feature**: Conversor de Temperatura CLI (`001-temperature-converter-cli`)  
**Date**: 2026-09-05  
**Status**: Completed  

---

## 1. CLI Parsing & Interactive Mode Strategy

### Decision
Utilizar el módulo estándar `argparse` de Python para el procesamiento de argumentos de línea de comandos posicionales/nombrados (`--value`, `--from`, `--to` y argumentos posicionales abreviados), implementando una rutina de entrada interactiva (`input()`) cuando el usuario invoque el comando sin argumentos o solicite modo interactivo.

### Rationale
- `argparse` está integrado en la biblioteca estándar de Python (sin requerir dependencias de terceros como `click` o `typer`).
- Genera de forma nativa mensajes de ayuda (`--help`) y manejo de sintaxis consistente.
- Cumple con el criterio de éxito SC-004: permite tanto la ejecución en una sola línea de comandos como el flujo interactivo guiado paso a paso.

### Alternatives Considered
- **`click` o `typer`**: Bibliotecas robustas de CLI pero requieren instalación externa (`pip install`), lo que añade fricción de empaquetado y configuración para una herramienta utilitaria ligera.
- **`sys.argv` manual**: Demasiado propenso a errores, requeriría reimplementar validación de banderas y generación de ayuda manualmente.

---

## 2. Cálculo Numérico y Estrategia de Redondeo

### Decision
Utilizar operaciones aritméticas con tipo `float` de precisión estándar de Python para los cálculos termodinámicos intermedios, aplicando redondeo a 2 cifras decimales con `round(resultado, 2)` y formateo de salida con `f"{resultado:.2f}"`.

### Rationale
- El requerimiento explícito es redondear el resultado a 2 decimales (`FR-002`, `SC-001`).
- Las conversiones térmicas (sumas, restas y multiplicaciones por ratios fraccionarios como 9/5 o 5/9) no presentan problemas críticos de acumulación de error de coma flotante cuando se redondean a 2 posiciones decimales.
- El formateo con `:.2f` asegura que números enteros o con un solo decimal muestren siempre dos dígitos fraccionarios (ej. `32.00`, `25.50`), cumpliendo los escenarios de aceptación.

### Alternatives Considered
- **`decimal.Decimal`**: Ofrece precisión decimal exacta, pero para fórmulas lineales simples de temperatura añade complejidad innecesaria en la conversión de tipos sin aportar beneficios medibles sobre el redondeo a 2 cifras decimales.

---

## 3. Fórmulas de Conversión y Validación del Cero Absoluto

### Decision
Adoptar la escala Celsius como pivote canónico interno de conversión:
1. **Unidad Origen → Celsius**:
   - Celsius: $C = C$
   - Fahrenheit: $C = (F - 32) \times \frac{5}{9}$
   - Kelvin: $C = K - 273.15$
2. **Celsius → Unidad Destino**:
   - Celsius: $C$
   - Fahrenheit: $F = C \times \frac{9}{5} + 32$
   - Kelvin: $K = C + 273.15$
3. **Validación de Cero Absoluto**:
   - Validar en la unidad de entrada antes de la conversión:
     - Si unidad es Kelvin y $K < 0$: Error inmediato ("Kelvin no puede ser menor a 0").
     - Si unidad es Celsius y $C < -273.15$: Error de cero absoluto ("Temperatura inferior al cero absoluto (-273.15 °C)").
     - Si unidad es Fahrenheit y $F < -459.67$: Error de cero absoluto ("Temperatura inferior al cero absoluto (-459.67 °F)").

### Rationale
- Cumple directamente con los requerimientos `FR-004`, `FR-005`, `FR-006` y los escenarios de aceptación de User Story 2.
- Al validar en la entrada original, se proporcionan mensajes de error claros y específicos en la escala que el usuario introdujo.
- El pivote en Celsius reduce la matriz de conversión de $3 \times 3 = 9$ fórmulas específicas a 2 funciones por unidad ($3 + 3 = 6$ pasos).

### Alternatives Considered
- **Fórmulas directas pares a pares (F→K, K→F directos)**: Incrementa el código duplicado y potenciales inconsistencias de redondeo entre rutas.

---

## 4. Normalización y Representación de Unidades

### Decision
Definir una enumeración `TemperatureUnit(Enum)` con valores `CELSIUS`, `FAHRENHEIT`, `KELVIN` y una función de parseo que normalice cadenas ignorando mayúsculas, minúsculas y espacios:
- Celsius: `"c"`, `"celsius"`, `"°c"`
- Fahrenheit: `"f"`, `"fahrenheit"`, `"°f"`
- Kelvin: `"k"`, `"kelvin"`

### Rationale
- Resuelve `FR-009`: aceptación indistinta de iniciales o nombres completos.
- Mantiene la seguridad de tipos en la lógica de negocio y encapsula los símbolos de presentación (`°C`, `°F`, `K`).

### Alternatives Considered
- **Uso directo de cadenas de texto sin validar**: Propenso a errores tipográficos y dificulta el manejo de sinónimos.

---

## 5. Manejo de Errores y Códigos de Salida

### Decision
- **Salida exitosa**: Imprimir resultado en `stdout` con código de salida `0`.
- **Errores de validación** (entrada vacía, no numérica, unidad inválida, violación de cero absoluto): Imprimir mensaje explicativo en `stderr` con código de salida `1` (o `2` en caso de error de sintaxis de argumentos en CLI).

### Rationale
- Convención Unix / POSIX estándar para herramientas de línea de comandos.
- Permite la composición de la herramienta en scripts o pipelines (redirección limpia de salida y captura de errores).

### Alternatives Considered
- **Capturar errores y salir con código 0**: Mala práctica en utilitarios CLI porque las herramientas automatizadas no detectarían los fallos.

---

## 6. Estrategia de Pruebas

### Decision
Utilizar el framework `unittest` de la biblioteca estándar de Python, estructurado de forma modular en el directorio `tests/`:
- `tests/unit/test_converter.py`: Pruebas de conversión matemática, redondeo y reflexividad.
- `tests/unit/test_validators.py`: Pruebas de cero absoluto, valores no numéricos y entradas vacías.
- `tests/contract/test_cli_contract.py`: Pruebas de contrato de interfaz CLI (argumentos, códigos de salida, stdout/stderr).

Compatible de forma nativa con `pytest` si se instala en el entorno.

### Rationale
- Cero dependencias externas necesarias para ejecutar la suite de pruebas (`python -m unittest discover tests`).
- Cumple con el principio de Test-First de la constitución del proyecto.
