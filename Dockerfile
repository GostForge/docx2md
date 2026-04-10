FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn python-multipart

COPY . .

EXPOSE 8082
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8082"]
