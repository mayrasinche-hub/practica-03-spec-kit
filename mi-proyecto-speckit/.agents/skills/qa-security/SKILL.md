---
name: qa-security
description: Revisa el proyecto en busca de secretos expuestos, validacion de entradas insuficiente y manejo de excepciones riesgoso.
---
# Instrucciones
1. Busca claves/contrasenas escritas directamente en el codigo.
2. Revisa validacion de entradas (tipo, formato, longitud, rango).
3. Busca `except:` generico o `except: pass`.
4. Reporta en esta tabla:

| Caso | Lo que se encontro | Correccion sugerida |
|---|---|---|
| Secreto expuesto | [hallazgo o "sin hallazgos"] | [sugerencia] |
| Validacion de entradas | [hallazgo o "sin hallazgos"] | [sugerencia] |
| Manejo de excepciones | [hallazgo o "sin hallazgos"] | [sugerencia] |

5. No corrijas automaticamente — solo diagnostica.