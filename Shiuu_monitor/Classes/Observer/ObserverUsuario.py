import smtplib
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Classes.Observer.ObserverAbstract import ObserverAbstract


class Usuario(ObserverAbstract):
    def __init__(self, nome, email, cargo, senha):
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.senha = senha
        from FacadeSingleton.FacadeSingletonManager import FacadeManager
        self.__facade = FacadeManager()

    def update(self, ambiente, **kwargs):
        # Configurações de envio de email
        destinatario = self.email
        if destinatario == "admin":
            return 0
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587
        EMAIL_REMETENTE = "shiuumonitor@gmail.com"
        EMAIL_SENHA = "lczy djgx smiw lbvo"

        try:
            # Criando o e-mail
            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = destinatario
            msg["Subject"] = f"Limite sonoro ultrapassado no ambiente {ambiente}"

            # Corpo do e-mail
            msg.attach(MIMEText(f"Shiuu Monitor informa: Limite sonoro ultrapassado no ambiente {ambiente}", "plain"))

            # Conectar ao servidor SMTP e enviar e-mail
            servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            servidor.starttls()  # Segurança
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
            servidor.quit()

            print(f"E-mail enviado para {destinatario} com sucesso!")

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")


    def cadastrar_usuario(self):
        usuario_data = {
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo,
            'senha': self.senha
        }
        self.__facade.db.insert("usuarios", usuario_data)
        user = self.__facade.db.fetch_one("usuarios", "email", self.email)
        if self.cargo == 0:
            print("Escolha os ambientes do usuário:")
            time.sleep(2)
            escolha = self.__facade.escolher_ambientes([])
            for i in escolha:
                data_rel_user_amb = {
                    'id_usuario': user['id'],
                    'id_ambiente': i,
                }
                self.__facade.db.insert("usuario_ambientes", data_rel_user_amb)

        else:
            all_ambientes = self.__facade.db.fetch_all("ambientes")
            if not all_ambientes:
                pass
            else:
                for i in all_ambientes:
                    data_rel_user_amb = {
                        'id_usuario': user['id'],
                        'id_ambiente': i['id'],
                    }
                    self.__facade.db.insert("usuario_ambientes", data_rel_user_amb)

    def deletar_usuario(self):
        confirma = input(f"Deseja deletar o Usuário: {self.nome}? [Y/N]").upper()
        if confirma == "Y":
            self.__facade.db.delete("usuarios", "email", self.email)
            print("Usuário deletado com sucesso!")
            return True
        else:
            return False

    def editar_nome_usuario(self):
        nome = input("Digite o novo nome: ")
        if nome == self.nome:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("usuarios", "nome", "email", nome, self.email)
            print("Valor alterado com sucesso!")

    def editar_cargo_usuario(self):
        cargo = int(input("Digite o novo cargo (0 ou 1): "))
        if cargo == self.cargo:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("usuarios", "cargo", "email", cargo, self.email)
            print("Valor alterado com sucesso!")

    def editar_senha_usuario(self):
        senha = self.__facade.solicitar_senha()
        senha = self.__facade.encriptar_senha(senha)
        if senha == self.senha:
            print("Valor igual ao atual, insira outro valor.")
        else:
            self.__facade.db.update("usuarios", "senha", "email", senha, self.email)
            print("Valor alterado com sucesso!")