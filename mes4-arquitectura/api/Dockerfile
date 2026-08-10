FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY mes4-arquitectura/api/requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY mes4-arquitectura/api/ ./api/
COPY src/ ./src/

WORKDIR /app/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]