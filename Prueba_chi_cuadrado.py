import numpy as np
import scipy.stats as stats


def chi_squared_test(numbers: list, num_bins=10, alpha=0.005):
    # Convertir los números a una escala de 0 a 1 si es necesario
    scaled_numbers = [(x / max(numbers)) for x in numbers]
    
    # Definir los límites de los bins
    bin_edges = np.linspace(0, 1, num_bins+1)
    
    # Crear un histograma con los números escalados
    observed_frequency, _ = np.histogram(scaled_numbers, bins=bin_edges)
    
    # Calcular la frecuencia esperada
    expected_frequency = len(scaled_numbers) / num_bins
    
    # Calcular el estadístico chi-cuadrado
    chi_squared_statistic = np.sum((observed_frequency - expected_frequency) ** 2 / expected_frequency)
    
    # Obtener el valor crítico de la distribución chi-cuadrado
    critical_value = stats.chi2.ppf(1 - alpha, num_bins - 1)
    
    # Retornar el resultado de la prueba
    return chi_squared_statistic <= critical_value