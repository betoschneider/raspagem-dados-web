FROM arm64v8/python:3.10.12

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y wget unzip

# Baixar e instalar o Chrome (se disponível para ARM64) e o chromedriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver

# Configurar o ambiente de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["python3", "main.py"]
