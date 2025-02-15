import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Classes.Observer.ObserverAbstract import Observer


class Usuario(Observer):
    def __init__(self, nome, email, cargo, senha):
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.senha = senha

    def update(self, ambiente, **kwargs):
        # Configurações de envio de email
        destinatario = self.email
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

