
from controllers.tda.graph.graphNoManagedLabel import GraphNoManagedLabel
from controllers.sinteticas.sinteticasControl import SinteticasControl
from controllers.sinteticas.calculoDistancia import CalculoDistancia
import os, re
from heapq import heappop, heappush
import math
import heapq 
import json 

class SinteticasGrafo(GraphNoManagedLabel):
    def __init__(self):
        self.__grafo = None
        self.__ndao = SinteticasControl()
        self.__dirPhysical = "static/d3/grafo.js"
        self.__labels = []
        self.__labelsVertex={}
        self.create_graph()
    

    @property
    def _grafo(self):
        if self.__grafo == None:
            self.create_graph()
        return self.__grafo

    @_grafo.setter
    def _grafo(self, value):
        self.__grafo = value
        
    def getVertex(self, label):
        try:
            return self.__labelsVertex[str(label)]
        except KeyError:
            return -1  
        
    def create_graph(self, origen=None, destino=None):
        # Obtener la lista de sintéticas
        lista_sinteticas = self.__ndao._list()
    
        # Verificar que la lista no esté vacía
        if lista_sinteticas._length > 0:
            self.__grafo = GraphNoManagedLabel(lista_sinteticas._length)
            arr = lista_sinteticas.toArray
            for i, sinteticas in enumerate(arr):
                self.__grafo.label_vertex(i, sinteticas._nombre)

            if os.path.exists(self.__dirPhysical):
                nc = SinteticasControl()
                with open(self.__dirPhysical, 'r') as file:
                    for line in file:
                        o_match = re.search(r'from:\s*(\d+)', line)
                        d_match = re.search(r'to:\s*(\d+)', line)
                        w_match = re.search(r'label:"([\d.]+)"', line)

                        if o_match and d_match and w_match:
                            o = int(o_match.group(1))
                            d = int(d_match.group(1))
                            w = float(w_match.group(1))

                            sinteticaOrigen = nc._list().binary_search_models(o, "_id")
                            sinteticaDestino = nc._list().binary_search_models(d, "_id")

                            if sinteticaOrigen is not None and sinteticaDestino is not None:
                                self.__grafo.insert_edges_weight_E(sinteticaOrigen._nombre, sinteticaDestino._nombre, w)
                            else:
                                print(f"Advertencia: No se encontraron nodos para los IDs {o} o {d}.")

        # Si se proporcionan origen y destino, calcular la distancia y agregar una arista
        if origen and destino:
            peso = CalculoDistancia().calcularDistancia(origen._lng, origen._lat, destino._lng, destino._lat)
            self.__grafo.insert_edges_weight_E(origen._nombre, destino._nombre, round(float(peso), 3))
        self.__grafo.paint_graph()
        self.__grafo.save_graph_to_json()
    
           
   