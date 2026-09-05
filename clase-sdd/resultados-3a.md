# Resultados Bloque 3.A — Spec a mano

Proyecto: Conversor de temperatura
Agente: agy (Antigravity CLI 1.1.26, Gemini 3.8 Flash High)
Archivo generado: conversor.py (155 lineas, 5573 bytes)

## Los 3 casos de prueba

| Tipo de caso | Comando | Resultado obtenido | Correcto |
|---|---|---|---|
| Normal | python conversor.py 25 C F | 77.0 | Si |
| Borde de mi spec (Kelvin < 0) | python conversor.py -5 K C | Error: La temperatura en Kelvin no puede ser menor a 0. | Si |
| No contemplado (Rankine) | python conversor.py 100 C R | Error: Unidad de destino 'R' no valida. Use Celsius (C), Fahrenheit (F) o Kelvin (K). | Manejado, aunque no estaba en la spec |

## Observaciones del comportamiento del agente

1. Leyo spec_manual.md por iniciativa propia, aunque el contenido ya iba pegado en el pedido.
2. Listo el directorio de trabajo sin que se le pidiera.
3. Intento leer C:\Users\mpsinche1\Documents\s4, fuera de su workspace. Se denego el acceso y la implementacion continuo sin problema.
4. Genero 155 lineas a partir de una spec de 5 criterios y 4 casos borde.
5. Invento reglas no especificadas: acepta alias de unidades (C, Celsius, CELSIUS) y valida unidades desconocidas con un mensaje propio. La spec nunca definio el formato de entrada de las unidades.
6. Agrego funcionalidad no pedida: invocacion por argumentos de terminal y manejo limpio de Ctrl+C.
7. No genero tests propios en esta corrida.

## Conclusion del bloque

La spec corta cubrio los criterios que si definio. Los huecos que dejo (formato de unidades, unidades desconocidas) los relleno el agente por su cuenta con decisiones razonables, pero que yo no elegi ni revise antes.