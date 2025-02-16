from abc import ABC, abstractmethod

class ObserverAbstract(ABC):
    @abstractmethod
    def update(self, ambiente, dado):
        pass