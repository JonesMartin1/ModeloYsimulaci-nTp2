import numpy as np
import scipy.stats as stats


def chiCuadrado(numeros: list, rango=10, E=0.005):
    # Convertir los números a una escala de 0 a 1 si es necesario
    numerosEscalados = [(x / 10) + 0.01 for x in numeros]
    
    # Definir los límites de los bins
    RangosEntre = np.linspace(0, 1, rango+1)
    
    # Crear un histograma con los números escalados
    frecuenciaObservada, _ = np.histogram(numerosEscalados, bins=RangosEntre)
    #print(frecuenciaObservada)
    
    # Calcular la frecuencia esperada
    frecuenciaEsperada = len(numerosEscalados) / rango
    
    # Calcular el estadístico chi-cuadrado
    estadistico = np.sum((frecuenciaObservada - frecuenciaEsperada) ** 2 / frecuenciaEsperada)
    
    # Obtener el valor crítico de la distribución chi-cuadrado
    valorCritico = stats.chi2.ppf(1 - E, rango - 1)
    
    # Retornar el resultado de la prueba
    return estadistico <= valorCritico, frecuenciaObservada, valorCritico, estadistico