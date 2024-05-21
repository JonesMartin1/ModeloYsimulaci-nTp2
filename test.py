import numpy as np
from scipy import stats

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

def generador_aleatorio_mixto1(semilla: int, a, c, m, p):
    resultados = []
    while len(resultados) < p:
        semilla = ((a * semilla + c) % m)
        resultados.append(semilla)
    if chi_squared_test(resultados):
        return [x / m for x in resultados]
    else:
        return generador_aleatorio_mixto1(semilla, a, c, m, p)

def simular_control_calidad(semilla, a, c, m, p_defecto, n, limite_aceptacion, tamano_lote=100):
    # Generar un lote de placas de video usando generador_aleatorio_mixto1
    probabilidades_defecto = generador_aleatorio_mixto1(semilla, a, c, m, tamano_lote)
    
    # Determinar si cada placa es defectuosa según la probabilidad de defecto
    lote = [1 if prob < p_defecto else 0 for prob in probabilidades_defecto]
    
    # Seleccionar una muestra aleatoria del lote
    muestra_indices = generador_aleatorio_mixto1(semilla, a, c, m, n)
    muestra_indices = [int(x * tamano_lote) for x in muestra_indices]
    muestra = [lote[i] for i in muestra_indices]
    
    # Inspeccionar la muestra y calcular la proporción de defectuosas
    placas_defectuosas = sum(muestra)
    proporcion_defectuosas = placas_defectuosas / n
    
    # Determinar el estado del lote
    aprobado = placas_defectuosas <= limite_aceptacion
    
    return aprobado, placas_defectuosas, proporcion_defectuosas

def simular_control_calidad_multiple_lotes(semilla, a, c, m, p_defecto, n, limite_aceptacion, cantidad_lotes, tamano_lote=100):
    resultados = []
    for _ in range(cantidad_lotes):
        resultado = simular_control_calidad(semilla, a, c, m, p_defecto, n, limite_aceptacion, tamano_lote)
        resultados.append(resultado)
        semilla += 1  # Incrementamos la semilla para cada lote para variar la secuencia de números aleatorios
    return resultados

def leer_parametros():
    p_defecto = float(input("Ingrese la probabilidad de placa gráfica defectuosa (en decimales): "))
    n = int(input("Ingrese el tamaño de la muestra de control: "))
    limite_aceptacion = int(input("Ingrese el límite de aceptación (número máximo de defectuosas permitidas): "))
    cantidad_lotes = int(input("Ingrese la cantidad de lotes a simular: "))
    return p_defecto, n, limite_aceptacion, cantidad_lotes

def main():
    # Leer los parámetros desde la consola
    p_defecto, n, limite_aceptacion, cantidad_lotes = leer_parametros()
    
    # Parámetros del generador aleatorio
    semilla = 123456  # Semilla inicial para el generador
    a = 1664525  # Multiplicador
    c = 1013904223  # Incremento
    m = 2**32  # Módulo
    tamano_lote = 100  # Tamaño del lote (opcional, por defecto 100)

    # Simulación de múltiples lotes
    resultados_lotes = simular_control_calidad_multiple_lotes(semilla, a, c, m, p_defecto, n, limite_aceptacion, cantidad_lotes, tamano_lote)

    lotes_aprobados = sum(resultado[0] for resultado in resultados_lotes)
    proporcion_aprobados = lotes_aprobados / cantidad_lotes
    
    # Mostrar resultados
    for i, (estado_lote, placas_defectuosas, proporcion_defectuosas) in enumerate(resultados_lotes, 1):
        print(f"Lote {i}: {'Aprobado' if estado_lote else 'Rechazado'}, Defectuosas en muestra: {placas_defectuosas}, Proporción defectuosas: {proporcion_defectuosas:.2f}")
    
    print(f"\nCantidad de lotes simulados: {cantidad_lotes}")
    print(f"Cantidad de lotes aprobados: {lotes_aprobados}")
    print(f"Cantidad de lotes no aprobados: {cantidad_lotes-lotes_aprobados}")
    print(f"Proporción de lotes aprobados: {proporcion_aprobados:.2f}")

if __name__ == "__main__":
    main()
