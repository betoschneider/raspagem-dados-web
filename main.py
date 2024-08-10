import requests
import pandas as pd
import sqlite3

# URL do site com a tabela
url = 'http://192.168.1.10:5216/'

#########################################
# Parte 1: Leitura dos dados página web #
#########################################

# Busca a maior data na API
# URL do endpoint
url = "http://192.168.1.10:5000/max"

# Fazendo a requisição GET
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Parseando a resposta JSON
    data = response.json()
    print(data['data'])
    if data['data'] == None:
        print('valor vazio')
else:
    print(f"Erro na requisição: {response.status_code}")


# Conectar ao banco de dados
conn = sqlite3.connect('/DATA/AppData/myspeed/data/storage.db')
cursor = conn.cursor()

# Nome da tabela que você deseja carregar
tabela1 = 'speedtests'
tabela2 = 'config'
data = data['data']

# Carregar o conteúdo da tabela em um DataFrame
df = pd.read_sql_query(f"""
    SELECT date(created) AS data
        ,time(created) AS hora 
        ,c.key AS server
        ,ping
        ,download
        ,upload
        ,type
    FROM {tabela1} t INNER JOIN {tabela2} c ON t.serverId = c.value
    WHERE error IS NULL AND date(created) >=  date(coalesce('{data}', '2024-08-01'))
    """, 
    conn
)

#########################################
#     Parte 2: Gravar na tabela bd      #
#########################################

# URL da API
api_url = 'http://192.168.1.10:5000/teste'

# Função para enviar dados para a API
def send_data_to_api(df, api_url):
    # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        # Preparar os dados para enviar
        data = {
            # 'data': row['data'].strftime('%Y-%m-%d'),  # Formato da data: '2024-07-30'
            # 'hora': row['hora'].strftime('%H:%M:%S'),  # Formato da hora: '17:37:00'
            'data': row['data'],
            'hora': row['hora'],
            'server': row['server'],
            'ping': row['ping'],
            'download': row['download'],
            'upload': row['upload'],
            'tipo': row['type']
        }
        
        # Enviar os dados via POST
        try:
            response = requests.post(api_url, json=data)
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
            print(f"Dados enviados com sucesso: {data}")
        except requests.RequestException as e:
            print(f"Erro ao enviar dados: {e}")

# Chamar a função para enviar dados para a API
send_data_to_api(df, api_url)
