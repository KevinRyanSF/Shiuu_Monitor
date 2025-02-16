import os, maskpass, copy, time

from Classes.Observer.ObserverUsuario import Usuario
from Classes.Observer.ObserverAmbiente import Ambiente
from Classes.nivel import Nivel
from Proxy.ProxyLogin import ProxyLogin
from database import BancoDeDados
from hashlib import sha256
from datetime import datetime
from fpdf import FPDF


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
        usuario_data = {
            'nome': user.nome,
            'email': user.email,
            'cargo': user.cargo,
            'senha': user.senha
        }
        self.db.insert("usuarios", usuario_data)
        user = self.db.fetch_one("usuarios", "email", user.email)
        if cargo == 0:
            print("Escolha os ambientes do usuário:")
            time.sleep(2)
            escolha = self.escolher_ambientes([])
            for i in escolha:
                data_rel_user_amb = {
                    'id_usuario': user['id'],
                    'id_ambiente': i,
                }
                self.db.insert("usuario_ambientes", data_rel_user_amb)

        else:
            all_ambientes = self.db.fetch_all("ambientes")
            if not all_ambientes:
                pass
            else:
                for i in all_ambientes:
                    data_rel_user_amb = {
                        'id_usuario': user['id'],
                        'id_ambiente': i['id'],
                    }
                    self.db.insert("usuario_ambientes", data_rel_user_amb)

    def cadastrar_ambiente(self):
        self.clear_screen()
        print("CADASTRAR AMBIENTE")
        nome = input("Digite o nome de ambiente: ")
        id = int(input("Digite o id do dispositivo do ambiente: "))
        ip = input("Digite o ip do dispositivo do ambiente: ")
        port = int(input("Digite o porta do dispositivo do ambiente: "))
        ambiente = Ambiente(nome, id, ip, port)
        ambiente_data = {
            'nome': ambiente.nome,
            'dispositivo_id': ambiente.dispositivo_id,
            'dispositivo_ip': ambiente.dispositivo_ip,
            'dispositivo_port': ambiente.dispositivo_port
        }
        self.db.insert("ambientes", ambiente_data)
        amb = self.db.fetch_one("ambientes", "nome", ambiente.nome)
        print("Escolha os níveis do ambiente:")
        time.sleep(2)
        escolha = self.escolher_niveis([])
        for i in escolha:
            data_rel_amb_niv = {
                'id_ambiente': amb['id'],
                'id_nivel': i,
            }
            self.db.insert("ambiente_niveis", data_rel_amb_niv)
        admins = self.db.fetch_all("usuarios")
        if not admins:
            pass
        else:
            for u in admins:
                data_rel_usu_amb = {
                    'id_usuario': u['id'],
                    'id_ambiente': amb['id'],
                }
                self.db.insert("usuario_ambientes", data_rel_usu_amb)

    def cadastrar_nivel(self):
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
        else:
            confirma = input(f"Deseja deletar o Usuário: {user['nome']}? [Y/N]").upper()
            if confirma == "Y":
                self.db.delete("usuarios", "email", email)
                print("Usuário deletado com sucesso!")
                return True
            else:
                return False

    def deletar_ambiente(self):
        nome = input("Digite o nome: ")
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        if ambiente is None:
            print("Nenhum ambiente encontrado")
        else:
            confirma = input(f"Deseja deletar o ambiente: {ambiente['nome']}? [Y/N]").upper()
            if confirma == "Y":
                self.db.delete("ambientes", "nome", nome)
                print("Ambiente deletado com sucesso!")
                return True
            else:
                return False

    def deletar_nivel(self):
        nome = input("Digite o nome: ")
        nivel = self.db.fetch_one("niveis", "nome", nome)
        if nivel is None:
            print("Nenhum nível encontrado")
        else:
            confirma = input(f"Deseja deletar o ambiente: {nivel['nome']}? [Y/N]").upper()
            if confirma == "Y":
                self.db.delete("niveis", "nome", nome)
                print("Nível deletado com sucesso!")
                return True
            else:
                return False



    def editar_nome_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        nome = input("Digite o novo nome: ")
        if nome == user["nome"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("usuarios", "nome", "email", nome, user["email"])
            print("Valor alterado com sucesso!")

    def editar_cargo_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        cargo = int(input("Digite o novo cargo (0 ou 1): "))
        if cargo == user["cargo"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("usuarios", "cargo", "email", cargo, user["email"])
            print("Valor alterado com sucesso!")

    def editar_senha_usuario(self, email):
        user = self.db.fetch_one("usuarios", "email", email)
        senha = self.solicitar_senha()
        senha = self.encriptar_senha(senha)
        if senha == user["senha"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("usuarios", "senha", "email", senha, user["email"])
            print("Valor alterado com sucesso!")

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
        novo_nome = input("Digite o novo nome do ambiente: ")
        if novo_nome == ambiente["nome"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("ambientes", "nome", "nome", novo_nome, ambiente["nome"])
            print("Nome do ambiente alterado com sucesso!")

    def editar_dispositivo_id_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "nome", nome)
        novo_id = input("Digite o novo ID do dispositivo: ")
        if novo_id == ambiente["dispositivo_id"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("ambientes", "dispositivo_id", "nome", novo_id, ambiente["nome"])
            print("ID do dispositivo alterado com sucesso!")

    def editar_dispositivo_ip_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "id", nome)
        novo_ip = input("Digite o novo IP do dispositivo: ")
        if novo_ip == ambiente["dispositivo_ip"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("ambientes", "dispositivo_ip", "nome", novo_ip, ambiente["nome"])
            print("IP do dispositivo alterado com sucesso!")

    def editar_dispositivo_port_ambiente(self, nome):
        ambiente = self.db.fetch_one("ambientes", "id", nome)
        nova_porta = input("Digite a nova porta do dispositivo: ")
        if nova_porta == ambiente["dispositivo_port"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("ambientes", "dispositivo_port", "nome", nova_porta, ambiente["nome"])
            print("Porta do dispositivo alterada com sucesso!")

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
        nome = input("Digite o novo nome: ")
        if nome == nivel["nome"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("niveis", "nome", "nome", nome, nivel["nome"])
            print("Valor alterado com sucesso!")

    def editar_limite_nivel(self, nome):
        nivel = self.db.fetch_one("niveis", "nome", nome)
        limite = int(input("Digite o novo limite: "))
        if limite == nivel["limite"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("niveis", "limite", "nome", limite, nivel["nome"])
            print("Valor alterado com sucesso!")

    def editar_alerta_nivel(self, nome):
        nivel = self.db.fetch_one("niveis", "nome", nome)
        alerta = input("Digite a mensagem de alerta: ")
        if alerta == nivel["alerta"]:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.db.update("niveis", "alerta", "nome", alerta, nivel["nome"])
            print("Valor alterado com sucesso!")


    def gerar_relatorio(self):
        # Solicita as datas ao usuário
        data_init = input("Digite a data inicial (Ex.: dd-mm-yyyy): ")
        data_end = input("Digite a data final (Ex.: dd-mm-yyyy): ")

        # Converte as datas para datetime.date
        try:
            data_init = datetime.strptime(data_init, "%d-%m-%Y").date()
            data_end = datetime.strptime(data_end, "%d-%m-%Y").date()
        except ValueError:
            print("Formato de data inválido. Use dd-mm-yyyy.")
            return

        # Busca todas as medições no banco de dados
        medicoes = self.db.fetch_all("medicoes")

        # Ordena medições por ambiente
        sorted_medicoes = sorted(medicoes, key=lambda amb: amb["nome_ambiente"])

        # Dicionário para agrupar medições por ambiente
        ambientes_relatorio = {}

        for medicao in sorted_medicoes:
            # Converte o campo 'data' (ISO 8601) para datetime
            try:
                timestamp_dt = datetime.fromisoformat(medicao["data"])  # Use fromisoformat() para string ISO 8601
            except ValueError as e:
                print(f"Erro ao converter timestamp: {e}")
                continue

            timestamp_data = timestamp_dt.date()  # Apenas a data para filtro
            timestamp_hora = timestamp_dt.strftime("%H:%M:%S")  # Apenas a hora para exibir

            # Filtra medições dentro do intervalo de datas
            if data_init <= timestamp_data <= data_end:
                ambiente_nome = medicao["nome_ambiente"]
                registro = f"{timestamp_data.strftime('%d/%m/%Y')} {timestamp_hora} - Valor: {medicao['valor']}dB"

                if ambiente_nome not in ambientes_relatorio:
                    ambientes_relatorio[ambiente_nome] = []

                ambientes_relatorio[ambiente_nome].append(registro)

        # Exibe o relatório formatado
        if not ambientes_relatorio:
            print("Nenhuma medição encontrada no período especificado.")
            return

        print("\n=== RELATÓRIO DE MEDIÇÕES ===")
        for ambiente, registros in ambientes_relatorio.items():
            print(f"\n🔹 Ambiente: {ambiente}")
            for registro in registros:
                print(registro)

        while True:
            pdf = input("Deseja gerar pdf? [y/n]: ").lower()
            if pdf == "y":
                break
            elif pdf == "n":
                return 0
            else:
                print("Digite uma opção válida.")

        # Verifica se há dados para gerar o relatório
        if not ambientes_relatorio:
            print("Nenhuma medição encontrada no período especificado.")
            return

        # Criando o PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        # Título do documento
        pdf.cell(200, 10, "Relatório de Medições", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Período: {data_init.strftime('%d/%m/%Y')} a {data_end.strftime('%d/%m/%Y')}", ln=True,
                 align="C")
        pdf.ln(10)

        # Adicionando os dados ao PDF
        for ambiente, registros in ambientes_relatorio.items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, f"Ambiente: {ambiente}", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", "", 12)
            for registro in registros:
                pdf.multi_cell(0, 8, registro)
            pdf.ln(10)

        # Salvar PDF
        nome_arquivo = f"relatorio_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
        pdf.output(nome_arquivo)

        print(f"Relatório gerado com sucesso: {nome_arquivo}")

    def clear_screen(self):
        """Método privado para limpar a tela."""
        os.system('cls' if os.name == 'nt' else 'clear')
