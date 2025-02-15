import requests

FLASK_SERVER_URL = "http://127.0.0.1:5000/number"  # Substitua pelo IP correto se necessário

def coletar_numero():
    try:
        response = requests.get(FLASK_SERVER_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"Número coletado: {data['random_number']}")
            return data['random_number']
        else:
            print(f"Erro ao coletar número: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")

if __name__ == "__main__":
    coletar_numero()