import random
import pandas as pd
import numpy as np

# Leer los datos
datos = pd.read_csv('filtered_accidentes_Ags_2019.csv', 
                    encoding='latin-1', 
                    usecols=['LATITUD', 'LONGITUD'], 
                    dtype={'LATITUD': 'float64', 'LONGITUD': 'float64'})
coordenadas_accidentes = datos.values  # Leer solo las coordenadas

# Parámetros
RADIO_COBERTURA = 4  # En kilómetros 
NUM_AMBULANCIAS = 4 
ITERACIONES_TABU = 100  
TAM_TABU = 10  # Tamaño de la lista tabú

# Distancia calculada usando fórmula de Haversine
def calcular_distancia(coord1, coord2):
    R = 6371  # Radio de la Tierra en kilómetros
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

# Precalcular distancias entre todos los accidentes y las ambulancias
def precalcular_distancias(accidentes, ambulancias):
    distancias = np.zeros((len(accidentes), len(ambulancias)))
    for i, accidente in enumerate(accidentes):
        for j, ambulancia in enumerate(ambulancias):
            distancias[i, j] = calcular_distancia(accidente, ambulancia)
    return distancias

# Función objetivo que usa la matriz de distancias precalculadas
def funcion_objetivo(ambulancias, accidentes, distancias):
    total_respuesta = 0
    for i, accidente in enumerate(accidentes):
        cobertura = distancias[i, :] <= RADIO_COBERTURA
        if np.any(cobertura):
            total_respuesta += np.min(distancias[i, cobertura])  # Tomar la menor distancia
        else:
            total_respuesta += 1000  # Penalización por accidentes fuera del radio
    return total_respuesta

# Cálculo del número de accidentes cubiertos
def calcular_accidentes_cubiertos(ambulancias, accidentes):
    distancias = precalcular_distancias(accidentes, ambulancias)
    cubiertos = np.any(distancias <= RADIO_COBERTURA, axis=1)  # Ver si algún accidente está dentro del radio
    return np.sum(cubiertos)  # Total de accidentes cubiertos

# Generación de una solución inicial
def generar_solucion_inicial(num_ambulancias, accidentes):
    indices = np.random.choice(len(accidentes), 
                               size=num_ambulancias,
                                 replace=False)
    return [tuple(accidentes[i]) for i in indices]

# Generación de vecinos simplificada
def generar_vecinos(solucion, accidentes):
    vecinos = []
    for i in range(len(solucion)):
        vecino = solucion[:]
        vecino[i] = tuple(random.choice(accidentes))
        vecinos.append(vecino)
    return vecinos

# Búsqueda tabú optimizada
def busqueda_tabu(accidentes, num_ambulancias, iteraciones, tabu_tam):
    solucion_actual = generar_solucion_inicial(num_ambulancias, accidentes)
    mejor_solucion = solucion_actual
    distancias = precalcular_distancias(accidentes, solucion_actual)
    mejor_costo = funcion_objetivo(solucion_actual, accidentes, distancias)

    # Inicializa la lista tabú vacía (para almacenar soluciones recientemente visitadas)
    lista_tabu = []

    for iteracion in range(iteraciones):
        # Genera vecinos de la solución actual (moviendo ambulancias a nuevas ubicaciones)
        vecinos = generar_vecinos(solucion_actual, accidentes)

        # Filtra los vecinos que están en la lista tabú (no permite soluciones ya visitadas recientemente)
        vecinos = [v for v in vecinos if v not in lista_tabu]

        # Si no hay vecinos válidos (por ejemplo, porque todos están en la lista tabú), pasa a la siguiente iteración
        if not vecinos:
            continue

        # Calcula los costos (usando la función objetivo) de todas las soluciones vecinas válidas
        costos_vecinos = [funcion_objetivo(vecino, accidentes, distancias) for vecino in vecinos]

        # Encuentra el vecino con el menor costo (el mejor vecino en esta iteración)
        mejor_vecino = vecinos[np.argmin(costos_vecinos)]
        lista_tabu.append(mejor_vecino)

        # Si la lista tabú excede el tamaño máximo permitido, elimina la solución más antigua (FIFO)
        if len(lista_tabu) > tabu_tam:
            lista_tabu.pop(0)

        solucion_actual = mejor_vecino

        # Recalcula las distancias de la solución actual para usarlas en la siguiente iteración
        distancias = precalcular_distancias(accidentes, solucion_actual)

        # Calcula el costo de la nueva solución actual
        costo_actual = funcion_objetivo(solucion_actual, accidentes, distancias)

        # Si el costo de la nueva solución actual es mejor que el mejor costo encontrado hasta ahora
        if costo_actual < mejor_costo:
            # Actualiza la mejor solución y su costo asociado
            mejor_solucion = solucion_actual
            mejor_costo = costo_actual

    # Devuelve la mejor solución encontrada y su costo asociado después de todas las iteraciones
    return mejor_solucion, mejor_costo

# Optimización con número fijo de ambulancias
def optimizar_numero_fijo_ambulancias(accidentes, num_ambulancias, iteraciones, tabu_tam):
    ubicaciones, costo = busqueda_tabu(accidentes, num_ambulancias, iteraciones, tabu_tam)
    cubiertos = calcular_accidentes_cubiertos(ubicaciones, accidentes)
    total_accidentes = len(accidentes)  # Total de accidentes (cubiertos + no cubiertos)
    no_cubiertos = total_accidentes - cubiertos  # Accidentes no cubiertos
    return ubicaciones, costo, cubiertos, total_accidentes, no_cubiertos

# Ejecutar el algoritmo
mejor_ubicaciones, mejor_costo, accidentes_cubiertos, total_accidentes, accidentes_no_cubiertos = optimizar_numero_fijo_ambulancias(
    accidentes=coordenadas_accidentes,
    num_ambulancias=NUM_AMBULANCIAS,
    iteraciones=ITERACIONES_TABU,
    tabu_tam=TAM_TABU
)

print("\nResultados:\n")
print(f"{'='*50}")
print(f"{'No. de ambulancias:':<30} {NUM_AMBULANCIAS}")
print(f"{'Accidentes cubiertos:':<30} {accidentes_cubiertos}")
print(f"{'Accidentes no cubiertos:':<30} {accidentes_no_cubiertos}")
print(f"{'Costo asociado:':<30} {mejor_costo:.2f}")
print(f"{'Ubicaciones de ambulancias:':<30}")
for idx, ubicacion in enumerate(mejor_ubicaciones, start=1):
    print(f"  Ambulancia {idx}: {ubicacion}")
print(f"{'='*50}\n")