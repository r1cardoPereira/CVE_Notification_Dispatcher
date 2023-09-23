from datetime import datetime, timedelta
import requests
import json
import os
import structlog


logging = structlog.get_logger()
api_key = os.getenv("API_NIST_KEY")  # Substitua com a sua própria API key  
base_url = 'https://services.nvd.nist.gov/rest/json/cpes/2.0/'

# Obter a data atual
data_atual = datetime.now()

# Lista de intervalos de dias que você deseja consultar
intervalos = [1, 7, 15, 30]

for intervalo in intervalos:
    # Calcular as datas de início e fim
    data_fim = data_atual.isoformat()  # Data fim é sempre a data atual
    data_inicio = (data_atual - timedelta(days=intervalo)).isoformat()
    logging.info(f'Consultando dados do NIST para o intervalo de {intervalo} dias')
    logging.info(f'Data de início: {data_inicio}')
    logging.info(f'Data de fim: {data_fim}')

    # Montar a URL com os parâmetros de data
    url = f'{base_url}?lastModStartDate={data_inicio}&lastModEndDate={data_fim}'
    logging.info(f'URL: {url}')

    # Fazer a requisição à API
    headers = {'api_key': api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Agora você pode fazer o que precisar com os dados

        # Por exemplo, salvar em um arquivo JSON
        with open(f'dados_nist_{intervalo}_dias.json', 'w') as file:
            json.dump(data, file)

    else:
        print(f'Erro na solicitação. Código de status: {response.status_code}')
logging.info('Fim do script')