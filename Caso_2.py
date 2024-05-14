import datetime
import numpy as np
import scipy.stats as stats
import pandas as pd

def chi_squared_test(numbers: list, num_bins=10, alpha=0.05):
    """
    Realiza el test de chi-cuadrado para evaluar si una secuencia de números sigue una distribución uniforme.
    
    Args:
        numbers (list): Secuencia de números generados.
        num_bins (int): Número de bins para el histograma.
        alpha (float): Nivel de significancia para el test de chi-cuadrado.

    Returns:
        bool: True si pasa el test, False de lo contrario.
        float: Estadístico de chi-cuadrado calculado.
        float: Valor crítico de chi-cuadrado.
    """
    expected_frequency = len(numbers) / num_bins
    observed_frequency, _ = np.histogram(numbers, bins=num_bins)
    chi_squared_statistic = np.sum((observed_frequency - expected_frequency) ** 2 / expected_frequency)
    critical_value = stats.chi2.ppf(1 - alpha, num_bins - 1)
    return chi_squared_statistic <= critical_value, chi_squared_statistic, critical_value

def congruential_mixed(seed: int, a=16807, c=32, m=2147483647, iterations=100, quant_digits=123):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método congruencial mixto.

    Args:
        seed (int): Semilla inicial para el generador de números aleatorios.
        a (int): Multiplicador.
        c (int): Incremento.
        m (int): Módulo.
        iterations (int): Número de iteraciones para generar la secuencia.
        quant_digits (int): Cantidad de dígitos a generar.

    Returns:
        list: Secuencia de números pseudoaleatorios generados.
    """
    results = []
    for _ in range(iterations):
        seed = (a * seed + c) % m
        seed += datetime.datetime.now().microsecond
        for digit in str(seed):
            results.append(int(digit))
            if len(results) == quant_digits:
                return results
    return results

def get_numeros_indices(probabilidad):
    """
    Obtiene los rangos de índices para clasificar los números generados como defectuosos o no defectuosos.

    Args:
        probabilidad (float): Probabilidad de defecto en la producción.

    Returns:
        dict: Diccionario con los rangos de índices para clasificar los números.
        int: Valor máximo posible de un número generado.
    """
    numero = str(probabilidad)
    numeros_despues_del_punto = numero.split(".")[1]
    maximo = "".join(["9" for _ in range(len(numeros_despues_del_punto))])
    maximo = int(maximo)
    rangos = {
        "defectuoso": [0, int(numeros_despues_del_punto) - 1],
        "no_defectuoso": [int(numeros_despues_del_punto), maximo]
    }
    return rangos, maximo

def simulador_lote(p, n, a, seed=12344):
    """
    Simula el proceso de control de calidad para un lote de placas de video.

    Args:
        p (float): Probabilidad de defecto en la producción.
        n (int): Tamaño de la muestra de control.
        a (int): Límite de aceptación para la proporción de placas defectuosas.
        seed (int): Semilla inicial para el generador de números aleatorios.

    Returns:
        bool: True si el lote es aprobado, False si es rechazado.
    """
    rangos_probabilidad, maximo = get_numeros_indices(p)
    defectuosas = 0
    no_defectuosas = 0
    numeros_generados = congruential_mixed(seed=seed, quant_digits=n * len(str(maximo)) * 2)
    validacion, _, _ = chi_squared_test(numeros_generados)
    while not validacion:
        seed += 1
        numeros_generados = congruential_mixed(seed=seed, quant_digits=n * len(str(maximo)) * 2)
        validacion, _, _ = chi_squared_test(numeros_generados)
    for _ in range(n):
        numero = int("".join(str(numeros_generados.pop(0)) for _ in range(len(str(maximo)))))
        if rangos_probabilidad["defectuoso"][0] <= numero <= rangos_probabilidad["defectuoso"][1]:
            defectuosas += 1
        else:
            no_defectuosas += 1
    if defectuosas <= a:
        return True
    else:
        return False

def simulador_global_electricity(cantidad_lotes):
    """
    Simula el proceso de control de calidad para múltiples lotes de placas de video.

    Args:
        cantidad_lotes (int): Cantidad de lotes a simular.
    """
    lotes = []
    print("Ingresar los valores de p, n y a para la simulación de la fábrica de placas de video")
    p = float(input("Probabilidad de placa grafica defectuosa (En decimales): "))
    n = int(input("Tamaño de la muestra de control: "))
    a = int(input("Límite de aceptación (Del tamaño de la muestra actual): "))
    for _ in range(cantidad_lotes):
        lotes.append(simulador_lote(p=0.23, n=60, a=15, seed=333))
    lotes = pd.DataFrame(lotes, columns=["Aprobado"])
    print(lotes)
    print(lotes["Aprobado"].value_counts())
    print(lotes["Aprobado"].value_counts(normalize=True))
    print("Proporción de placas defectuosas promedio:", lotes["Aprobado"].mean())

simulador_global_electricity(10)