FROM python:3.9-slim-buster

WORKDIR /app

# Instalar dependências de sistema e fontes
RUN apt-get update && \
    apt-get install -y libjpeg-dev zlib1g-dev gcc libfreetype6 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
