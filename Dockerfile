# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Definir diretório de trabalho no contêiner
WORKDIR /app

# Copiar arquivos do projeto para o diretório de trabalho
COPY . .

# Instalar dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expôr a porta que o app usa
EXPOSE 8080

# Comando para iniciar o app
CMD ["python", "app.py"]
