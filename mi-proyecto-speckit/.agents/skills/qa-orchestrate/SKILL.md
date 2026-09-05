---
name: qa-orchestrate
description: Ejecuta el flujo completo de calidad invocando en orden a tester-agent, security-agent y report-agent, sin pedir confirmacion entre cada uno.
---
# Instrucciones
1. Verifica que exista `test-spec.md` y `ordenes-agentes.md`. Si falta alguno, detente y pide que se cree.
2. Invoca al agente tester-agent siguiendo la orden en ordenes-agentes.md. Espera a que termine por completo.
3. Invoca al agente security-agent siguiendo la orden en ordenes-agentes.md. Espera a que termine por completo.
4. Invoca al agente report-agent siguiendo la orden en ordenes-agentes.md.
5. Presenta al usuario el veredicto final, con un resumen de 1 linea de que hizo cada agente en el camino.

No pidas confirmacion entre fase y fase — este es un flujo automatico de punta a punta.