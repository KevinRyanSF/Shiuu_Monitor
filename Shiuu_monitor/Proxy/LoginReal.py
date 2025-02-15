from database import BancoDeDados
from hashlib import sha256

class LoginReal:
    def __init__(self, banco):
        self.db = BancoDeDados("Shiuu_monitor.db")

    def autenticar(self, email, senha):
        usuario = self.db.fetch_one("usuarios", "email", email)
        if usuario is None:
            print("Email não encontrado")
            return False
        else:
            senha_crip = usuario["senha"]
            senha = sha256(senha.encode()).hexdigest()
            if senha == senha_crip:
                return True
            else:
                return False