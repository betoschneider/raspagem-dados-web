from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import pandas as pd

# URL do site com a tabela
url = 'http://192.168.1.10:5216/'

#########################################
# Parte 1: Leitura dos dados página web #
#########################################

# Configuração do Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executar em modo headless, sem interface gráfica
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acessando a página
driver.get(url)

# Aguardar o carregamento do conteúdo dinâmico (ajuste o tempo conforme necessário)
time.sleep(5)

# Obter o conteúdo da página
html_content = driver.page_source

# Fechar o navegador
driver.quit()

# Usar BeautifulSoup para parsear o HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar elementos com base na nova estrutura HTML
speedtest_areas = soup.find_all('div', class_='speedtest')

#########################################
#     Parte 2: Armazenar em lista       #
#########################################

# Definir a data atual
current_date = datetime.now().strftime('%d/%m/%Y')

# Lista para armazenar os registros
registros = []

# Iterar sobre os elementos e extrair os dados
for area in speedtest_areas:
    date = area.find('h2', class_='date-text')
    if date:
        date = date.get_text().replace('Às ', '')
    else:
        date = 'Data não encontrada'

    rows = area.find_all('div', class_='speedtest-row')

    taxa = {'0': 'ping', '1': 'download', '2': 'upload'}
    n = 0
    for row in rows:
        speed = row.find('h2', class_='speedtest-text')
        if speed:
            speed = speed.get_text()
        else:
            speed = 'Velocidade não encontrada'
        # Adicionar os dados à lista de registros
        registros.append([current_date, date, speed, taxa[str(n)]])
        n += 1

#########################################
#   Parte 3: Transformação dos dados    #
#########################################

# Transformando as linhas em colunas
df = pd.DataFrame(registros, columns=['data', 'hora', 'valor', 'taxa'])

# Converter tipo de dado das colunas
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M').dt.time
df['valor'] = df['valor'].astype(float)

# Pivotar o DataFrame
df = df.pivot_table(index=['data', 'hora'], columns='taxa', values='valor', aggfunc='first').reset_index()

# Ajustar os nomes das colunas
df.columns.name = None
df = df.rename_axis(None, axis=1)

# Reordenar as colunas
df = df[['data', 'hora', 'ping', 'download', 'upload']]

#########################################
#     Parte 4: Gravar na tabela bd      #
#########################################

# URL da API
api_url = 'http://192.168.1.10:5000/teste'

# Função para enviar dados para a API
def send_data_to_api(df, api_url):
    # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        # Preparar os dados para enviar
        data = {
            'data': row['data'].strftime('%Y-%m-%d'),  # Formato da data: '2024-07-30'
            'hora': row['hora'].strftime('%H:%M:%S'),  # Formato da hora: '17:37:00'
            'ping': row['ping'],
            'download': row['download'],
            'upload': row['upload']
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
