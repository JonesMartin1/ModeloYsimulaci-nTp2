import numpy as np
from scipy import stats
import datetime

def chi_square(observed, expected):
    """
    Calculate the chi-square statistic.

    Args:
        observed (list): Observed frequencies.
        expected (list): Expected frequencies.

    Returns:
        float: Chi-square statistic.
    """
    if len(observed) != len(expected):
        raise ValueError("Observed and expected arrays must have the same length.")
    chi_sq = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    return chi_sq

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
    frecuencia_observada, _ = np.histogram(numeros, bins=cantidad_bins)
    frecuencia_esperada = len(numeros) / cantidad_bins
    estadistico_chi_cuadrado = chi_square(frecuencia_observada, [frecuencia_esperada] * cantidad_bins)
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
        for digit in str(semilla):
            resultados.append(int(digit))
        if len(resultados) == cantidad_digitos:
            return resultados
    return resultados

def test_prueba_chi_cuadrado():
    # Generate a list of 100 random numbers using the generador_aleatorio_mixto function
    semilla = 12345  # Seed for random number generation
    numeros = generador_aleatorio_mixto(semilla, iteraciones=100)
    
    # Perform the chi-square test
    pasa_prueba, estadistico_chi_cuadrado, valor_critico = prueba_chi_cuadrado(numeros)
    
    # Print the results
    print("Resultados del test de chi-cuadrado:")
    print("Pasa el test:", pasa_prueba)
    print("Estadístico de chi-cuadrado:", estadistico_chi_cuadrado)
    print("Valor crítico de chi-cuadrado:", valor_critico)

# Run the test
test_prueba_chi_cuadrado()