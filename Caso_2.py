import datetime
import numpy as np
import scipy.stats as stats

def prueba_chi_cuadrado(numeros: list, cantidad_bins=10, nivel_significancia=0.05):
    """
    Realiza el test de chi-cuadrado para evaluar si una secuencia de números sigue una distribución uniforme.

    Args:
        numeros (list): Secuencia de números generados.
        cantidad_bins (int): Número de bins para el histograma.
        nivel_significancia (float): Nivel de significancia para el test de chi-cuadrado.

    Returns:
        bool: True si pasa el test, False de lo contrario.
        float: Estadístico de chi-cuadrado calculado.
        float: Valor crítico de chi-cuadrado.
    """
    frecuencia_esperada = len(numeros) / cantidad_bins
    frecuencia_observada, _ = np.histogram(numeros, bins=cantidad_bins)
    estadistico_chi_cuadrado = np.sum((frecuencia_observada - frecuencia_esperada) ** 2 / frecuencia_esperada)
    valor_critico = stats.chi2.ppf(1 - nivel_significancia, cantidad_bins - 1)
    return estadistico_chi_cuadrado <= valor_critico, estadistico_chi_cuadrado, valor_critico

def generador_aleatorio_mixto(semilla: int, coeficiente_multiplicador=16807, incremento=32, modulo=2147483647, iteraciones=100, cantidad_digitos=123):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método congruencial mixto.

    Args:
        semilla (int): Semilla inicial para el generador de números aleatorios.
        coeficiente_multiplicador (int): Multiplicador.
        incremento (int): Incremento.
        modulo (int): Módulo.
        iteraciones (int): Número de iteraciones para generar la secuencia.
        cantidad_digitos (int): Cantidad de dígitos a generar.

    Returns:
        list: Secuencia de números pseudoaleatorios generados.
    """
    resultados = []
    for _ in range(iteraciones):
        semilla = (coeficiente_multiplicador * semilla + incremento) % modulo
        semilla += datetime.datetime.now().microsecond
        for digit in str(semilla):
            resultados.append(int(digit))
        if len(resultados) == cantidad_digitos:
            return resultados
    return resultados

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
    cantidad_no_defectuosas = 0
    numeros_aleatorios = generador_aleatorio_mixto(semilla=semilla, cantidad_digitos=tamaño_muestra * len(str(valor_maximo)) * 2)
    prueba_valida = False
    while not prueba_valida:
        semilla += 1
        numeros_aleatorios = generador_aleatorio_mixto(semilla=semilla, cantidad_digitos=tamaño_muestra * len(str(valor_maximo)) * 2)
        prueba_valida, _, _ = prueba_chi_cuadrado(numeros_aleatorios)
    for numero_generado in numeros_aleatorios:
        if rangos_probabilidad["defectuoso"][0] <= numero_generado <= rangos_probabilidad["defectuoso"][1]:
            cantidad_defectuosas += 1
        else:
            cantidad_no_defectuosas += 1
    return cantidad_defectuosas <= limite_aceptacion

def simular_control_fabrica(cantidad_simulaciones):
    """
    Simula el proceso de control de calidad para múltiples lotes de placas de video.

    Args:
        cantidad_simulaciones (int): Cantidad de lotes a simular.
    """
    resultados_lotes = []
    print("Ingresar los valores de p, n y a para la simulación de la fábrica de placas de video")
    probabilidad_lote = float(input("Probabilidad de placa grafica defectuosa (En decimales): "))
    tamaño_muestra = int(input("Tamaño de la muestra de control: "))
    limite_aceptacion = int(input("Límite de aceptación (Del tamaño de la muestra actual): "))
    for _ in range(cantidad_simulaciones):
        resultado_lote = simular_control_lote(probabilidad_lote, tamaño_muestra, limite_aceptacion)
        resultados_lotes.append(resultado_lote)
    cantidad_lotes_aprobados = sum(resultados_lotes)
    proporcion_lotes_aprobados = cantidad_lotes_aprobados / cantidad_simulaciones
    print(f"Cantidad de lotes simulados: {cantidad_simulaciones}")
    print(f"Cantidad de lotes aprobados: {cantidad_lotes_aprobados}")
    print(f"Proporción de lotes aprobados: {proporcion_lotes_aprobados:.2%}")

simular_control_fabrica(10)
