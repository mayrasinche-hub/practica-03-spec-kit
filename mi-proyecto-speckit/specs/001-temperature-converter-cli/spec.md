# Feature Specification: Conversor de Temperatura CLI

**Feature Branch**: `001-temperature-converter-cli`

**Created**: 2026-09-05

**Status**: Draft

**Input**: User description: "Un conversor de temperatura en Python por linea de comandos. Convierte un valor entre Celsius, Fahrenheit y Kelvin en ambos sentidos. Redondea el resultado a 2 decimales. Rechaza una temperatura en Kelvin menor a 0 con un mensaje de error claro. Maneja entrada no numerica, entrada vacia, misma unidad de origen y destino, y valores negativos validos en Celsius y Fahrenheit."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversión Bidireccional entre Escalas Térmicas (Priority: P1)

Como usuario de la interfaz de línea de comandos, deseo convertir un valor de temperatura entre Celsius, Fahrenheit y Kelvin en cualquier dirección (incluyendo conversiones con la misma unidad de origen y destino), obteniendo el resultado numérico redondeado exactamente a 2 decimales, para realizar cálculos térmicos precisos y consistentes.

**Why this priority**: Constituye el núcleo fundamental (MVP) del conversor. Sin la capacidad de realizar conversiones exactas y redondeadas entre las tres escalas, el sistema carece de valor operativo.

**Independent Test**: Puede validarse de forma independiente ejecutando conversiones representativas para cada combinación de unidades (C→F, C→K, F→C, F→K, K→C, K→F, y combinaciones reflexivas C→C, F→F, K→K) con valores positivos y neutros, verificando que los resultados coincidan con las fórmulas estándar redondeadas a 2 decimales.

**Acceptance Scenarios**:

1. **Given** un valor de temperatura de `0` en escala `Celsius` y unidad de destino `Fahrenheit`, **When** el usuario solicita la conversión, **Then** el resultado es `32.00 °F`.
2. **Given** un valor de temperatura de `100` en escala `Celsius` y unidad de destino `Kelvin`, **When** el usuario solicita la conversión, **Then** el resultado es `373.15 K`.
3. **Given** un valor de temperatura de `98.6` en escala `Fahrenheit` y unidad de destino `Celsius`, **When** el usuario solicita la conversión, **Then** el resultado es `37.00 °C`.
4. **Given** un valor de temperatura de `300` en escala `Kelvin` y unidad de destino `Fahrenheit`, **When** el usuario solicita la conversión, **Then** el resultado es `80.33 °F`.
5. **Given** un valor de temperatura de `25.5` en escala `Celsius` y unidad de destino `Celsius`, **When** el usuario solicita la conversión, **Then** el resultado retornado es `25.50 °C` sin alteraciones en su magnitud.

---

### User Story 2 - Validación de Límites Físicos y Soporte de Temperaturas Negativas Válidas (Priority: P2)

Como usuario, deseo que el sistema valide rigurosamente los límites termodinámicos físicos del cero absoluto —rechazando con un mensaje explícito cualquier temperatura en Kelvin inferior a 0 K o por debajo del cero absoluto en las demás escalas— mientras permite y calcula correctamente valores negativos físicamente viables en Celsius y Fahrenheit.

**Why this priority**: Garantiza la integridad física y la confiabilidad de los datos, previniendo resultados imposibles en la realidad física mientras preserva el soporte para temperaturas bajo cero de uso cotidiano e industrial.

**Independent Test**: Puede validarse independientemente introduciendo temperaturas negativas válidas (como -40 °C o -10 °F) y corroborando el resultado correcto, así como ingresando valores inferiores al cero absoluto (< 0 K, < -273.15 °C, < -459.67 °F) y verificando el rechazo con mensajes claros.

**Acceptance Scenarios**:

1. **Given** un valor de temperatura de `-40` en escala `Celsius` y unidad de destino `Fahrenheit`, **When** el usuario solicita la conversión, **Then** el resultado es `-40.00 °F`.
2. **Given** un valor de temperatura de `-10` en escala `Fahrenheit` y unidad de destino `Celsius`, **When** el usuario solicita la conversión, **Then** el resultado es `-23.33 °C`.
3. **Given** un valor de temperatura de `-5` en escala `Kelvin` y cualquier unidad de destino, **When** el usuario solicita la conversión, **Then** el sistema rechaza la operación e informa que la temperatura en Kelvin no puede ser menor a 0.
4. **Given** un valor de temperatura de `-300` en escala `Celsius` (inferior al cero absoluto de -273.15 °C), **When** el usuario solicita la conversión, **Then** el sistema rechaza la operación con un mensaje indicando que el valor está por debajo del cero absoluto.

---

### User Story 3 - Manejo Resiliente de Entradas Inválidas y Guía de Uso (Priority: P3)

Como usuario, deseo recibir retroalimentación clara, amigable y comprensible cuando ingrese valores no numéricos, campos vacíos o unidades no reconocidas, para corregir mi entrada rápidamente sin experimentar fallos inesperados de la aplicación.

**Why this priority**: Asegura la solidez de la experiencia en la consola de comandos, evitando que el programa falle de forma abrupta y guiando al usuario hacia la ejecución exitosa.

**Independent Test**: Puede validarse de forma independiente ejecutando la herramienta con argumentos en blanco, cadenas de texto alfanuméricas en el campo de valor o códigos de unidad desconocidos, comprobando que se muestren mensajes de error orientados a la solución.

**Acceptance Scenarios**:

