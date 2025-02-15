import sys
import subprocess

# Função para instalar um pacote usando pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Verifica se o módulo requests está instalado
try:
    import requests
except ImportError:
    print("Módulo 'requests' não encontrado. Instalando...")
    install("requests")
    import requests  # Tenta importar novamente após a instalação

from Classes.Observer.ObserverAmbiente import Ambiente

if __name__ == "__main__":
    # Verifica se todos os argumentos foram passados
    if len(sys.argv) != 5:
        print("Uso: python monitorar_ambiente.py <nome> <dispositivo_id> <dispositivo_ip> <dispositivo_port>")
        sys.exit(1)

    # Captura os argumentos
    nome = sys.argv[1]
    dispositivo_id = int(sys.argv[2])
    dispositivo_ip = sys.argv[3]
    dispositivo_port = int(sys.argv[4])

    # Cria uma instância da classe Ambiente
    ambiente = Ambiente(nome, dispositivo_id, dispositivo_ip, dispositivo_port)

    # Inicia o monitoramento
    ambiente.monitorar_ambiente_loop()