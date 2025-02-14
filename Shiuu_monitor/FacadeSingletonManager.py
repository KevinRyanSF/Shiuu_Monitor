import os
from Classes.usuario import Usuario
from Proxy.ProxyLogin import ProxyLogin
from database import BancoDeDados


class FacadeManager:
    _instance = None  # Para o padrão Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = BancoDeDados("Shiuu_monitor.db")  # Instancia o banco de dados

    def login(self):
        self.clear_screen()
        print("LOGIN")
        email = input("Digite o email: ")
        password = input("Digite a senha: ")
        login_validation = ProxyLogin()
        return login_validation.autenticar(email, password)


    def buscar_usuario(self):
        user = self.db.fetch_one("usuarios", "email", input("Digite o email: "))
        if user is None:
            print("Usuario inexistente")
            return False
        else:
            return user

    def cadastrar_usuario(self):
        self.clear_screen()
        print("CADASTRAR USUÁRIO")
        nome = input("Digite o nome de usuário: ")
        email = input("Digite o email: ")
        cargo = int(input("Digite o cargo (0 ou 1): "))
        while True:
            senha = input("Digite a senha: ")
            conf_senha = input("Confirme a senha: ")
            if senha == conf_senha:
                break
            else:
                print("Senhas diferentes, digite novamente.")
        user = Usuario(nome, email, cargo, senha)
        usuario_data = {
            'nome': user.nome,
            'email': user.email,
            'cargo': user.cargo,
            'senha': user.senha
        }
        self.db.insert("usuarios", usuario_data)

    def listar_usuarios(self):
        self.clear_screen()
        users = self.db.fetch_all("usuarios")
        if users is None:
            print("Nenhum usuário encontrado")
        else:
            for u in users:
                print(f"ID: {u["id"]}, Nome: {u['nome']}, Email: {u['email']}, Cargo: {u['cargo']}")

    def deletar_usuario(self):
        email = input("Digite o email: ")
        user = self.db.fetch_one("usuarios", "email", email)
        if user is None:
            print("Nenhum usuário encontrado")
        else:
            confirma = input(f"Deseja deletar o Usuário: {user['nome']}? [Y/N]").upper()
            if confirma == "Y":
                self.db.delete("usuarios", "email", email)
                return True
            else:
                return False

    def editar_usuario(self):
        email = input("Digite o email: ")
        user = self.db.fetch_one("usuarios", "email", email)
        if user is None:
            print("Usuário não encontrado")
        else:
            print(f"ID: {user["id"]}, Nome: {user['nome']}, Email: {user['email']}, Cargo: {user['cargo']}")
            while True:
                print(f"Editar {user['nome']}")
                print("+--------------------------------------+")
                print("| 1. NOME                              |")
                print("| 2. CARGO                             |")
                print("| 3. SENHA                             |")
                print("| 4. SAIR                              |")
                print("+--------------------------------------+")
                opcao = input("ESCOLHA UMA OPÇÃO: ")

                if opcao == "1":
                    while True:
                        nome = input("Digite o novo nome: ")
                        if nome == user["nome"]:
                            print("Valor igual ao atual, insira outro valor.")
                        else:
                            self.db.update("usuarios", "nome", "email", nome, user["email"])
                            break
                elif opcao == "2":
                    while True:
                        cargo = int(input("Digite o novo cargo (0 ou 1): "))
                        if cargo == user["cargo"]:
                            print("Valor igual ao atual, insira outro valor.")
                        else:
                            self.db.update("usuarios", "cargo", "email", cargo, user["email"])
                            break
                elif opcao == "3":
                    while True:
                        senha = int(input("Digite o nova senha: "))
                        if senha == user["senha"]:
                            print("Valor igual ao atual, insira outro valor.")
                        else:
                            self.db.update("usuarios", "senha", "email", senha, user["email"])
                            break
                else:
                    break

    def clear_screen(self):
        """Método privado para limpar a tela."""
        os.system('cls' if os.name == 'nt' else 'clear')
