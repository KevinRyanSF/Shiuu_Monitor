from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, ambiente, dado):
        pass