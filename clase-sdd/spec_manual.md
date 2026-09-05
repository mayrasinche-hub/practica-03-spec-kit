# Spec manual — Conversor de temperatura

## Objetivo
Convertir un valor de temperatura entre Celsius, Fahrenheit y Kelvin para uso en linea de comandos.

## Criterios de aceptacion
- [ ] Convierte correctamente de Celsius a Fahrenheit y de Fahrenheit a Celsius
- [ ] Convierte correctamente de Celsius a Kelvin y de Kelvin a Celsius
- [ ] Convierte correctamente de Fahrenheit a Kelvin y de Kelvin a Fahrenheit
- [ ] Redondea el resultado a 2 decimales
- [ ] Rechaza una temperatura en Kelvin menor a 0 con un mensaje de error claro

## Casos borde
- Entrada no numerica (ej. "abc") -> devuelve un mensaje de error claro, sin excepcion sin controlar
- Entrada vacia -> devuelve un mensaje de error claro pidiendo un valor
- Misma unidad de origen y destino (ej. Celsius a Celsius) -> devuelve el mismo numero redondeado a 2 decimales
- Valores negativos validos en Celsius y Fahrenheit (ej. -40) -> se procesan sin problema