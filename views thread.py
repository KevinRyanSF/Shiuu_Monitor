import logging
import requests
import time
import threading
from django.http import JsonResponse
from django.shortcuts import render
from ambientes.models import Ambiente

logger = logging.getLogger(__name__)

ultimo_numero = None


def coletar_numeros_em_segundo_plano():
    ambiente = Ambiente.objects.get(id=1)

    if not ambiente:
        logger.error("Ambiente não encontrado!")
        return

    dispositivo_ip = ambiente.dispositivo_ip
    dispositivo_port = ambiente.dispostivo_port
    FLASK_SERVER_URL = f"http://{dispositivo_ip}:{dispositivo_port}/number"
    print(FLASK_SERVER_URL)

    global ultimo_numero
    while True:
        try:
            response = requests.get(FLASK_SERVER_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                ultimo_numero = data['dado_gerado']
                id_disposito = data['id']
                hora = data['hora_envio']
                logger.info(f"Id: {id_disposito}, Número coletado: {ultimo_numero}, hora: {hora}")
                print(f"Id: {id_disposito}, Número coletado: {ultimo_numero}, hora: {hora}")

                for nivel in ambiente.niveis.all():
                    if ultimo_numero > nivel.nivel_DB:
                        logger.warning(f"Alerta para o nível {nivel.nome}: {nivel.alerta}")

            else:
                logger.error(f"Erro ao coletar número: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Erro na requisição: {e}")

        time.sleep(5)


thread = threading.Thread(target=coletar_numeros_em_segundo_plano, daemon=True)
thread.start()

def obter_numero(request):
    global ultimo_numero
    if ultimo_numero is not None:
        return JsonResponse({"random_number": ultimo_numero})
    else:
        return JsonResponse({"error": "Nenhum número coletado ainda"}, status=500)













def homepage(request):
    #return HttpResponse("Homepage")
    return render(request, 'homepage.html')
