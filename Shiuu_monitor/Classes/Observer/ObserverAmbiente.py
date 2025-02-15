import requests
import time
from Classes.Observer.ObserverUsuario import Usuario

class Ambiente:
    def __init__(self, nome, dispositivo_id, dispositivo_ip, dispositivo_port):
        from FacadeSingleton.FacadeSingletonManager import FacadeManager
        self.__facade = FacadeManager()
        self.nome = nome
        self.dispositivo_id = dispositivo_id
        self.dispositivo_ip = dispositivo_ip
        self.dispositivo_port = dispositivo_port



    def notificar_users(self):
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
                                self.notificar_users()
                                break
                            else:
                                continue
            else:
                print(f"Erro ao coletar número: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")
