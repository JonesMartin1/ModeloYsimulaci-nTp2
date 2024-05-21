import datetime
import numpy as np
import scipy.stats as stats

def chi_squared_test(numbers: list, num_bins=10, alpha=0.005):
    # Convertir los números a una escala de 0 a 1 si es necesario
    scaled_numbers = [(x / 10) + 0.01 for x in numbers]
    
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
        for digit in str(semilla):
            if len(resultados) < p:
                resultados.append(int(digit))
    if chi_squared_test(resultados):
        return [((((x / m)*100000000)*3)-datetime.datetime.now().microsecond*0.0000001) for x in resultados]
    else:
        return generador_aleatorio_mixto1(semilla, a, c, m, p)

def clasificar_numeros(lista):
    if lista == False:
        return False
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
        elif 0.888 <= valor:
            clasificados.append(3)
    return clasificados

def procesar_y_sumar(clasificados, tiempo0):
    if clasificados == False:
        return "No se aceptó la prueba"
    Compuerta1 = 0
    Compuerta2 = 0
    Compuerta3 = 0
    Compuerta4 = 0
    AlertaRoja = 0
    AlrtaDeSequía = 0
    contadordedías = 0
    
    suma_total = tiempo0
    for valor in clasificados:
        contadordedías += 1
                
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
        if suma_total >= 52:
            print ("La compuerta 1 se abrió ", Compuerta1 ," veces")
            print ("La compuerta 2 se abrió ", Compuerta2 ," veces")
            print ("La compuerta 3 se abrió ", Compuerta3 ," veces")
            print ("La compuerta 4 se abrió ", Compuerta4 ," veces")
            print ("Sonó la alerta Roja ", AlertaRoja ," veces")
            return ("El agua sobrepasó la represa en el día "+ str(contadordedías))
        elif suma_total > 45:
            suma_total -= 4
            Compuerta1 += 1
            Compuerta2 += 1
            Compuerta3 += 1
            Compuerta4 += 1
            AlertaRoja += 1
        elif suma_total > 40:
            suma_total -= 4
            Compuerta1 += 1
            Compuerta2 += 1
            Compuerta3 += 1
            Compuerta4 += 1
        elif suma_total > 32:
            suma_total -= 3
            Compuerta1 += 1
            Compuerta2 += 1
            Compuerta3 += 1
        elif suma_total > 25:
            suma_total -= 2
            Compuerta1 += 1
            Compuerta2 += 1
        elif suma_total > 15:
            suma_total -= 1
            Compuerta1 += 1
        elif suma_total <= 2:
            AlrtaDeSequía += 1
            
    print ("La compuerta 1 se abrió ", Compuerta1 ," veces")
    print ("La compuerta 2 se abrió ", Compuerta2 ," veces")
    print ("La compuerta 3 se abrió ", Compuerta3 ," veces")
    print ("La compuerta 4 se abrió ", Compuerta4 ," veces")
    print ("Sonó la alerta Roja ", AlertaRoja ," veces")
    print ("Sonó la alerta de sequía ", AlrtaDeSequía ," veces")
    return ("El nivel del caudal después de " + str(len(clasificados)) + " periodos de días es de " + str(suma_total) + " metros")

# Introducir valores desde la entrada del usuario
p = int(input("Introducir el número de iteraciones de tiempo: "))
tiempo0 = int(input("Introduce el valor del tiempo0: "))

# Llamar a la función generador_aleatorio_mixto1 con los valores introducidos por el usuario
aleatorios = generador_aleatorio_mixto1(9999, 1103515245, 12345, (2**31-1), p)
# Llamar a las funciones siguientes con los resultados
resultado_clasificacion = clasificar_numeros(aleatorios)
resultado_procesamiento = procesar_y_sumar(resultado_clasificacion, tiempo0)

print("Resultado final:", resultado_procesamiento)