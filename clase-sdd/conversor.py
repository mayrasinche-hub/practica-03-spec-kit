"""Conversor de temperatura entre Celsius, Fahrenheit y Kelvin.

Este módulo implementa la función convertir(valor, origen, destino) y un menú
simple por consola para interactuar con el usuario.
"""

import sys

MAPA_UNIDADES = {
    'C': 'C',
    'CELSIUS': 'C',
    'F': 'F',
    'FAHRENHEIT': 'F',
    'K': 'K',
    'KELVIN': 'K',
}

NOMBRES_UNIDADES = {
    'C': 'Celsius (°C)',
    'F': 'Fahrenheit (°F)',
    'K': 'Kelvin (K)',
}


def convertir(valor, origen, destino):
    """Convierte un valor de temperatura entre Celsius, Fahrenheit y Kelvin.

    Parámetros:
        valor: Valor numérico o texto representativo de la temperatura.
        origen: Unidad de origen ('C', 'F', 'K' o nombres completos).
        destino: Unidad de destino ('C', 'F', 'K' o nombres completos).

    Retorna:
        float: Resultado redondeado a 2 decimales si la conversión es exitosa.
        str: Mensaje de error claro si los datos no son válidos.
    """
    # 1. Validación de entrada vacía o nula
    if valor is None:
        return "Error: Entrada vacía. Por favor, ingrese un valor de temperatura."

    if isinstance(valor, bool):
        return "Error: Entrada no numérica. Debe ingresar un valor numérico válido."

    if isinstance(valor, str):
        val_str = valor.strip()
        if val_str == "":
            return "Error: Entrada vacía. Por favor, ingrese un valor de temperatura."
        # Permitir coma como separador decimal si no hay punto
        if ',' in val_str and '.' not in val_str:
            val_str = val_str.replace(',', '.')
        try:
            valor_num = float(val_str)
        except (ValueError, TypeError):
            return "Error: Entrada no numérica. Debe ingresar un valor numérico válido."
    elif isinstance(valor, (int, float)):
        valor_num = float(valor)
    else:
        return "Error: Entrada no numérica. Debe ingresar un valor numérico válido."

    # 2. Validación de unidades
    if not isinstance(origen, str) or not isinstance(destino, str):
        return "Error: Las unidades deben ser texto (C, F o K)."

    orig_key = origen.strip().upper()
    dest_key = destino.strip().upper()

    if orig_key not in MAPA_UNIDADES:
        return f"Error: Unidad de origen '{origen}' no válida. Use Celsius (C), Fahrenheit (F) o Kelvin (K)."

    if dest_key not in MAPA_UNIDADES:
        return f"Error: Unidad de destino '{destino}' no válida. Use Celsius (C), Fahrenheit (F) o Kelvin (K)."

    u_origen = MAPA_UNIDADES[orig_key]
    u_destino = MAPA_UNIDADES[dest_key]

    # 3. Rechazar temperatura en Kelvin menor a 0 en origen
    if u_origen == 'K' and valor_num < 0:
        return "Error: La temperatura en Kelvin no puede ser menor a 0."

    # 4. Misma unidad de origen y destino
    if u_origen == u_destino:
        return round(valor_num, 2)

    # 5. Fórmulas de conversión
    if u_origen == 'C' and u_destino == 'F':
        resultado = (valor_num * 9 / 5) + 32
    elif u_origen == 'F' and u_destino == 'C':
        resultado = (valor_num - 32) * 5 / 9
    elif u_origen == 'C' and u_destino == 'K':
        resultado = valor_num + 273.15
    elif u_origen == 'K' and u_destino == 'C':
        resultado = valor_num - 273.15
    elif u_origen == 'F' and u_destino == 'K':
        resultado = (valor_num - 32) * 5 / 9 + 273.15
    elif u_origen == 'K' and u_destino == 'F':
        resultado = (valor_num - 273.15) * 9 / 5 + 32
    else:
        return "Error: Conversión no soportada."

    # Rechazar temperatura en Kelvin menor a 0 en resultado
    if u_destino == 'K' and resultado < 0:
        return "Error: La temperatura en Kelvin no puede ser menor a 0."

    # 6. Redondear resultado a 2 decimales
    return round(resultado, 2)


def menu():
    """Muestra un menú simple por consola para interactuar con el conversor."""
    print("=" * 45)
    print("          CONVERSOR DE TEMPERATURA          ")
    print("=" * 45)

    while True:
        print("\nOpciones:")
        print("  1. Convertir temperatura")
        print("  2. Salir")

        try:
            opcion = input("\nSeleccione una opción (1 o 2): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSaliendo del programa...")
            break

        if opcion == "2":
            print("\n¡Gracias por usar el conversor de temperatura! Hasta luego.")
            break
        elif opcion == "1":
            print("\n--- Nueva conversión ---")
            try:
                valor_input = input("Ingrese el valor de la temperatura: ")
                origen = input("Unidad de origen (C: Celsius, F: Fahrenheit, K: Kelvin): ")
                destino = input("Unidad de destino (C: Celsius, F: Fahrenheit, K: Kelvin): ")
            except (EOFError, KeyboardInterrupt):
                print("\nOperación cancelada.")
                break

            resultado = convertir(valor_input, origen, destino)

            if isinstance(resultado, str) and resultado.startswith("Error"):
                print(f"\n[!] {resultado}")
            else:
                simbolo_dest = NOMBRES_UNIDADES.get(MAPA_UNIDADES.get(destino.strip().upper(), ''), destino)
                print(f"\n>>> Resultado: {resultado} ({simbolo_dest})")
        else:
            print("\n[!] Opción no válida. Por favor, ingrese 1 o 2.")


if __name__ == '__main__':
    # Si se pasan 3 argumentos por línea de comandos, ejecuta directamente
    if len(sys.argv) == 4:
        res = convertir(sys.argv[1], sys.argv[2], sys.argv[3])
        print(res)
    else:
        menu()
