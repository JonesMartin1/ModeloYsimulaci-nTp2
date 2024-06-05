from Metodos_Generadores import generador_aleatorio_mixto1
print(generador_aleatorio_mixto1(12320, 7, 11, 11, 10))
def binomial_sample(n, p, size):
    """
    Genera muestras artificiales con distribución binomial.
    
    Parámetros:
    - n: número de ensayos en cada experimento.
    - p: probabilidad de éxito en cada ensayo.
    - size: número de muestras a generar.
    
    Retorna:
    - Una lista de muestras generadas.
    """
    samples = []
    for _ in range(size):
        count = 0
        for i in range(n):
            if generador_aleatorio_mixto1(12320, 7, 11, 11, 10)[i] > p:
                count += 1
        samples.append(count)
    return samples

# Ejemplo de uso de la función
n = 10  # Número de ensayos en cada experimento
p = 0.5  # Probabilidad de éxito en cada ensayo
size = 10 # Número de muestras a generar

print(binomial_sample(10, 0.5, 20))