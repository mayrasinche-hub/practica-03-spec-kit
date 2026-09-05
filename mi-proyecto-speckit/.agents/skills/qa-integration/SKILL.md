---
name: qa-integration
description: Genera un test de integracion siguiendo lo definido en test-spec.md, sin improvisar el flujo a probar.
---
# Instrucciones
1. Lee `test-spec.md`, seccion "Que debe verificar el test de integracion". Si no existe, DETENTE y pide que se cree primero.
2. Genera un test que verifique exactamente ese flujo, de punta a punta.
3. Guarda en `tests/test_integracion.py`. Corre `python -m pytest tests/test_integracion.py -v` y reporta el resultado.