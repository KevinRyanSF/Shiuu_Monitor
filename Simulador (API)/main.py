from flask import Flask, jsonify
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Classe Dispositivo
class Dispositivo:
    def __init__(self, id):
        self.id = id
        self.dado_gerado = None
        self.hora_envio = None

    def gerar_dado(self):
        self.dado_gerado = random.randint(0, 100)
        self.hora_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Instância do dispositivo
dispositivo = Dispositivo(id=1)  # ID do dispositivo
client_connected = False

# Função para gerar números aleatórios
def generate_random_number():
    global client_connected
    while True:
        if client_connected:
            dispositivo.gerar_dado()  # Gera um novo dado
            print(f"Dispositivo {dispositivo.id} enviou: {dispositivo.dado_gerado} às {dispositivo.hora_envio}")
        time.sleep(5)

# Rota para obter os dados do dispositivo
@app.route('/number', methods=['GET'])
def get_number():
    global client_connected
    client_connected = True
    return jsonify({
        "id": dispositivo.id,
        "dado_gerado": dispositivo.dado_gerado,
        "hora_envio": dispositivo.hora_envio
    })

# Inicia o servidor Flask
if __name__ == '__main__':
    threading.Thread(target=generate_random_number, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)