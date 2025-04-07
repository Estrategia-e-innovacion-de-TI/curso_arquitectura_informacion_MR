import folium
import osmnx as ox
import random
import networkx as nx
from geopy.distance import geodesic


class TrackingService:
    """
    Servicio de seguimiento y simulación de rutas para vendedores en Medellín, Colombia.
    Utiliza OSMnx para construir el grafo vial y genera rutas reales y simuladas.
    """

    def __init__(self):
        """
        Inicializa el grafo de la ciudad de Medellín con la red vial tipo 'drive'.
        """
        self.graph = ox.graph_from_place("Medellín, Colombia", network_type="drive")

    def get_route(self, origin, destination):
        """
        Calcula la ruta más corta entre dos coordenadas geográficas.

        Args:
            origin (tuple): Coordenadas de inicio (lat, lon).
            destination (tuple): Coordenadas de destino (lat, lon).

        Returns:
            list: Lista de tuplas (lat, lon) que representan la ruta.
        """
        orig_node = ox.distance.nearest_nodes(self.graph, origin[1], origin[0])
        dest_node = ox.distance.nearest_nodes(self.graph, destination[1], destination[0])
        route = nx.shortest_path(self.graph, orig_node, dest_node, weight="length")
        return [(self.graph.nodes[n]['y'], self.graph.nodes[n]['x']) for n in route]

    def get_real_routes(self, num_valid=30, num_invalid=5):
        """
        Genera rutas válidas simuladas y rutas reales con posibles discrepancias.

        Args:
            num_valid (int): Número de rutas válidas a generar.
            num_invalid (int): Número de rutas reales con discrepancias a introducir.

        Returns:
            tuple: Dos listas de rutas:
                - valid_routes: Rutas planeadas (simuladas).
                - real_routes: Rutas realmente recorridas (con posibles desviaciones).
        """
        nodes = list(self.graph.nodes())
        valid_routes = []

        for _ in range(num_valid):
            start, end = random.sample(nodes, 2)
            route = self.get_route(
                (self.graph.nodes[start]['y'], self.graph.nodes[start]['x']),
                (self.graph.nodes[end]['y'], self.graph.nodes[end]['x'])
            )
            valid_routes.append(route)

        real_routes = [r.copy() for r in valid_routes]

        for _ in range(num_invalid):
            idx = random.randint(0, len(real_routes) - 1)
            start, end = random.sample(nodes, 2)
            real_routes[idx] = self.get_route(
                (self.graph.nodes[start]['y'], self.graph.nodes[start]['x']),
                (self.graph.nodes[end]['y'], self.graph.nodes[end]['x'])
            )

        return valid_routes, real_routes

    def plot_routes_with_discrepancies(self, valid_routes, real_routes, discrepancies, filename="./graphics/rutas_medellin_discrepancias.html"):
        """
        Visualiza rutas válidas y rutas con discrepancias en un mapa de Medellín usando Folium.

        Args:
            valid_routes (list): Lista de rutas simuladas.
            real_routes (list): Lista de rutas reales recorridas.
            discrepancies (list): Lista de booleanos indicando discrepancias por ruta.
            filename (str): Ruta de archivo donde guardar el HTML del mapa.

        Returns:
            str: Ruta del archivo HTML generado.
        """
        map_mde = folium.Map(location=[6.25, -75.58], zoom_start=13)

        # Rutas válidas (azul)
        for route in valid_routes:
            folium.PolyLine(route, color='blue', weight=3, opacity=0.6, tooltip="Ruta Válida").add_to(map_mde)

        # Rutas reales con discrepancia (rojo)
        for idx, (route, has_discrepancy) in enumerate(zip(real_routes, discrepancies)):
            if has_discrepancy:
                folium.PolyLine(route, color='red', weight=3, opacity=0.8, tooltip=f"Ruta Real #{idx} con Discrepancia").add_to(map_mde)

        map_mde.save(filename)
        return filename


class VerificationService:
    """
    Servicio de verificación que compara rutas planeadas y rutas reales para detectar desviaciones significativas.
    """

    def detect_inconsistencies(self, reported_route, actual_route, threshold_km=0.5):
        """
        Verifica si una ruta real se desvía significativamente de una ruta reportada.

        Args:
            reported_route (list): Ruta esperada como lista de coordenadas (lat, lon).
            actual_route (list): Ruta realmente seguida.
            threshold_km (float): Distancia en kilómetros para considerar una discrepancia.

        Returns:
            bool: True si hay discrepancia, False si la ruta es consistente.
        """
        for r, a in zip(reported_route, actual_route):
            if geodesic(r, a).km > threshold_km:
                return True
        return False

    def validate_routes(self, reported_routes, real_routes):
        """
        Valida múltiples rutas para detectar discrepancias.

        Args:
            reported_routes (list): Lista de rutas esperadas.
            real_routes (list): Lista de rutas reales.

        Returns:
            list: Lista de booleanos indicando si hubo discrepancia en cada ruta.
        """
        return [self.detect_inconsistencies(r, a) for r, a in zip(reported_routes, real_routes)]