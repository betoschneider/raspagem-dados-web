FROM python:3.10.12

# Configurar o ambiente de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["python3", "main.py"]
