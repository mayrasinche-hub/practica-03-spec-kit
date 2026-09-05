---
name: qa-coverage
description: Ejecuta y resume el reporte de cobertura de tests del proyecto, senalando lineas sin probar.
---
# Instrucciones
1. Corre `python -m pytest --cov=src --cov-report=term-missing`.
2. Resume: porcentaje total, y que lineas "Missing" son casos borde olvidados vs. codigo no usado.
3. No agregues tests automaticamente — solo diagnostica.