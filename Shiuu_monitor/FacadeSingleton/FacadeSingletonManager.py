import os, maskpass, copy, time
import threading
import subprocess
from hashlib import sha256

from Classes.Observer.ObserverUsuario import Usuario
from Classes.Observer.GrupoAmbiente import Ambiente
from Classes.nivel import Nivel
from Proxy.ProxyLogin import ProxyLogin
from database import BancoDeDados
from Classes.Relatorio import Relatorio


class FacadeManager:
    _instance = None  # Para o padrão Singleton
    _usuario_logado = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = BancoDeDados("Shiuu_monitor.db")  # Instancia o banco de dados

    def iniciar(self):
        from Commands.CommandExibirMenu import CommandExibirMenu
        menu_command = CommandExibirMenu()  # Criando o comando
        menu_command.execute()  # Executando o menu

    def login(self):
        self.clear_screen()
        print("LOGIN")
        email = input("Digite o email: ")
        password = self.solicitar_senha()
        login_validation = ProxyLogin()
        if login_validation.autenticar(email, password):
            self._usuario_logado = self.db.fetch_one("usuarios", "email", email)
            return True
        else:
            return False

    def get_usuario_logado(self):
        return self._usuario_logado

    def logout(self):
        self._usuario_logado = None

    def solicitar_senha(self):
        senha = maskpass.askpass(prompt="Digite sua senha: ", mask="*")
        return senha

    def encriptar_senha(self, senha):
        hash_senha = sha256(senha.encode())
        return hash_senha.hexdigest()



    def buscar_usuario(self):
        user = self.db.fetch_one("usuarios", "email", input("Digite o email: "))
        if user is None:
            print("Usuario inexistente")
            return False
        else:
            return user

    def buscar_ambiente(self):
        ambiente = self.db.fetch_one("ambientes", "nome", input("Digite o nome do ambiente: "))
        if ambiente is None:
            print("Ambiente inexistente")
            return False
        else:
            return ambiente

    def buscar_niveis(self):
        nivel = self.db.fetch_one("niveis", "nome", input("Digite o nome do nivel: "))
        if nivel is None:
            print("Nivel inexistente")
            return False
        else:
            return nivel


    def escolher_ambientes(self, lista):
        escolha = copy.deepcopy(lista)
        self.listar_ambientes()
        while True:
            amb = int(input("Digite o id do ambiente ou 0 para sair: "))
            if amb == 0: break
            if amb.is_integer() and (self.db.fetch_one("ambientes", "id", amb) is not None):
                if amb in escolha:
                    print("Ambiente já escolhido, tente outro!")
                else:
                    escolha.append(amb)
            else:
                print("Ambiente inexistente, ou digitado errado!")
        return escolha

    def escolher_niveis(self, lista):
        escolha = copy.deepcopy(lista)
        self.listar_niveis()
        while True:
            niv = int(input("Digite o id do nível ou 0 para sair: "))
            if niv == 0: break
            if niv.is_integer() and (self.db.fetch_one("niveis", "id", niv) is not None):
                if niv in escolha:
                    print("Nível já escolhido, tente outro!")
                else:
                    escolha.append(niv)
            else:
                print("Nível inexistente, ou digitado errado!")
        return escolha


    def cadastrar_usuario(self):
        try:
            self.clear_screen()
            print("CADASTRAR USUÁRIO")
            nome = input("Digite o nome de usuário: ")
            email = input("Digite o email: ")
            cargo = int(input("Digite o cargo (0-Fiscal ou 1-Admin): "))
            while True:
                senha = self.solicitar_senha()
                conf_senha = self.solicitar_senha()
                if senha == conf_senha:
                    break
                else:
                    print("Senhas diferentes, digite novamente.")
            senha_armazenada = self.encriptar_senha(senha)
            user = Usuario(nome, email, cargo, senha_armazenada)
            user.cadastrar_usuario()
        except:
            print("Algum dado foi inserido errado!")

    def cadastrar_ambiente(self):
        try:
            self.clear_screen()
            print("CADASTRAR AMBIENTE")
            nome = input("Digite o nome de ambiente: ")
            id = int(input("Digite o id do dispositivo do ambiente: "))
            ip = input("Digite o ip do dispositivo do ambiente: ")
            port = int(input("Digite o porta do dispositivo do ambiente: "))
            ambiente = Ambiente(nome, id, ip, port)
            ambiente.cadastrar_ambiente()
        except:
            print("Algum dado foi inserido errado!")

    def cadastrar_nivel(self):
        try:
            self.clear_screen()
            print("CADASTRAR NIVEL")
            nome = input("Digite o nome de nivel: ")
            limite = int(input("Digite o limite: "))
            alerta = input("Digite a mensagem de alerta: ")
            nivel = Nivel(nome, limite, alerta)
            nivel_data = {
                'nome': nivel.nome,
                'limite': nivel.limite,
                'alerta': nivel.alerta
            }
            self.db.insert("niveis", nivel_data)
        except:
            print("Algum dado foi inserido errado!")

    def listar_usuarios(self):
        self.clear_screen()
        users = self.db.fetch_all("usuarios")
        while True:
            if not users:
                print("Nenhum usuário encontrado")
            else:
                for u in users:
                    amb_ids = []
                    amb = self.db.fetch_all("usuario_ambientes")
                    for a in amb:
                        if a["id_usuario"] == u["id"]:
                            amb_ids.append(a["id_ambiente"])
                    print(f"ID: {u['id']}, Nome: {u['nome']}, Email: {u['email']}, Cargo: {u['cargo']}, Ambientes: {amb_ids}")
            confirma = input("Digite 0 para sair: ")
            if confirma == "0":
                break

    def listar_ambientes(self):
        self.clear_screen()
        ambientes = self.db.fetch_all("ambientes")
        while True:
            if not ambientes:
                print("Nenhum ambiente encontrado")
            else:
                for a in ambientes:
                    niv_ids = []
                    niv = self.db.fetch_all("ambiente_niveis")
                    for n in niv:
                        if n["id_ambiente"] == a["id"]:
                            niv_ids.append(n["id_nivel"])
                    print(f"ID: {a['id']}, Nome: {a['nome']}, Dispositivo_id: {a['dispositivo_id']}, Dispositivo_ip: {a['dispositivo_ip']}, Dispositivo_port: {a['dispositivo_port']}, Níveis: {niv_ids}")
            confirma = input("Digite 0 para sair: ")
            if confirma == "0":
                break

    def listar_niveis(self):
        self.clear_screen()
        niveis = self.db.fetch_all("niveis")
        while True:
            if not niveis:
                print("Nenhum nivel encontrado")
            else:
                for n in niveis:
                    print(f"ID: {n['id']}, Nome: {n['nome']}, Limite(DB): {n['limite']}, alerta: {n['alerta']}")
            confirma = input("Digite 0 para sair: ")
            if confirma == "0":
                break



    def deletar_usuario(self):
        email = input("Digite o email: ")
        user = self.db.fetch_one("usuarios", "email", email)
        if user is None:
            print("Nenhum usuário encontrado")
            pass
        else:
            usuario = Usuario(user["nome"], user["email"], user["cargo"], user["senha"])
            usuario.deletar_usuario()

    def deletar_ambiente(self):
        nome = input("Digite o nome: ")
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        if ambiente is None:
            print("Nenhum ambiente encontrado")
        else:
            amb = Ambiente(ambiente["nome"], ambiente["dispositivo_id"], ambiente["dispositivo_ip"], ambiente["dispositivo_port"])
            amb.deletar_ambiente()

    def deletar_nivel(self):
        nome = input("Digite o nome: ")
        nivel = self.db.fetch_one("niveis", "nome", nome)
        if nivel is None:
            print("Nenhum nível encontrado")
        else:
            niv = Nivel(nivel["nome"], nivel["limite"], nivel["alerta"])
            niv.deletar_nivel()



    def editar_nome_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        usuario = Usuario(user["nome"], user["email"], user["cargo"], user["senha"])
        usuario.editar_nome_usuario()

    def editar_cargo_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        usuario = Usuario(user["nome"], user["email"], user["cargo"], user["senha"])
        usuario.editar_cargo_usuario()

    def editar_senha_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        usuario = Usuario(user["nome"], user["email"], user["cargo"], user["senha"])
        usuario.editar_senha_usuario()

    def adicionar_ambientes_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        escolha = []
        if user["cargo"] == 0:
            amb = self.db.fetch_all("usuario_ambientes")
            for a in amb:
                if a["id_usuario"] == user["id"]:
                    escolha.append(a["id_ambiente"])
            print("Escolha os ambientes do usuário:")
            time.sleep(2)
            escolha_amb = self.escolher_ambientes(escolha)
            for i in escolha_amb:
                if i not in escolha:
                    data_rel_user_amb = {
                        'id_usuario': user['id'],
                        'id_ambiente': i,
                    }
                    self.db.insert("usuario_ambientes", data_rel_user_amb)
        else:
            ambientes = self.db.fetch_all("ambientes")
            if not ambientes:
                return False
            else:
                for a in ambientes:
                    data_rel_user_amb = {
                        'id_usuario': user['id'],
                        'id_ambiente': a["id"],
                    }
                    self.db.insert("usuario_ambientes", data_rel_user_amb)

                print("Valor alterado com sucesso!")

    def remover_ambientes_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        amb_user = []
        if user["cargo"] == 0:
            amb = self.db.fetch_all("usuario_ambientes")
            for a in amb:
                if a["id_usuario"] == user["id"]:
                    amb_user.append(a["id_ambiente"])
            print("Escolha os ambientes do usuário a serem removidos:")
            print(f"ID: {user['id']}, Nome: {user['nome']}, Email: {user['email']}, Cargo: {user['cargo']}, Ambientes: {amb_user}")
            remove_amb = []
            while True:
                escolha = int(input("Digite o id do ambiente a ser removido, ou 0 para sair: "))
                if escolha == 0: break
                if escolha.is_integer() and (self.db.fetch_one("ambientes", "id", escolha) is not None):
                    if escolha in remove_amb:
                        print("Ambiente já escolhido, tente outro!")
                    else:
                        remove_amb.append(escolha)
                else:
                    print("Ambiente inexistente, ou digitado errado!")
            for i in remove_amb:
                self.db.delete("usuario_ambientes", "id_ambiente", i)
                print("Campo removido!")



    def editar_nome_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        amb = Ambiente(ambiente["nome"], ambiente["dispositivo_id"], ambiente["dispositivo_ip"],
                       ambiente["dispositivo_port"])
        amb.deletar_ambiente()

    def editar_dispositivo_id_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        amb = Ambiente(ambiente["nome"], ambiente["dispositivo_id"], ambiente["dispositivo_ip"],
                       ambiente["dispositivo_port"])
        amb.editar_dispositivo_id_ambiente()

    def editar_dispositivo_ip_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "id", nome)
        amb = Ambiente(ambiente["nome"], ambiente["dispositivo_id"], ambiente["dispositivo_ip"],
                       ambiente["dispositivo_port"])
        amb.editar_dispositivo_ip_ambiente()

    def editar_dispositivo_port_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "id", nome)
        amb = Ambiente(ambiente["nome"], ambiente["dispositivo_id"], ambiente["dispositivo_ip"],
                       ambiente["dispositivo_port"])
        amb.editar_dispositivo_port_ambiente()

    def adicionar_niveis_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        escolha = []
        niv = self.db.fetch_all("ambiente_niveis")
        for a in niv:
            if a["id_ambiente"] == ambiente["id"]:
                escolha.append(a["id_nivel"])
        print("Escolha os níveis do ambiente:")
        time.sleep(2)
        escolha_niv = self.escolher_niveis(escolha)
        for i in escolha_niv:
            if i not in escolha:
                data_rel_amb_niv = {
                    'id_ambiente': ambiente['id'],
                    'id_nivel': i,
                }
                self.db.insert("ambiente_niveis", data_rel_amb_niv)
        print("Valor alterado com sucesso!")

    def remover_niveis_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        niv_amb = []
        niv = self.db.fetch_all("ambiente_niveis")
        for a in niv:
            if a["id_ambiente"] == ambiente["id"]:
                niv_amb.append(a["id_nivel"])
        print("Escolha os níveis do ambiente a serem removidos:")
        print(f"ID: {ambiente['id']}, Nome: {ambiente['nome']}, Dispositivo_id: {ambiente['dispositivo_id']}, Dispositivo_ip: {ambiente['dispositivo_ip']}, Dispositivo_port: {ambiente['dispositivo_port']}, Níveis: {niv_amb}")
        remove_niv = []
        while True:
            escolha = int(input("Digite o id do nível a ser removido, ou 0 para sair: "))
            if escolha == 0: break
            if escolha.is_integer() and (self.db.fetch_one("niveis", "id", escolha) is not None):
                if escolha in remove_niv:
                    print("Nível já escolhido, tente outro!")
                else:
                    remove_niv.append(escolha)
            else:
                print("Nível inexistente, ou digitado errado!")
        for i in remove_niv:
            self.db.delete("ambiente_niveis", "id_nivel", i)
            print("Campo removido!")



    def editar_nome_nivel(self, nome):
        nivel = self.db.fetch_one("niveis", "nome", nome)
        niv = Nivel(nivel["nome"], nivel["limite"], nivel["alerta"])
        niv.editar_nome_nivel()

    def editar_limite_nivel(self, nome):
        nivel = self.db.fetch_one("niveis", "nome", nome)
        niv = Nivel(nivel["nome"], nivel["limite"], nivel["alerta"])
        niv.editar_limite_nivel()

    def editar_alerta_nivel(self, nome):
        nivel = self.db.fetch_one("niveis", "nome", nome)
        niv = Nivel(nivel["nome"], nivel["limite"], nivel["alerta"])
        niv.editar_alerta_nivel()

    def abrir_monitoramento(self, ambiente_nome):
        """Abre um novo terminal do CMD e inicia o monitoramento de um ambiente específico."""
        # Obtém os dados do ambiente pelo nome
        ambiente = self.db.fetch_one("ambientes", "nome", ambiente_nome)
        if not ambiente:
            print(f"Erro: Ambiente '{ambiente_nome}' não encontrado no banco de dados.")
            return
        # Caminho completo para o script monitorar_ambiente.py
        script_path = r"C:\Shiuu_monitor\monitorar_ambiente.py"
        # Monta o comando para executar o script em uma nova janela do terminal
        comando = [
            "start", "cmd", "/k",
            "python", script_path,
            ambiente["nome"],  # Passa o nome sem aspas
            str(ambiente["dispositivo_id"]),  # Passa o dispositivo_id como inteiro
            ambiente["dispositivo_ip"],  # Passa o IP sem aspas
            str(ambiente["dispositivo_port"])  # Passa a porta como inteiro
        ]
        def abrir_terminal():
            """Abre uma nova janela do CMD e executa o comando"""
            try:
                # Usa subprocess.Popen para abrir uma nova janela do terminal
                subprocess.Popen(comando, shell=True)
            except Exception as e:
                print(f"Erro ao abrir o terminal: {e}")
        # Inicia uma nova thread para evitar que o programa principal trave
        thread = threading.Thread(target=abrir_terminal)
        thread.start()


    def gerar_relatorio(self):
        relatorio = Relatorio()
        relatorio.gerar_historico()

    def clear_screen(self):
        """Método privado para limpar a tela."""
        os.system('cls' if os.name == 'nt' else 'clear')
