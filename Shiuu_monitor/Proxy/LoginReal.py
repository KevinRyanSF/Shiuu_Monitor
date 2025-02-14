from database import BancoDeDados

class LoginReal:
    def __init__(self, banco):
        self.db = BancoDeDados("Shiuu_monitor.db")

    def autenticar(self, email, senha):
        usuario = self.db.fetch_one("usuarios", "email", email)
        if usuario is None:
            print("Email não encontrado")
            return False
        else:
            if senha == usuario["senha"]:
                return True
            else:
                return False