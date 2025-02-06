FROM python:3.9

WORKDIR /app

# Copiamos primero requirements.txt
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Luego copiamos el resto del código
COPY . .

EXPOSE 5000

CMD ["python", "inventory_api.py"]
