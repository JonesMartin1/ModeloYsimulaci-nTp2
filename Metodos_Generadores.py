import datetime
import numpy as np
import math
from Prueba_chi_cuadrado import chi_squared_test

def generador_aleatorio_mixto1(semilla: int, a: int, c: int, m: int, p: int):
    """
    Generador de números pseudoaleatorios utilizando el método de congruencia lineal mixto.
    
    Args:
        semilla (int): Valor inicial o semilla.
        a (int): Multiplicador.
        c (int): Incremento.
        m (int): Módulo.
        p (int): Cantidad de números a generar.

    Returns:
        list: Lista de números pseudoaleatorios normalizados entre 0 y 1.

    Nota:
        Si los números generados no pasan la prueba de chi-cuadrado, la generación se repite con la última semilla.
    """
    resultados = []
    while len(resultados) < p:
        semilla = ((a * semilla + c) % m)
        resultados.append(semilla)
    if chi_squared_test(resultados):
        return [x / m for x in resultados]
    else:
        return generador_aleatorio_mixto1(semilla, a, c, m, p)
      
      
    
def generador_aleatorio_aditivo(semilla: int, c: int, m: int, p: int):
    """
    Generador de números pseudoaleatorios utilizando el método de congruencia aditiva.
    
    Args:
        semilla (int): Valor inicial o semilla.
        c (int): Incremento.
        m (int): Módulo.
        p (int): Cantidad de números a generar.

    Returns:
        list: Lista de números pseudoaleatorios normalizados entre 0 y 1.

    Nota:
        Si los números generados no pasan la prueba de chi-cuadrado, la generación se repite con la última semilla.
    """
    resultados = []
    while len(resultados) < p:
        semilla = (semilla + c) % m
        resultados.append(semilla)
    if chi_squared_test(resultados):
        return [x / m for x in resultados]
    else:
        return generador_aleatorio_aditivo(semilla, c, m, p)

def generador_congruencial_multiplicativo(semilla: int, a: int, m: int, p: int):
    """
    Genera números pseudoaleatorios utilizando el método congruencial multiplicativo.
    
    Parameters:
    semilla (int): Semilla inicial.
    a (int): Constante multiplicativa.
    m (int): Módulo.
    p (int): Cantidad de números a generar.
    
    Returns:
    list: Lista de números pseudoaleatorios.
    """
    resultados = []
    while len(resultados) < p:
        semilla = (a * semilla) % m
        semilla += datetime.datetime.now().microsecond
        for digit in str(semilla):
            if len(resultados) < p:
                resultados.append(int(digit))
    if chi_squared_test(resultados):
        return [x / 10**len(str(max(resultados))) for x in resultados]
    else:
        return generador_congruencial_multiplicativo(semilla, a, m, p)



def generador_cuadrados_medios(semilla: int, p: int):
    """
    Genera números pseudoaleatorios utilizando el método de cuadrados medios.
    
    Parameters:
    semilla (int): Semilla inicial.
    p (int): Cantidad de números a generar.
    
    Returns:
    list: Lista de números pseudoaleatorios.
    """
    resultados = []
    while len(resultados) < p:
        semilla = int(str(semilla ** 2).zfill(8)[2:6]) + datetime.datetime.now().microsecond
        for digit in str(semilla):
            if len(resultados) < p:
                resultados.append(int(digit))
    if chi_squared_test(resultados):
        return [x / 10**len(str(max(resultados))) for x in resultados]
    else:
        return generador_cuadrados_medios(semilla, p)
    

def generador_poisson(lam: float, p: int):
    """
    Generador de números pseudoaleatorios siguiendo la distribución de Poisson.
    
    Args:
        lam (float): La media (lambda) de la distribución de Poisson.
        p (int): Cantidad de números a generar.

    Returns:
        list: Lista de números generados con la distribución de Poisson.
    """
    resultados = []
    for _ in range(p):
        L = math.exp(-lam)
        k = 0
        p_temp = 1
        while True:
            k += 1
            u = np.random.uniform(0, 1)
            p_temp *= u
            if p_temp <= L:
                break
        resultados.append(k - 1)
    
    if chi_squared_test(resultados):
        return resultados
    else:
        return generador_poisson(lam, p)