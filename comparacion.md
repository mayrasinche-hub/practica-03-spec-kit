# Comparacion — Spec a mano vs Spec Kit

Proyecto: Conversor de temperatura (Celsius, Fahrenheit, Kelvin)
Sesion 4 — Programacion de Backend y MCP en Python para IA Generativa

## Tabla comparativa

| Aspecto | Spec a mano | Spec Kit |
|---|---|---|
| Cubrio los mismos casos borde? | Si, los 4 que escribi: entrada no numerica, entrada vacia, misma unidad, negativos validos | Si, los mismos 4 y ademas la validacion del cero absoluto fisico en las tres escalas, que yo no habia pensado |
| Que genero Spec Kit que yo no habia escrito? | — | Checklist de calidad de la propia spec, documento de investigacion tecnica, modelo de dominio con diagrama Mermaid, contrato formal de la CLI con codigos de salida POSIX, guia de validacion rapida, 19 tareas ordenadas por dependencia y 24 pruebas automatizadas |
| Que se sintio mas rapido de arrancar? | La spec a mano: 15 minutos de escritura y un solo pedido al agente para tener codigo funcionando | Spec Kit: mas de 20 minutos y 4 comandos encadenados antes de ver la primera linea de codigo |
| Cual me genero mas confianza en el resultado? | Confianza media: funciona, pero lo unico que lo respalda son las 3 pruebas que corri a mano | Confianza alta: 24 pruebas automatizadas pasando y un contrato explicito de la interfaz. Ademas detecto y corrigio solo un error de codificacion de Windows que yo no habria visto |

## Los 3 casos, lado a lado

| Caso | Spec a mano (agy) | Spec Kit |
|---|---|---|
| Normal: 25 C a F | 77.0 | 77.00 grados F |
| Borde de mi spec: -5 K a C | Error: La temperatura en Kelvin no puede ser menor a 0. | Error: La temperatura en Kelvin no puede ser menor a 0. |
| No contemplado: 100 C a Rankine | Error: Unidad de destino 'R' no valida. Use Celsius (C), Fahrenheit (F) o Kelvin (K). | Error: Unidad no reconocida 'R'. Unidades validas: Celsius (C), Fahrenheit (F), Kelvin (K). |

Los dos manejaron el caso no contemplado, pero por caminos distintos: en la spec a mano el agente relleno el hueco improvisando durante la implementacion; en Spec Kit la regla quedo escrita en el contrato de la CLI antes de programar. El formato de salida tambien difiere por la misma razon: mi spec nunca dijo como imprimir el resultado, y Spec Kit si lo definio.

## Diferencia de volumen

| | Spec a mano | Spec Kit |
|---|---|---|
| Documentos de especificacion | 1 archivo, 15 lineas | 7 archivos, mas de 600 lineas |
| Archivos de codigo | 1 (conversor.py, 155 lineas) | 4 modulos en src/ mas 3 suites de tests |
| Pruebas automatizadas | 0 | 24 |
| Tiempo hasta primer codigo | ~15 min | ~25 min |

## Cierre

La proxima vez que tenga un proyecto de tamano pequeno, elegiria la spec a mano porque en 15 minutos llego a codigo funcionando y el costo de equivocarme es bajo: si el agente rellena un hueco de forma distinta a la que yo esperaba, lo corrijo probando. Para un proyecto mediano o grande elegiria Spec Kit, porque los artefactos que genera (contrato de interfaz, modelo de dominio, tareas ordenadas y suite de pruebas) son justamente lo que se vuelve caro reconstruir cuando el proyecto crece o cuando otra persona tiene que entenderlo.