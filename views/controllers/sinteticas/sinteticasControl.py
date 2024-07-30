from controllers.tda.linked.linkedList import Linked_List
from controllers.dao.daoAdapter import DaoAdapter
from models.sinteticas import Sinteticas

class SinteticasControl(DaoAdapter):
    def __init__(self):
        super().__init__(Sinteticas)
        self.__sinteticas= None

    @property
    def _sinteticas(self):
        if self.__sinteticas == None:
            self.__sinteticas = Sinteticas()
        return self.__sinteticas

    @_sinteticas.setter
    def _sinteticas(self, value):
        self.__sinteticas = value

    def _lista(self):
        return self._list()

    @property
    def save(self):
        #self._negocio._id = self.lista._length + 1
        self._save(self._sinteticas)

    def merge(self, pos):
        self._merge(self._sinteticas, pos)
    
    def eliminar(self, pos):
        self._delete(pos)
        
    
    
    
    