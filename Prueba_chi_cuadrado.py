import numpy as np
import scipy.stats as stats


#Prueba de chi adaptada a ejercicio 2
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

