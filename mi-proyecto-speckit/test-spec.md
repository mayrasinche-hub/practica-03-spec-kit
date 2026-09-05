# Spec de pruebas — Conversor de temperatura

## Que deben verificar los tests unitarios
- [ ] convert: dado 25 en Celsius a Fahrenheit, debe devolver 77.00
- [ ] convert: dado 100 en Celsius a Kelvin, debe devolver 373.15
- [ ] convert: con la misma unidad de origen y destino (25 C a C), debe devolver 25.00
- [ ] convert: con texto en vez de numero (por ejemplo "abc"), debe dar un error claro y controlado, no una excepcion sin manejar
- [ ] convert: con una temperatura en Kelvin menor a 0, debe rechazarla con un mensaje de error
- [ ] convert: con -40 en Celsius a Fahrenheit, debe devolver -40.00

## Que debe verificar el test de integracion
- [ ] El flujo completo desde la linea de comandos (python -m src.cli 25 C F) hasta la salida final debe imprimir el resultado convertido en stdout y devolver codigo de salida 0