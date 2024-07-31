import os.path
import json
import os
from controllers.tda.graph.adjacent import Adjacent
import heapq
import json
import heapq
import math

class Graph():
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        
    @property
    def num_vertex(self): 
        raise NotImplementedError("Please implement this method")
    
    @property
    def num_edges(self): 
        raise NotImplementedError("Please implement this method")
    
    def exist_edge(self, start_vertex, end_vertex):
        # Implementación para verificar la existencia de un borde
        return (start_vertex, end_vertex) in self.edges
    
    
    def weight_edges(self, start_vertex, end_vertex):
        # Implementación para obtener el peso de un borde
        return self.edges.get((start_vertex, end_vertex), math.inf)
    
    def insert_edges(self,v1, v2): #para insertar una arista sin peso
        raise NotImplementedError("Please implement this method")
    
    def insert_edges_weight(self, v1, v2, weight): #para insertar una arista con peso
        raise NotImplementedError("Please implement this method")
    
    def adjacent(self,v1): #para ver los vertices adyacentes
        raise NotImplementedError("Please implement this method")
    
    def get_neighbors(self, vertex):
        return [(target, weight) for (start, target), weight in self.edges.items() if start == vertex]
    def __str__(self) -> str:
        out = ""
        for i in range(0, self.num_vertex):
            out += "V" +str(i+1) + "\n"
            adjs = self.adjacent(i)
            if not adjs.isEmpty:
                for j in range(0, adjs._length):
                    adj = adjs.get(j)
                    out+= "ady" + "V" + str(adj._destination +1) + " weight: " + str(adj._weight) + "\n"
        return out
    
    def paint_graph(self):
        url = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))+"/static/d3/grafo.js"
        js = 'var nodes = new vis.DataSet(['
        for i in range(0, self.num_vertex):
            js+= '{id: ' + str(i+1) + ',label:"' + str(self.getLabel(i))+'"},'+ "\n"
        js+= ']);'
        js+= "\n"
        js+= 'var edges = new vis.DataSet(['
        for i in range(0, self.num_vertex):
            #ini = str(i+1)
            adjs = self.adjacent(i)
            if not adjs.isEmpty:
                for j in range(0, adjs._length):
                    adj = adjs.getNode(j)
                    des = str(adj._destination+1) 
                    js+= '{from: '+str(i+1) +',to:'+str(des) + ',label:"'+str(adj._weight)+'"},'+ "\n"
        js+= ']);'
        js+= "\n"
        js+= 'var container = document.getElementById("mynetwork"); var data = {nodes: nodes,edges: edges,};var options = {};var network = new vis.Network(container, data, options);'
        a = open(url, 'w')
        a.write(js)
        a.close() 
        
    def save_graph_to_json(self):
        graph_data = {
            'vertices': [],
            'edges': []
        }

        for i in range(self.num_vertex):
            label = self.getLabel(i)  
            graph_data['vertices'].append({'id': i + 1, 'label': label})

            adjs = self.adjacent(i)
            if not adjs.isEmpty:
                for j in range(adjs._length):
                    adj = adjs.get(j)
                    graph_data['edges'].append({
                        'source': i + 1,
                        'target': adj._destination + 1,
                        'weight': adj._weight
                    })
        file_path = os.path.join('data', 'grafo.json')

        if not os.path.exists('data'):
            os.makedirs('data')

        with open(file_path, 'w') as json_file:
            json.dump(graph_data, json_file, indent=4)

        print(f"Grafo guardado en {file_path}")
        
    def load_from_json(self, json_data):
        data = json.loads(json_data)
        for vertex in data['vertices']:
            self.add_vertex(vertex['id'], vertex['label'])
        for edge in data['edges']:
            self.add_edge(edge['source'], edge['target'], edge['weight'])
            
    def add_vertex(self, id, label):
        self.vertices[id] = label
        self.edges[id] = {}

    def add_edge(self, source, target, weight):
        self.edges[source][target] = weight
        self.edges[target][source] = weight

    def dijkstra(self, start_vertex):
        distances = {vertex: math.inf for vertex in self.vertices}
        previous_vertices = {vertex: None for vertex in self.vertices}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.edges[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous_vertices

    def get_path(self, previous_vertices, start_vertex, end_vertex):
        path = []
        while end_vertex is not None:
            path.append(end_vertex)
            end_vertex = previous_vertices[end_vertex]
        path.reverse()
        return path

    def floyd_warshall(self):
        distances = {vertex: {vertex2: math.inf for vertex2 in self.vertices} for vertex in self.vertices}
        next_vertices = {vertex: {vertex2: None for vertex2 in self.vertices} for vertex in self.vertices}

        for vertex in self.vertices:
            distances[vertex][vertex] = 0

        for source in self.edges:
            for target, weight in self.edges[source].items():
                distances[source][target] = weight
                next_vertices[source][target] = target

        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if distances[i][k] + distances[k][j] < distances[i][j]:
                        distances[i][j] = distances[i][k] + distances[k][j]
                        next_vertices[i][j] = next_vertices[i][k]

        return distances, next_vertices

    def get_path_floyd(self, next_vertices, start_vertex, end_vertex):
        path = []
        while start_vertex != end_vertex:
            path.append(start_vertex)
            start_vertex = next_vertices[start_vertex][end_vertex]
            if start_vertex is None:
                return []
        path.append(end_vertex)
        return path