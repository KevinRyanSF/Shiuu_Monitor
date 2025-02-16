from abc import ABC, abstractmethod

class GrupoAbstract(ABC):
    @abstractmethod
    def notificar(self, ambiente, dado):
        pass