# CLI Interface Contract: Conversor de Temperatura

**Feature**: Conversor de Temperatura CLI (`001-temperature-converter-cli`)  
**Interface Type**: Command Line Interface (CLI)  
**Status**: Approved  

---

## 1. Modos de Invocación

### A. Sintaxis Posicional Directa (Recomendada)
```bash
python -m src.cli <VALOR> <ORIGEN> <DESTINO>
```

### B. Sintaxis con Opciones Nombradas
```bash
python -m src.cli --value <VALOR> --from <ORIGEN> --to <DESTINO>
# o abreviado:
python -m src.cli -v <VALOR> -f <ORIGEN> -t <DESTINO>
```

### C. Modo Interactivo (Asistido)
Si se ejecuta sin argumentos:
```bash
python -m src.cli
```
El sistema solicitará secuencialmente:
1. `Ingrese el valor de temperatura: `
2. `Ingrese la unidad de origen (C/F/K): `
3. `Ingrese la unidad de destino (C/F/K): `

---

## 2. Especificación de Parámetros

| Parámetro | Posición / Bandera | Tipo | Requerido | Descripción | Ejemplos Válidos |
|---|---|---|---|---|---|
| **Valor** | 1 / `-v`, `--value` | String / Float | Sí | Magnitud numérica de la temperatura | `100`, `0`, `-40`, `98.6`, `25.50` |
| **Origen** | 2 / `-f`, `--from` | String | Sí | Unidad de medida de origen | `C`, `c`, `Celsius`, `F`, `Fahrenheit`, `K`, `Kelvin` |
| **Destino** | 3 / `-t`, `--to` | String | Sí | Unidad de medida de destino | `C`, `c`, `Celsius`, `F`, `Fahrenheit`, `K`, `Kelvin` |

---

## 3. Formato de Salida y Contratos de Respuesta

### Salida Exitosa (`stdout`, Exit Code `0`)
El resultado debe imprimirse en la salida estándar mostrando el valor numérico con exactamente 2 decimales y el símbolo de la unidad de destino:

```text
32.00 °F
```
O formato detallado opcional si se solicita `--verbose`:
```text
0.00 °C = 32.00 °F
```

### Casos de Prueba Contractuales de Éxito

| Invocación | Salida Esperada (`stdout`) | Código de Salida |
|---|---|---|
| `python -m src.cli 0 C F` | `32.00 °F` | `0` |
| `python -m src.cli 100 C K` | `373.15 K` | `0` |
| `python -m src.cli 98.6 F C` | `37.00 °C` | `0` |
| `python -m src.cli 300 K F` | `80.33 °F` | `0` |
| `python -m src.cli 25.5 C C` | `25.50 °C` | `0` |
| `python -m src.cli -40 C F` | `-40.00 °F` | `0` |
| `python -m src.cli -10 F C` | `-23.33 °C` | `0` |

---

## 4. Contratos de Error (`stderr`, Exit Code > 0)

Todos los errores deben imprimirse en `stderr` con un mensaje descriptivo y devolver un código de salida distinto de cero:

| Condición | Código de Salida | Salida Esperada (`stderr`) |
|---|---|---|
| **Kelvin menor a 0** | `1` | `Error: La temperatura en Kelvin no puede ser menor a 0.` |
| **Celsius < -273.15** | `1` | `Error: La temperatura no puede ser inferior al cero absoluto (-273.15 °C).` |
| **Fahrenheit < -459.67** | `1` | `Error: La temperatura no puede ser inferior al cero absoluto (-459.67 °F).` |
| **Entrada no numérica** | `1` | `Error: El valor de temperatura debe ser un número válido.` |
| **Entrada vacía** | `1` | `Error: El valor de temperatura no puede estar vacío.` |
| **Unidad desconocida** | `1` | `Error: Unidad no reconocida '<VALOR>'. Unidades válidas: Celsius (C), Fahrenheit (F), Kelvin (K).` |
| **Argumentos incompletos (CLI)** | `2` | Mensaje estándar de ayuda y uso generado por `argparse`. |
