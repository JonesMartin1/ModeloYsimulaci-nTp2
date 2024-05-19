import datetime
import numpy as np
import scipy.stats as stats

tiempo0 = 15

def congruentialmixed(a, c, m, seed, p):
    """
    Simulates a congruential mixed linear generator.

    Args:
        a: Multiplier constant.
        c: Increment constant.
        m: Modulus.
        seed: Initial seed value.
        p: Number of pseudo-random numbers to generate.

    Returns:
        A list of pseudo-random numbers.
    """
    numerosPseudoAleatorios = []
    for _ in range(p):
        seed = (a * seed + c) % m
        seed += (datetime.datetime.now().microsecond * 0.000001)
        pseudo_random_number = seed / m
        if pseudo_random_number < 1:
            numerosPseudoAleatorios.append(pseudo_random_number)
        else:
            numerosPseudoAleatorios.append(pseudo_random_number - int(pseudo_random_number))
        
    return numerosPseudoAleatorios

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
    return chi_squared_statistic <= critical_value


def clasificar_numeros(lista, resultado_chi_cuadrado):
    """
    Clasifica los números de la lista según los rangos especificados si el resultado del test chi-cuadrado es True.

    Args:
        lista (list): Lista de números generados.
        resultado_chi_cuadrado (bool): Resultado del test de chi-cuadrado.

    Returns:
        list: Lista de números clasificados.
    """
    if not resultado_chi_cuadrado:
        return []

    clasificados = []
    for valor in lista:
        if 0 <= valor <= 0.036:
            clasificados.append(-3)
        elif 0.037 <= valor <= 0.188:
            clasificados.append(-2)
        elif 0.189 <= valor <= 0.224:
            clasificados.append(-1)
        elif 0.225 <= valor <= 0.605:
            clasificados.append(0)
        elif 0.606 <= valor <= 0.659:
            clasificados.append(1)
        elif 0.660 <= valor <= 0.887:
            clasificados.append(2)
        elif 0.888 <= valor <= 0.999:
            clasificados.append(3)
    return clasificados


def procesar_y_sumar(clasificados, tiempo0):
    """
    Toma una lista de números clasificados, multiplica cada valor por 5 y suma todos los valores.
    Aplica reglas de resta en cada iteración según el valor total.

    Args:
        clasificados (list): Lista de números clasificados.

    Returns:
        int: Suma de todos los valores multiplicados por 5, aplicando reglas de resta.
    """
    Compuerta1 = 0
    Compuerta2 = 0
    Compuerta3 = 0
    Compuerta4 = 0
    AlertaRoja = 0
    
    suma_total = tiempo0
    for valor in clasificados:
        # Multiplicar el valor clasificado por 5
        
        if valor > 0:
            if valor == 3:
                valor_multiplicado = valor + 3
            if valor == 2:
                valor_multiplicado = valor + 2
            if valor == 1:
                valor_multiplicado = valor + 1
        elif valor < 0:
            valor_multiplicado = valor - 1
        elif valor == 0:
            valor_multiplicado = valor + 0
        
        # Sumar el valor multiplicado al total actual
        suma_total += valor_multiplicado
        
        # Aplicar reglas de resta según el valor total
        if suma_total >= 55:
            print ("SE ROMPIO LA REPRESA")
        elif suma_total > 40:
            suma_total -= 4
            Compuerta1 += 1
            Compuerta2 += 1
            Compuerta3 += 1
            Compuerta4 += 1
            AlertaRoja += 1
        elif suma_total > 32:
            suma_total -= 3
            Compuerta1 += 5
            Compuerta2 += 1
            Compuerta3 += 1
        elif suma_total > 25:
            suma_total -= 2
            Compuerta1 += 1
            Compuerta2 += 1
        elif suma_total > 15:
            suma_total -= 1
            Compuerta1 += 1
        elif suma_total < 0:
            print("SEQUIA")
    print ("La compuerta 1 se abrió ", Compuerta1 ," veces")
    print ("La compuerta 2 se abrió ", Compuerta2 ," veces")
    print ("La compuerta 3 se abrió ", Compuerta3 ," veces")
    print ("La compuerta 4 se abrió ", Compuerta4 ," veces")
    print ("Sonó la Alerta Roja ", AlertaRoja ," veces")
    return suma_total
    

print(procesar_y_sumar(clasificar_numeros(congruentialmixed(7,3,4,4444,1000), chi_squared_test(congruentialmixed(7,3,4,4444,100))),tiempo0))

