class Sinteticas():
    def _init_(self) -> None:
        self.__id = 0
        self.__nombre = ''
        self.__direccion = 's/n'
        self.__horario = 's/n'
        self.__lng = "0.0" 
        self.__lat = "0.0"

    @property
    def _lng(self):
        return self.__lng

    @_lng.setter
    def _lng(self, value):
        self.__lng = value

    @property
    def _lat(self):
        return self.__lat

    @_lat.setter
    def _lat(self, value):
        self.__lat = value

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        self.__id = value

    @property
    def _nombre(self):
        return self.__nombre

    @_nombre.setter
    def _nombre(self, value):
        self.__nombre = value

    @property
    def _direccion(self):
        return self.__direccion

    @_direccion.setter
    def _direccion(self, value):
        self.__direccion = value

    @property
    def _horario(self):
        return self.__horario

    @_horario.setter
    def _horario(self, value):
        self.__horario = value

    

    @property
    def serializable(self):
        
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "direccion": self.__direccion,
            "horario": self.__horario,
            "lng": self.__lng,
            "lat": self.__lat
            
        }
    
    def deserializar(data):
        sinteticas = Sinteticas()
        sinteticas._id = data["id"]
        sinteticas._nombre = data["nombre"]
        sinteticas._direccion = data["direccion"]
        sinteticas._horario = data["horario"]
        sinteticas._lng = data["lng"]
        sinteticas._lat = data["lat"]

        return sinteticas
    
    def __str__(self) -> str:
        return (f"ID: {self.__id}, Nombre: {self.__nombre}, Dirección: {self.__direccion}, "
                f"Horario: {self.__horario}, Longitud: {self.__lng}, Latitud: {self.__lat}")
