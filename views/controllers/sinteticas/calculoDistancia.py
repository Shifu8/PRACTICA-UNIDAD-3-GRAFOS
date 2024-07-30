import math

class CalculoDistancia:
    @staticmethod
    def calcularDistancia(lng1, lat1, lng2, lat2):
        try:
            # Convertir entradas a flotantes
            lng1 = float(lng1)
            lat1 = float(lat1)
            lng2 = float(lng2)
            lat2 = float(lat2)
        except ValueError:
            raise ValueError("Las coordenadas deben ser números reales.")
        
        # Radio de la Tierra en kilómetros
        R = 6371.0
        
        # Convertir grados a radianes
        lng1_rad = math.radians(lng1)
        lat1_rad = math.radians(lat1)
        lng2_rad = math.radians(lng2)
        lat2_rad = math.radians(lat2)
        
        # Diferencias de coordenadas
        d_lng = lng2_rad - lng1_rad
        d_lat = lat2_rad - lat1_rad
        
        # Fórmula del Haversine
        a = math.sin(d_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distancia = R * c
        
        return distancia