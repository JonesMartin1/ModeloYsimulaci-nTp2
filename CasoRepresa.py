import datetime
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
    return estadistico <= valorCritico

def generador_aleatorio_mixto1(semilla: int, a, c, m, p):
    resultados = []
    while len(resultados) < p:
        semilla = ((a * semilla + c) % m) + datetime.datetime.now().microsecond
        for digit in str(semilla):
            if len(resultados) < p:
                resultados.append(int(digit))
    #print(resultados)
    if chiCuadrado(resultados):
        return [((((x / m)*100000000)*3)-datetime.datetime.now().microsecond*0.0000001) for x in resultados]
    else:
        return generador_aleatorio_mixto1(semilla, a, c, m, p)

def clasificar_numeros(lista):
    # Clasifica cada número de la lista y lo posiciona según la distribución proporcionada por el escenario
    clasificados = []
    for valor in lista:
        if 0 >= valor <= 0.036:
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
        elif valor >= 0.888:
            clasificados.append(3)
    # Transforma cada número aleatorio en una marca de clase la cuál está relacionada por una distribución 
    return clasificados

def procesar_y_sumar(clasificados, tiempo0):
    # Inicialización de variables
    Compuerta1 = 0
    Compuerta2 = 0
    Compuerta3 = 0
    Compuerta4 = 0
    AlertaRoja = 0
    AlertaDeSequía = 0
    contadordedías = 0
    suma_total = tiempo0
    almacen = 0
    
    # Por cada número clasificado se va sumando o restando según corresponda a una variable llamada suma_total
    for valor in clasificados:
        contadordedías += 1
        
        if valor > 0:
            suma_total += valor * 2
        else:
            suma_total += valor
        
        # Asegurar que suma_total no sea negativo
        if suma_total < 0:
            suma_total = 0
        
        # Aplicar reglas de resta según el valor total
        if suma_total > 52:
            print("La compuerta 1 se abrió", Compuerta1, "veces")
            print("La compuerta 2 se abrió", Compuerta2, "veces")
            print("La compuerta 3 se abrió", Compuerta3, "veces")
            print("La compuerta 4 se abrió", Compuerta4, "veces")
            print("Sonó la alerta Roja", AlertaRoja, "veces")
            return "El agua sobrepasó la represa en el día " + str(contadordedías) + " provocando la ruptura de la misma"
        elif suma_total > 45:
            exceso = suma_total - 40
            suma_total -= 6
            if almacen + exceso > 15:
                almacen = 15
            else:
                almacen += exceso
                print("Se almacenarón " + str(exceso) + " metros de agua en el almacen el día " + str(contadordedías))
                print("El amacen cuenta con una capacidad de " +str(almacen)+ " metros de agua el día "+ str(contadordedías))
            Compuerta1 += 1
            Compuerta2 += 1
            Compuerta3 += 1
            Compuerta4 += 1
            AlertaRoja += 1
            print("Sonó la alerta roja el día", str(contadordedías))
        elif suma_total > 40:
            exceso = suma_total - 40
            suma_total -= 6
            if almacen + exceso > 15:
                almacen = 15
            else:
                almacen += exceso
                print("Se almacenarón " + str(exceso) + " metros de agua en el almacen el día " + str(contadordedías))
                print("El amacen cuenta con una capacidad de " +str(almacen)+ " metros de agua el día "+ str(contadordedías))      
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
            if almacen > 0:
                suma_total += almacen
                print("Se liberaron " + str(almacen) + " metros de agua del almacen el día " + str(contadordedías))
                almacen = 0
            AlertaDeSequía += 1
            print("Sonó la alerta de sequía el día", str(contadordedías))
        
        # Asegurar que suma_total no sea negativo después de restar
        if suma_total < 0:
            suma_total = 0
    
    # Impresión final de resultados
    print("La compuerta 1 se abrió", Compuerta1, "veces")
    print("La compuerta 2 se abrió", Compuerta2, "veces")
    print("La compuerta 3 se abrió", Compuerta3, "veces")
    print("La compuerta 4 se abrió", Compuerta4, "veces")
    if AlertaRoja == 1:
        print("Sonó la alerta de roja una sola vez")
    elif AlertaRoja > 1:
        print("Sonó la alerta de roja", AlertaRoja, "veces")
    else:
        print("No sonó la alerta de roja")
        
    if AlertaDeSequía == 1:
        print("Sonó la alerta de sequía una sola vez")
    elif AlertaDeSequía > 1:
        print("Sonó la alerta de sequía", AlertaDeSequía, "veces")
    else:
        print("No sonó la alerta de sequía")
    
    return "El nivel del caudal después de " + str(len(clasificados)) + " periodos de días es de " + str(suma_total) + " metros"

# Introducir valores desde la entrada del usuario
p = int(input("Introducir el número de iteraciones de tiempo: "))
tiempo0 = int(input("Introduce el valor del caudal en el tiempo 0 (Número entre 0 y 51): "))

# Llamar a la función generador_aleatorio_mixto1 con los valores introducidos por el usuario
aleatorios = generador_aleatorio_mixto1(9999, 1103515244, 12345, (2**31-1), p)
# Llamar a las funciones siguientes con los resultados
resultado_clasificacion = clasificar_numeros(aleatorios)
resultado_procesamiento = procesar_y_sumar(resultado_clasificacion, tiempo0)

print("Resultado final:", resultado_procesamiento)