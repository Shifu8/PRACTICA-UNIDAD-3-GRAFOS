import time
import random
from controllers.tda.graph.graph import Graph

def crear_grafo(tamano):
    g = Graph()
    for i in range(1, tamano + 1):
        g.add_vertex(i, f'V{i}')
    
    for i in range(1, tamano + 1):
        for j in range(i + 1, tamano + 1):
            weight = random.randint(1, 10)
            g.add_edge(i, j, weight)
    
    return g

def medir_tiempos(tamano):
    g = crear_grafo(tamano)
    
    start_time = time.time()
    distancias_dijkstra, _ = g.dijkstra(1)
    tiempo_dijkstra = time.time() - start_time

    start_time = time.time()
    distancias_floyd, _ = g.floyd_warshall()
    tiempo_floyd = time.time() - start_time

    return tiempo_dijkstra, tiempo_floyd

def imprimir_resultados(tamanos):
    resultados = []

    for tamano in tamanos:
        print(f"Evaluando grafo con {tamano} vértices...")
        tiempo_dijkstra, tiempo_floyd = medir_tiempos(tamano)
        resultados.append({
            'tamano': tamano,
            'dijkstra': tiempo_dijkstra,
            'floyd': tiempo_floyd
        })

    print("Resultados:")
    print("Tamaño | Tiempo Dijkstra | Tiempo Floyd")
    for resultado in resultados:
        print(f"{resultado['tamano']} | {resultado['dijkstra']:.4f} s | {resultado['floyd']:.4f} s")