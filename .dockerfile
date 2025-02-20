# Usa una imagen base de Python
FROM python:3.x

# Establece el directorio de trabajo
WORKDIR /klipfolio_app

# Copia los archivos de requisitos
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
