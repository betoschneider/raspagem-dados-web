FROM arm64v8/python:3.10.12

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y wget unzip chromium chromium-chromedriver

# Configurar o ambiente de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Configurar o WebDriver para usar Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Comando para rodar a aplicação
CMD ["python3", "main.py"]
