# Resultados Sesion 5 — Pruebas, cobertura y seguridad con agentes

Proyecto: Conversor de temperatura (mi-proyecto-speckit)
Agente: agy (Antigravity CLI 1.1.27, Gemini 3.8 Flash High)

## Arquitectura construida

| Capa | Que se creo |
|---|---|
| Skills (6) | qa-unit, qa-integration, qa-coverage, qa-security, qa-report, qa-orchestrate |
| Agentes (3) | tester-agent (qa-unit, qa-integration, qa-coverage), security-agent (qa-security), report-agent (qa-report) |
| Hook | gate-tests.ps1 + hooks.json, se dispara despues de editar archivos |
| Ordenes de trabajo | ordenes-agentes.md, una por agente, con tarea, criterios y entregable |

## Tabla de seguridad (security-agent)

| Caso | Lo que se encontro | Correccion sugerida |
|---|---|---|
| Secreto expuesto | Sin hallazgos: no se identificaron claves, contrasenas ni tokens hardcodeados en el codigo fuente | Ninguna. Mantener las credenciales fuera del repositorio |
| Validacion de entradas | Validacion funcional completa (tipo numerico, formato finito, rango de cero absoluto), pero sin limite de longitud maxima en las cadenas recibidas por CLI | Limitar la longitud maxima de la entrada antes de parsear a float, para evitar consumos excesivos de memoria |
| Manejo de excepciones | Uso de `except Exception: pass` generico y silencioso en cli.py lineas 12 y 17, al reconfigurar la codificacion de stdout y stderr | Capturar excepciones especificas (AttributeError, io.UnsupportedOperation). CORREGIDO en esta sesion |

## Bloque B — El hook en accion

| Momento | Resultado de gate-tests.ps1 | Codigo de salida |
|---|---|---|
| Antes del bug | 31 tests pasando | 0 (permite avanzar) |
| Con el bug (9/5 cambiado a 5/9 en Celsius a Fahrenheit) | 6 tests fallando + mensaje BLOQUEADO | 2 (bloquea) |
| Despues de corregir | 31 tests pasando | 0 (permite avanzar) |

En ningun momento le dije al agente cual era el bug. Solo le pase el resultado del hook y lo encontro desde los tests que fallaron.

## Bloque E — Orquestacion automatica

Segundo bug introducido: la constante de Celsius a Kelvin cambiada de 273.15 a 270.15.

Con un solo comando (`/qa-orchestrate`) corrieron los tres agentes en cadena:

| Agente | Que hizo |
|---|---|
| tester-agent | Ejecuto la suite segun test-spec.md: 5 de 6 unitarios pasados, 1 fallido en Celsius a Kelvin, integracion OK, 60% de cobertura |
| security-agent | Reviso secretos, validacion de entradas y manejo de excepciones: 0 hallazgos |
| report-agent | Ejecuto el script consolidador y genero reporte-qa.html |

## Preguntas de cierre

**1. Cual fue el veredicto final?**
REQUIERE CORRECCION. Los 31 tests pasan y no hay hallazgos de seguridad, pero la cobertura quedo en 60%, por debajo del umbral de 80% que definimos. El principal responsable es cli.py, que no computa cobertura porque el test de integracion lo ejecuta en un subproceso aislado.

**2. El inspector encontro ______ que el cocinero no habia visto.**
El inspector encontro dos bloques `except Exception: pass` en cli.py que el cocinero no habia visto: silenciaban cualquier error al configurar la codificacion UTF-8, sin dejar rastro de que algo hubiera fallado.

## Reflexion sobre la orquestacion

**1. En que se sintio distinto invocar agentes comparado con skills sueltas?**
Los agentes leyeron primero su propio archivo de rol y su orden de trabajo antes de hacer nada, y al terminar marcaron como cumplidos los criterios de su orden en ordenes-agentes.md, sin que nadie se lo pidiera. Una skill suelta ejecuta y ya. Tambien se noto en la salida: cada agente entrego exactamente el formato que decia su orden (resumen de 3-4 lineas el tester, tabla de 3 filas el security, veredicto de una linea el report).

**2. Que pasaria si el security-agent intentara modificar los tests? Podria?**
En teoria no: su archivo solo declara `tools: qa-security`. Pero en la practica esa restriccion es texto dentro de un archivo markdown, no una barrera que el sistema imponga. La prueba es que el tester-agent, que solo debia generar tests, edito src/converter.py y src/__init__.py para agregar una funcion `convert()` que no existia. El minimo privilegio esta escrito, no aplicado.

**3. Como seria si otro agente decidiera el orden en vez de mi?**
Eso fue exactamente `/qa-orchestrate`. La diferencia practica fue que deje de decidir cuando invocar a cada uno, pero no perdi control real: segui aprobando cada comando y el veredicto final fue el mismo. Lo que perdi fueron los pasos repetitivos, no las decisiones. El control de verdad estaba en otro lado: en test-spec.md y en ordenes-agentes.md, que se escribieron antes de que ningun agente corriera.

## Observaciones sobre el comportamiento de los agentes

1. El tester-agent salio de su rol: modifico codigo de produccion (src/converter.py, src/__init__.py) cuando su definicion decia que solo se ocupara de tests.
2. Los tres agentes editaron ordenes-agentes.md por iniciativa propia para marcar sus criterios como cumplidos.
3. El agente intento leer C:\Users\mpsinche1\Documents\s4, fuera de su workspace, y tambien su propia carpeta de memoria interna (~/.gemini/antigravity-cli/brain). Se denego el acceso y siguio trabajando sin problema.
4. El mismo script de reporte da resultados distintos segun desde donde se ejecute: desde PowerShell recoge 31 tests, desde el contexto de agy recoge 14. La cobertura calculada cambia en consecuencia.