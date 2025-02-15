from flask import Flask, jsonify
import random
import threading
import time

app = Flask(__name__)
current_number = 0
client_connected = False

def generate_random_number():
    global current_number, client_connected
    while True:
        if client_connected:
            current_number = random.randint(0, 100)
            print(f"Generated number: {current_number}")
        time.sleep(5)

@app.route('/coleta', methods=['GET'])
def get_number():
    global client_connected
    client_connected = True
    return jsonify({"id": 1, "dado_gerado": current_number})

if __name__ == '__main__':
    threading.Thread(target=generate_random_number, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)