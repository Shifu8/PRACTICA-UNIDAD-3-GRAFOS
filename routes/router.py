from flask import Blueprint, jsonify, abort , request, render_template, redirect, Flask, flash, url_for
from controllers.sinteticas.sinteticasControl import SinteticasControl
from controllers.tda.graph.graphNoManagedLabel import GraphNoManagedLabel
from controllers.sinteticas.sinteticasGrafo import SinteticasGrafo
from controllers.tda.linked.quick import QuickSort
from controllers.tda.linked.mergesort import MergeSort
from controllers.tda.linked.shellsort import ShellSort
from controllers.tda.graph.graph import Graph
router = Blueprint('router', __name__)
import json
import time
from controllers.tda.graph.graph import Graph
import math


#GET: PARA PRESENTAR DATOS
#POST: GUARDA DATOS, MODIFICA DATOS Y EL INICIO DE SESION, EVIAR DATOS AL SERVIDOR

@router.route('/') #SON GETS
def home():
    return render_template('index.html')

@router.route("/sala")
def sala():
    return render_template("sinteticas/sala.html")

#LISTA PERSONAS
@router.route('/sinteticas')
def lista_sinteticas():
    nc = SinteticasControl()
    return render_template('sinteticas/lista.html', lista=nc.to_dic())


@router.route('/sinteticas/agregar')
def ver_guardar_sinteticas():
    return render_template('sinteticas/guardar.html')


@router.route('/sinteticas/guardar', methods=["POST"])
def guardar_sinteticas():
    nc = SinteticasControl()
    data = request.form
    
    nc._sinteticas._nombre = data["nombre"]
    nc._sinteticas._direccion = data["direccion"]
    nc._sinteticas._horario = data["horario"]
    nc._sinteticas._lng = data["lng"]
    nc._sinteticas._lat = data["lat"]
    nc.save
        
    return redirect("/sinteticas", code=302)

@router.route('/sinteticas/verGrafo')
def grafo_sinteticas():
    ng = SinteticasGrafo()
    ng.create_graph()
    return render_template("sinteticas/sala.html")

@router.route('/grafo_sinteticas/ver')
def ver_grafo_sinteticas():
    return render_template("d3/grafo.html")

@router.route('/sinteticas/admin')
def admin():
    nc = SinteticasControl()
    grafo = SinteticasGrafo()._grafo
    arraySinteticas = nc.to_dic()
    matriz_adyencia = [
        [
            grafo.weight_edges_E(arraySinteticas[i]["nombre"], arraySinteticas[j]["nombre"])
            if grafo.exist_edge_E(arraySinteticas[i]["nombre"], arraySinteticas[j]["nombre"]) else "--"
            for j in range(len(arraySinteticas))
        ]
        for i in range(len(arraySinteticas))
    ]
    return render_template("sinteticas/adyacencias.html", lista=arraySinteticas, matrizAux=matriz_adyencia)

@router.route('/sinteticas/adyacencia', methods=["POST"])
def crear_ady():
    ndc = SinteticasControl()
    grafo = SinteticasGrafo()._grafo
    data = request.form
    origen, destino = data["origen"], data["destino"]
    
    if origen == destino or grafo.exist_edges(int(origen)-1, int(destino)-1):
        flash('Seleccione un origen y destino distintos' if origen == destino else 'Ya existe una adyacencia entre estas sinteticas', 'error')
    else:
        sinteticaOrigen = ndc._list().binary_search_models(int(origen), "_id")
        sinteticaDestino = ndc._list().binary_search_models(int(destino), "_id")
        SinteticasGrafo().create_graph(sinteticaOrigen, sinteticaDestino)
    
    return redirect("/sinteticas/admin", code=302)

