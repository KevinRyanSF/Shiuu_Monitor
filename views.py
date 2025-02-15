from django.http import JsonResponse
import requests

FLASK_SERVER_URL = "http://127.0.0.1:5000/number"

def obter_numero(request):
    try:
        response = requests.get(FLASK_SERVER_URL)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Falha ao obter número"}, status=response.status_code)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)