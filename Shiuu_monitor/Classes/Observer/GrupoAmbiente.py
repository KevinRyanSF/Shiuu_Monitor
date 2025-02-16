import requests
import time
from datetime import datetime, timedelta
from Classes.Observer.GrupoAbstract import GrupoAbstract
from Classes.Observer.ObserverUsuario import Usuario

class Ambiente(GrupoAbstract):
    def __init__(self, nome, dispositivo_id, dispositivo_ip, dispositivo_port):
        from FacadeSingleton.FacadeSingletonManager import FacadeManager
        self.__facade = FacadeManager()
        self.nome = nome
        self.dispositivo_id = dispositivo_id
        self.dispositivo_ip = dispositivo_ip
        self.dispositivo_port = dispositivo_port
        self.ultima_notificacao = datetime.now() - timedelta(minutes=5)



    def notificar(self, **kwargs):
        ambiente_atual = self.__facade.db.fetch_one("ambientes", "nome", self.nome)
        usuarios_id = self.__facade.db.search_all_by("usuario_ambientes", "id_ambiente", ambiente_atual["id"])
        usuarios = []
        for id in usuarios_id:
            usuario = self.__facade.db.fetch_one("usuarios", "id", id["id_usuario"])
            if not usuario:
                break
            usuarios.append(usuario)
        if usuarios != []:
            for u in usuarios:
                user = Usuario(u["nome"], u["email"], u["cargo"], u["senha"])
                user.update(self.nome)

    def monitorar_ambiente_loop(self):
        while True:
            self.monitorar_ambiente()
            time.sleep(5)

    def monitorar_ambiente(self):
        FLASK_SERVER_URL = f"http://{self.dispositivo_ip}:{self.dispositivo_port}/coleta"  # Substitua pelo IP correto se necessário

        try:
            response = requests.get(FLASK_SERVER_URL)
            if response.status_code == 200:
                data = response.json()
                if data["id"] == self.dispositivo_id:
                    amb_atual = self.__facade.db.fetch_one("ambientes", "nome", self.nome)
                    niveis_id = self.__facade.db.search_all_by("ambiente_niveis", "id_ambiente", amb_atual["id"])
                    niveis = []
                    for id in niveis_id:
                        nivel = self.__facade.db.fetch_one("niveis", "id", id["id_nivel"])
                        if not nivel:
                            break
                        niveis.append(nivel)
                    if niveis != []:
                        sorted_niveis = sorted(niveis, key=lambda n: n["limite"], reverse=True)
                        for lim in sorted_niveis:
                            if lim["limite"] < data["dado_gerado"]:
                                print(lim["alerta"])

                                timestamp_atual = datetime.fromisoformat(data["timestamp"])
                                if self.ultima_notificacao and (timestamp_atual - self.ultima_notificacao) < timedelta(
                                        minutes=5):
                                    continue
                                data_medicao = {
                                    'nome_ambiente': amb_atual["nome"],
                                    'valor': data["dado_gerado"],
                                    'data': data["timestamp"]
                                }
                                self.__facade.db.insert("medicoes", data_medicao)

                                self.ultima_notificacao = timestamp_atual
                                self.notificar()
                                break
                            else:
                                continue
            else:
                print(f"Erro ao coletar número: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")


    def cadastrar_ambiente(self):
        ambiente_data = {
            'nome': self.nome,
            'dispositivo_id': self.dispositivo_id,
            'dispositivo_ip': self.dispositivo_ip,
            'dispositivo_port': self.dispositivo_port
        }
        self.__facade.db.insert("ambientes", ambiente_data)
        amb = self.__facade.db.fetch_one("ambientes", "nome", self.nome)
        print("Escolha os níveis do ambiente:")
        time.sleep(2)
        escolha = self.__facade.escolher_niveis([])
        for i in escolha:
            data_rel_amb_niv = {
                'id_ambiente': amb['id'],
                'id_nivel': i,
            }
            self.__facade.db.insert("ambiente_niveis", data_rel_amb_niv)
        admins = self.__facade.db.fetch_all("usuarios")
        if not admins:
            pass
        else:
            for u in admins:
                data_rel_usu_amb = {
                    'id_usuario': u['id'],
                    'id_ambiente': amb['id'],
                }
                self.__facade.db.insert("usuario_ambientes", data_rel_usu_amb)

    def deletar_ambiente(self):
        confirma = input(f"Deseja deletar o ambiente: {self.nome}? [Y/N]").upper()
        if confirma == "Y":
            self.__facade.db.delete("ambientes", "nome", self.nome)
            print("Ambiente deletado com sucesso!")
            return True
        else:
            return False

    def editar_nome_ambiente(self):
        novo_nome = input("Digite o novo nome do ambiente: ")
        if novo_nome == self.nome:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("ambientes", "nome", "nome", novo_nome, self.nome)
            print("Nome do ambiente alterado com sucesso!")

    def editar_dispositivo_id_ambiente(self):
        novo_id = input("Digite o novo ID do dispositivo: ")
        if novo_id == self.dispositivo_id:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("ambientes", "dispositivo_id", "nome", novo_id, self.nome)
            print("ID do dispositivo alterado com sucesso!")

    def editar_dispositivo_ip_ambiente(self):
        novo_ip = input("Digite o novo IP do dispositivo: ")
        if novo_ip == self.dispositivo_ip:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("ambientes", "dispositivo_ip", "nome", novo_ip, self.nome)
            print("IP do dispositivo alterado com sucesso!")

    def editar_dispositivo_port_ambiente(self):
        nova_porta = input("Digite a nova porta do dispositivo: ")
        if nova_porta == self.dispositivo_port:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("ambientes", "dispositivo_port", "nome", nova_porta, self.nome)
            print("Porta do dispositivo alterada com sucesso!")