from Strategy.StrategyUsuarioAbstract import UsuarioStrategy


class UsuarioAdmin(UsuarioStrategy):

    def pode_acessar_usuarios(self):
        return True

    def pode_acessar_niveis(self):
        return True

    def pode_cadastrar_ambiente(self):
        return True

    def pode_editar_ambiente(self):
        return True

    def pode_deletar_ambiente(self):
        return True


class UsuarioFiscal(UsuarioStrategy):

    def pode_acessar_usuarios(self):
        print("Acesso negado, requer nível de administrador!")
        return False

    def pode_acessar_niveis(self):
        print("Acesso negado, requer nível de administrador!")
        return False

    def pode_cadastrar_ambiente(self):
        print("Acesso negado, requer nível de administrador!")
        return False

    def pode_editar_ambiente(self):
        print("Acesso negado, requer nível de administrador!")
        return False

    def pode_deletar_ambiente(self):
        print("Acesso negado, requer nível de administrador!")
        return False