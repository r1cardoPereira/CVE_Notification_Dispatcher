import os
import requests
import structlog

# Configurando o structlog
structlog.configure(processors=[structlog.processors.JSONRenderer()])
logging = structlog.get_logger()

api_key = os.getenv("API_NIST_KEY")  # Substitua com a sua própria API key
url = 'https://services.nvd.nist.gov/rest/json/cpes/2.0'  # URL base da API

# Configurando os headers para incluir a API key
headers = {'api_key': api_key}

# Fazendo uma solicitação GET para a API
response = requests.get(url, headers=headers)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # A resposta está em formato JSON
    data = response.json()

    # Iterando sobre os resultados e registrando os logs
    for entry in data:
        cpeNameId = str(entry['cpeNameId'])
        created = str(entry['created'])
        lastModified = str(entry['lastModified'])
        titles = str(entry['titles'])
        refs = str(entry['refs'])

        logging.info(
            "CPE Info",
            cpeNameId=cpeNameId,
            created=created,
            lastModified=lastModified,
            titles=titles,
            refs=refs
        )
else:
    logging.error(f'Erro na solicitação. Código de status: {response.status_code}')
