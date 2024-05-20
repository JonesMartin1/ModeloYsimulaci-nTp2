import datetime

#Metodo adaptado para el ejercicio 3
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
        semilla += datetime.datetime.now().microsecond
        for digit in str(semilla):
            resultados.append(int(digit))
        if len(resultados) == cantidad_digitos:
            return resultados
    return resultados


def generador_fibonacci(semilla1: int, semilla2: int, iteraciones=100, cantidad_digitos=123):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método de Fibonacci.

    Args:
        semilla1 (int): Primera semilla para el generador de números aleatorios.
        semilla2 (int): Segunda semilla para el generador de números aleatorios.
        iteraciones (int): Número de iteraciones para generar la secuencia.
        cantidad_digitos (int): Cantidad de dígitos a generar.

    Returns:
        list: Secuencia de números pseudoaleatorios generados.
    """
    resultados = []
    for _ in range(iteraciones):
        nuevo_numero = (semilla1 + semilla2) % 10**8  # Usamos un módulo grande para mantener los números en un rango razonable
        nuevo_numero += datetime.datetime.now().microsecond
        semilla1, semilla2 = semilla2, nuevo_numero
        for digit in str(nuevo_numero):
            resultados.append(int(digit))
        if len(resultados) == cantidad_digitos:
            return resultados
    return resultados

def generador_cuadrados_medios(semilla: int, iteraciones=100, cantidad_digitos=123):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método de Cuadrados Medios de Von Neumann.

    Args:
        semilla (int): Semilla inicial para el generador de números aleatorios.
        iteraciones (int): Número de iteraciones para generar la secuencia.
        cantidad_digitos (int): Cantidad de dígitos a generar.

    Returns:
        list: Secuencia de números pseudoaleatorios generados.
    """
    resultados = []
    semilla_str = str(semilla)
    n = len(semilla_str)
    if n % 2 != 0:
        raise ValueError("La semilla debe tener un número par de dígitos.")

    for _ in range(iteraciones):
        semilla_cuadrada = str(semilla ** 2).zfill(n * 2)
        mid_index = len(semilla_cuadrada) // 2
        semilla_str = semilla_cuadrada[mid_index - n // 2 : mid_index + n // 2]
        semilla = int(semilla_str)
        semilla += datetime.datetime.now().microsecond

        for digit in semilla_str:
            resultados.append(int(digit))
        if len(resultados) >= cantidad_digitos:
            return resultados[:cantidad_digitos]

    return resultados

def generador_congruencial_multiplicativo(semilla: int, a=1664525, m=2**32, iteraciones=100, cantidad_digitos=123):
    """
    Genera una secuencia de números pseudoaleatorios utilizando el método congruencial multiplicativo.

    Args:
        semilla (int): Semilla inicial para el generador de números aleatorios.
        a (int): Multiplicador.
        m (int): Módulo.
        iteraciones (int): Número de iteraciones para generar la secuencia.
        cantidad_digitos (int): Cantidad de dígitos a generar.

    Returns:
        list: Secuencia de números pseudoaleatorios generados.
    """
    resultados = []
    for _ in range(iteraciones):
        semilla = (a * semilla) % m
        semilla += datetime.datetime.now().microsecond  # Aumentar aleatoriedad con microsegundos
        semilla_str = str(semilla)
        for digit in semilla_str:
            resultados.append(int(digit))
        if len(resultados) >= cantidad_digitos:
            return resultados[:cantidad_digitos]
    return resultados