@router.route('/sinteticas/camino', methods=['GET', 'POST'])
def camino():
    graph = Graph()
    with open('data/grafo.json', 'r') as file:
        graph_data = file.read()
        graph.load_from_json(graph_data)

    arraySinteticas = [{'id': id, 'nombre': label} for id, label in graph.vertices.items()]

    if request.method == 'POST':
        origen_id = int(request.form['origen'])
        destino_id = int(request.form['destino'])
        algoritmo = request.form['algoritmo']

        if algoritmo not in ['dijkstra', 'floyd']:
            flash('Algoritmo no soportado.', 'error')
            return render_template('sinteticas/caminoRapido.html', lista=arraySinteticas, camino='', peso_total=None, algoritmo=algoritmo)

        try:
            if algoritmo == 'dijkstra':
                distances, previous_vertices = graph.dijkstra(origen_id)
                path = graph.get_path(previous_vertices, origen_id, destino_id)
                total_distance = distances[destino_id]
            elif algoritmo == 'floyd':
                distances, next_vertices = graph.floyd_warshall()
                path = graph.get_path_floyd(next_vertices, origen_id, destino_id)
                total_distance = distances[origen_id][destino_id]

            if total_distance == math.inf:
                flash('No hay camino disponible entre los puntos seleccionados.', 'error')
                return render_template('sinteticas/caminoRapido.html', lista=arraySinteticas, camino='', peso_total=None, algoritmo=algoritmo)

            # Generar una cadena con el camino completo
            camino = ' -> '.join([graph.vertices[v] for v in path])
            return render_template('sinteticas/caminoRapido.html', lista=arraySinteticas, camino=camino, peso_total=total_distance, algoritmo=algoritmo)

        except KeyError:
            flash('Índice de vértice fuera de rango.', 'error')
            return render_template('sinteticas/caminoRapido.html', lista=arraySinteticas, camino='', peso_total=None, algoritmo=algoritmo)

    # Manejar solicitud GET
    return render_template('sinteticas/caminoRapido.html', lista=arraySinteticas, camino='', peso_total=None)
    
@router.route('/sinteticas/editar/<pos>')
def ver_editarSinteticas(pos):
    fd = SinteticasControl()
    sinteticas = fd._list().get(int(pos)-1)
    print("fsafasf")
    print(sinteticas)
    return render_template("sinteticas/editar.html", data = sinteticas)
    

#MODIFICAR PERSONAS
@router.route('/sinteticas/modificar', methods=["POST"])
def modificar_sinteticas():
    fd = SinteticasControl()
    data = request.form
    pos = data["id"]
    sinteticas1 = fd._list().get(int(data["id"]) -1)
    if not "nombre" in data.keys():
        abort(400)
    
    #TODO ...Validar
    fd._sinteticas = sinteticas1
    fd._sinteticas._id = data ["id"]
    fd._sinteticas._nombre = data["nombre"]
    fd._sinteticas._direccion = data["direccion"]
    fd._sinteticas._horario = data["horario"]
    fd._sinteticas._lng = data["lng"]
    fd._sinteticas._lat = data["lat"]
    fd.merge(int(pos)-1)
    return redirect("/sinteticas", code=302)

@router.route('/sinteticas/eliminar/<int:sintetica_id>', methods=["POST"])
def eliminar_sintetica(sintetica_id):
    fc = SinteticasControl()
    try:
        fc.eliminar(sintetica_id)
        # Elimina la sintética del archivo JSON
        with open('data/sinteticas.json', 'r') as file:
            sinteticas = json.load(file)
        sinteticas = [sintetica for sintetica in sinteticas if sintetica['id'] != sintetica_id]
        with open('data/sinteticas.json', 'w') as file:
            json.dump(sinteticas, file, indent=4)

        return '', 204  # No Content
    except Exception as e:
        print(f"Error: {str(e)}")  # Para depuración
        return '', 500  # Internal Server Error
    
@router.route('/sinteticas/ordenar', methods=["GET"])    
def ordenar_sinteticas():
    sort_attribute = request.args.get('sortAttribute')
    sort_order = request.args.get('sortOrder')
    descending = sort_order == 'descendente'

    # Obtener la lista de sinteticas desde la base de datos o desde una fuente de datos
    lista_sinteticas = SinteticasControl()._list().toArray  # Convierte a una lista si es necesario

    # Ordenar los datos
    if descending:
        lista_sinteticas.sort(key=lambda x: getattr(x, sort_attribute), reverse=True)
    else:
        lista_sinteticas.sort(key=lambda x: getattr(x, sort_attribute))

    # Convertir la lista a formato JSON
    data = [item.serializable for item in lista_sinteticas]

    return jsonify(data)
