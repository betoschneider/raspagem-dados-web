import requests
import sqlite3
import pandas as pd


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
    WHERE error IS NULL AND date(created) >= date(coalesce(data, '2021-08-01'))
    """, 
    conn
)

print(df)
