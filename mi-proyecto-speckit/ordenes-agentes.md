# Ordenes de trabajo para los agentes de QA

## Orden: tester-agent
**Tarea:** Verificar la calidad funcional de este proyecto.
**Criterios de aceptacion de esta tarea:**
- [x] Genera y corre tests unitarios segun test-spec.md
- [x] Genera y corre el test de integracion segun test-spec.md
- [x] Reporta el porcentaje de cobertura y que lineas quedaron sin probar
**Entregable esperado:** resumen de 3-4 lineas, sin codigo completo pegado en el chat.

## Orden: security-agent
**Tarea:** Revisar riesgos de seguridad basicos en este proyecto.
**Criterios de aceptacion de esta tarea:**
- [x] Revisa secretos expuestos, validacion de entradas, manejo de excepciones
- [x] Reporta en la tabla de exactamente 3 filas
**Entregable esperado:** la tabla, sin agregar hallazgos fuera de esas 3 categorias.

## Orden: report-agent
**Tarea:** Generar el veredicto final de calidad.
**Criterios de aceptacion de esta tarea:**
- [x] Ejecuta el script de reporte (no redacta el reporte con IA)
- [x] Presenta el veredicto y, si aplica, los 2-3 problemas mas importantes
**Entregable esperado:** veredicto + resumen de una linea, no el HTML completo pegado en el chat.