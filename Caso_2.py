from Prueba_chi_cuadrado import prueba_chi_cuadrado
from Metodos_Generadores import generador_aleatorio_mixto

def obtener_rangos_probabilidad(probabilidad_defecto):
    """
    Obtiene los rangos de índices para clasificar los números generados como defectuosos o no defectuosos.

    Args:
        probabilidad_defecto (float): Probabilidad de defecto en la producción.

    Returns:
        dict: Diccionario con los rangos de índices para clasificar los números.
        int: Valor máximo posible de un número generado.
    """
    numero_str = str(probabilidad_defecto)
    numeros_despues_del_punto = numero_str.split(".")[1]
    valor_maximo = int("".join(["9" for _ in range(len(numeros_despues_del_punto))]))
    rangos_clasificacion = {
        "defectuoso": [0, int(numeros_despues_del_punto) - 1],
        "no_defectuoso": [int(numeros_despues_del_punto), valor_maximo]
    }
    return rangos_clasificacion, valor_maximo

def simular_control_lote(probabilidad_lote, tamaño_muestra, limite_aceptacion, semilla=12344):
    """
    Simula el proceso de control de calidad para un lote de placas de video.

    Args:
        probabilidad_lote (float): Probabilidad de defecto en la producción para el lote actual.
        tamaño_muestra (int): Tamaño de la muestra de control.
        limite_aceptacion (int): Límite de aceptación para la proporción de placas defectuosas.
        semilla (int): Semilla inicial para el generador de números aleatorios.

    Returns:
        bool: True si el lote es aprobado, False si es rechazado.
    """
    rangos_probabilidad, valor_maximo = obtener_rangos_probabilidad(probabilidad_lote)
    cantidad_defectuosas = 0
    numeros_aleatorios = generador_aleatorio_mixto(semilla=semilla, cantidad_digitos=tamaño_muestra * len(str(valor_maximo)))
    
    prueba_valida = False
    while not prueba_valida:
        semilla += 1
        numeros_aleatorios = generador_aleatorio_mixto(semilla=semilla, cantidad_digitos=tamaño_muestra * len(str(valor_maximo)))
        prueba_valida, _, _ = prueba_chi_cuadrado(numeros_aleatorios)

    for numero_generado in numeros_aleatorios[:tamaño_muestra]:
        if rangos_probabilidad["defectuoso"][0] <= numero_generado <= rangos_probabilidad["defectuoso"][1]:
            cantidad_defectuosas += 1

    return cantidad_defectuosas <= limite_aceptacion

def simular_control_fabrica(cantidad_simulaciones):
    """
    Simula el proceso de control de calidad para múltiples lotes de placas de video.

    Args:
        cantidad_simulaciones (int): Cantidad de lotes a simular.
    """
    print("Ingresar los valores de p, n y α para la simulación de la fábrica de placas de video")
    probabilidad_lote = float(input("Probabilidad de placa gráfica defectuosa (En decimales): "))
    tamaño_muestra = int(input("Tamaño de la muestra de control: "))
    limite_aceptacion = int(input("Límite de aceptación (Número máximo de defectuosas permitidas): "))
    
    resultados_lotes = []
    for _ in range(cantidad_simulaciones):
        resultado_lote = simular_control_lote(probabilidad_lote, tamaño_muestra, limite_aceptacion)
        resultados_lotes.append(resultado_lote)
    
    cantidad_lotes_aprobados = sum(resultados_lotes)
    proporcion_lotes_aprobados = cantidad_lotes_aprobados / cantidad_simulaciones
    
    print(f"Cantidad de lotes simulados: {cantidad_simulaciones}")
    print(f"Cantidad de lotes aprobados: {cantidad_lotes_aprobados}")
    print(f"Proporción de lotes aprobados: {proporcion_lotes_aprobados:.2%}")

# Ejecutar la simulación para 150 lotes
simular_control_fabrica(150)