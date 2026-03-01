# Imagen base ligera de Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Exponer puerto 3000
EXPOSE 3000

# Ejecutar servidor FastAPI
CMD ["uvicorn", "Biblioteca_main:app", "--host", "0.0.0.0", "--port", "3000"]