# La receta del contenedor. Cada línea es un paso que Docker ejecuta al construir la imagen.

# 1. Partir de una imagen que ya trae Python 3.12 instalado
FROM python:3.12-slim

# 2. Trabajar dentro de la carpeta /app del contenedor
WORKDIR /app

# 3. Instalar las librerías primero: si solo cambia el código, Docker reutiliza este paso
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el programa
COPY app.py .

# 5. Valor por defecto de la versión; la definición de tarea lo puede cambiar
ENV VERSION=v1

# 6. El puerto por el que escucha la aplicación
EXPOSE 8080

# 7. El comando que se ejecuta al arrancar el contenedor
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
