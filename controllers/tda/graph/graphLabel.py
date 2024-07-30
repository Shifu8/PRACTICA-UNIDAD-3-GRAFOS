from math import nan
import os.path
import json
import os
from controllers.exception.arrayPositionException import ArrayPositionException
from controllers.tda.graph.graphManaged import GraphManaged

class GraphLabel(GraphManaged):
    def __init__(self, num_vert) -> None:
        super().__init__(num_vert)
        self.labels = {} 

    def addLabel(self, vertex, obj): 
        if vertex < self.num_vertex: 
            self.labels[vertex] = obj   
        else:
            raise ArrayPositionException("Delimite out")

    def getLabel(self, vertex): 
        if vertex in self.labels:
            return self.labels[vertex]
        else:
            return None

    def add_edges_label(self, obj1, obj2, weight): 
        v1 = self.get_vertexlabel(obj1)
        v2 = self.get_vertexlabel(obj2)
        if v1 is not None and v2 is not None:
            self.insert_edges_weight(v1, v2, weight)
        else:
           raise ArrayPositionException("Delimite out")

    def get_vertexlabel(self, obj):
        for vertex, label in self.labels.items():
            if label == obj:
                return vertex
        return None