1. **Given** una entrada vacía o que contiene únicamente espacios en blanco para el valor de temperatura, **When** el usuario solicita la conversión, **Then** el sistema muestra un mensaje de error indicando que el valor de temperatura no puede estar vacío.
2. **Given** un valor de temperatura no numérico (por ejemplo, `"cien"` o `"12a"`), **When** el usuario solicita la conversión, **Then** el sistema muestra un mensaje de error indicando que se requiere un número válido.
3. **Given** una unidad de origen o destino no soportada (por ejemplo, `"Rankine"` o `"X"`), **When** el usuario solicita la conversión, **Then** el sistema muestra un mensaje indicando que las unidades válidas son Celsius, Fahrenheit y Kelvin.

---

### Edge Cases

- **Cero absoluto exacto**: Procesamiento exitoso de las fronteras `0 K`, `-273.15 °C` y `-459.67 °F`.
- **Punto de intersección Celsius-Fahrenheit**: Comportamiento a `-40 °C`, produciendo exactamente `-40.00 °F`.
- **Entrada de unidades insensible a mayúsculas/minúsculas**: Aceptación coherente de identificadores en minúsculas (`c`, `f`, `k`) o mayúsculas (`C`, `F`, `K`), así como nombres completos (`celsius`, `fahrenheit`, `kelvin`).
- **Valores con alta precisión decimal**: Redondeo adecuado de valores periódicos o con muchos decimales (por ejemplo `33.333333` o resultados fraccionarios como `1/3`) al estándar de 2 cifras decimales.
- **Misma unidad de origen y destino**: Conversión reflexiva (`C→C`, `F→F`, `K→K`) devolviendo el valor numérico formateado a 2 decimales sin distorsión.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir la conversión bidireccional entre las escalas de temperatura Celsius, Fahrenheit y Kelvin.
- **FR-002**: El sistema DEBE formatear el resultado de toda conversión numérica redondeado exactamente a 2 decimales.
- **FR-003**: El sistema DEBE soportar conversiones donde la unidad de origen y la unidad de destino sean idénticas, retornando el valor de entrada formateado a 2 decimales.
- **FR-004**: El sistema DEBE rechazar cualquier entrada de temperatura en la escala Kelvin con un valor menor a 0, mostrando un mensaje de error claro y comprensible.
- **FR-005**: El sistema DEBE rechazar cualquier entrada de temperatura que se encuentre por debajo del límite físico del cero absoluto (-273.15 °C o -459.67 °F), informando al usuario sobre el límite termodinámico violado.
- **FR-006**: El sistema DEBE aceptar y procesar sin errores valores numéricos negativos válidos en las escalas Celsius (>= -273.15 °C) y Fahrenheit (>= -459.67 °F).
- **FR-007**: El sistema DEBE validar las entradas del usuario y rechazar entradas vacías o compuestas únicamente de espacios en blanco con un mensaje explicativo.
- **FR-008**: El sistema DEBE validar que la magnitud de la temperatura sea un número real, rechazando entradas de texto no numérico o símbolos inválidos con un mensaje explicativo.
- **FR-009**: El sistema DEBE aceptar identificadores de unidades tanto por su inicial (`C`, `F`, `K`) como por su denominación completa (`Celsius`, `Fahrenheit`, `Kelvin`), sin distinción entre mayúsculas y minúsculas.
- **FR-010**: El sistema DEBE proporcionar instrucciones claras de uso y ejemplos de sintaxis ante invocaciones incompletas o erróneas en la línea de comandos.

### Key Entities

- **Temperatura (Temperature Reading)**: Entidad que representa la magnitud térmica analizada. Posee dos atributos clave: el valor cuantitativo (número real) y la unidad física asociada.
- **Unidad de Medida (Temperature Unit)**: Representa la escala termodinámica utilizada (Celsius, Fahrenheit, Kelvin), definiendo sus identificadores válidos y su límite inferior de cero absoluto.
- **Resultado de Conversión (Conversion Result)**: Entidad resultante del procesamiento que contiene la temperatura original (magnitud y unidad de origen) y la temperatura resultante (magnitud redondeada a 2 decimales y unidad de destino).
- **Notificación de Error (Validation Error)**: Representación de una falla en los datos de entrada (tipo de dato no numérico, campo ausente, unidad desconocida o violación de límites físicos) con texto explicativo para el usuario.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de las conversiones válidas entre cualquier combinación de unidades (Celsius, Fahrenheit, Kelvin) genera resultados numéricos matemáticamente correctos y formateados a 2 decimales.
- **SC-002**: El 100% de los intentos de conversión que violen el límite de cero absoluto (Kelvin < 0, Celsius < -273.15, Fahrenheit < -459.67) son rechazados con un mensaje de error claro sin interrupciones anormales del programa.
- **SC-003**: El 100% de las entradas no numéricas, vacías o con unidades inválidas emiten un mensaje descriptivo y guiado en menos de 1 segundo de tiempo de respuesta de cara al usuario.
- **SC-004**: Los usuarios pueden completar cualquier consulta de conversión en un único comando de consola, o mediante un flujo interactivo paso a paso cuando no se proporcionen parámetros.

## Assumptions

- Se asume el uso del punto (`.`) como separador decimal estándar.
- Las constantes de conversión corresponden a las definiciones físicas estandarizadas ($0\text{ K} = -273.15\text{ }^\circ\text{C}$; $[^\circ\text{F}] = [^\circ\text{C}] \times \frac{9}{5} + 32$).
- La salida de resultados y mensajes de error se presentará en texto plano legible en la consola de comandos estándar (stdout / stderr).
- El soporte para unidades incluye indistintamente mayúsculas y minúsculas para mayor comodidad del usuario.
