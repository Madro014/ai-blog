#Dockerfile
 
# 1. La Imagen Base: Empezamos con una imagen oficial de Python ligera.
FROM python:3.11-slim
 
# 2. El Directorio de Trabajo: Creamos una carpeta dentro del contenedor.
WORKDIR /app
 
# 3. Instalación de Dependencias:
# Primero copiamos solo el archivo de requisitos para aprovechar el caché de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# 4. Copia del Código: Copiamos el resto de nuestro código (main.py, etc.)
COPY . .
 
# 5. El Comando de Ejecución:
# Le decimos a Docker cómo iniciar la API.
# Usamos 0.0.0.0 para que sea accesible desde fuera del contenedor.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]