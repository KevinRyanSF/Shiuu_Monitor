from abc import ABC, abstractmethod


class UsuarioStrategyAbstract(ABC):

    @abstractmethod
    def pode_acessar_usuarios(self):
        pass

    @abstractmethod
    def pode_acessar_niveis(self):
        pass

    @abstractmethod
    def pode_cadastrar_ambiente(self):
        pass

    @abstractmethod
    def pode_editar_ambiente(self):
        pass

    @abstractmethod
    def pode_deletar_ambiente(self):
        pass