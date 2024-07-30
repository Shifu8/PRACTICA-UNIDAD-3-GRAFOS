from controllers.tda.graph.graphNoManeged import  GraphNoManaged
from controllers.exception.arrayPositionException import ArrayPositionException
from math import nan
import heapq

class GraphNoManagedLabel(GraphNoManaged):
    def __init__(self, num_vert):
        super().__init__(num_vert)
        self.__labels = []
        self.__labelsVertex={}
        for i in range(0, self.num_vertex):
            self.__labels.append(None)
        
    def getVertex(self, label):
        try:
            return self.__labelsVertex[str(label)]
        except KeyError:
            return -1 
    
    def label_vertex(self, v, label):
        self.__labels[v] = label
        self.__labelsVertex[str(label)] = v
        
    def get_all_vertices(self):
        return list(self.__labelsVertex.keys())
        
    def getLabel(self, v):
        return self.__labels[v]
    
    def exist_edge_E(self, label1, label2):
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            return self.exist_edges(v1, v2)
        else:
            return False
        
    def insert_edges_weight_E(self, label1, label2, weight):
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            self.insert_edges_weight(v1, v2, weight)
        else:
            raise ArrayPositionException("Vertex not found")
        
    def insert_edges_E(self, label1, label2): #sirve para insertar aristas
        self.insert_edges_weight_E(label1, label2, nan)
    
    def weight_edges_E(self, label1, label2): #sirve para obtener el peso de las aristas
        v1 = self.getVertex(label1)
        v2 = self.getVertex(label2)
        if v1 != -1 and v2 != -1:
            return self.weight_edges(v1, v2)
        else:
            raise ArrayPositionException("Vertex not found") 
        
    def adjacent_E(self, label1): #es para obtener los vertices adyacentes
        v1 = self.getVertex(label1)
        if v1 != -1:
            return self.adjacent(v1)
        else:
            raise ArrayPositionException("Vertex not found")
    
    