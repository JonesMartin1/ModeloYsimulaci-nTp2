import datetime
from Prueba_chi_cuadrado import chi_squared_test

def generador_aleatorio_mixto1(semilla: int, a, c, m, p):
    resultados = []
    while len(resultados) < p:
        semilla = ((a * semilla + c) % m)
        resultados.append(semilla)
    if chi_squared_test(resultados):
        return [x / m for x in resultados]
    else:
        return generador_aleatorio_mixto1(semilla, a, c, m, p)
    
def generador_fibonacci(semilla1: int, semilla2: int, p: int):
    """
    Genera números pseudoaleatorios utilizando el método de Fibonacci.
    
    Parameters:
    semilla1 (int): Primera semilla.
    semilla2 (int): Segunda semilla.
    p (int): Cantidad de números a generar.
    
    Returns:
    list: Lista de números pseudoaleatorios.
    """
    resultados = [semilla1, semilla2]
    while len(resultados) < p:
        nuevo_numero = (resultados[-1] + resultados[-2]) % 10
        resultados.append(nuevo_numero)
    if chi_squared_test(resultados):
        return [x / 10 for x in resultados]
    else:
        return generador_fibonacci(resultados[-2], resultados[-1], p)
    
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

