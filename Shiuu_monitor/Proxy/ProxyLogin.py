from Proxy.LoginReal import LoginReal

class ProxyLogin:
    def __init__(self):
        self.real = LoginReal("Shiuu_monitor.db")
        self.tentativas = {}

    def autenticar(self, email, senha):
        if email == "" or senha == "":
            print("Email e senha não podem estar vazios.")
            return False
        resposta = self.real.autenticar(email, senha)
        if not resposta:
            print("Email ou senha incorretos.")
        return resposta