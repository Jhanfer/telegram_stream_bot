# Este Dockerfile es usado para desplegar un contenedor simple

# Se establece la versión de Python a utilizar
FROM python:3.11


# Creando un directorio de trabajo llamado "/app"
WORKDIR /app
# Compiar el contenido a "/app" dentro del contenedor 
COPY . .

# Creamos la variable donde se va a guardar el entorno virtual - Es recomendable cambiar el nombre del ".venv" a ".venv_[CUALQUIERCOSA]" para evitar confusiones o incompatibilidad
ENV VIRTUAL_ENV=/app/.venv_telegram_bot

# Añadir al "PATH" el entorno virtual que hemos creado antesz
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Ejecutar el comando de Python para crear el entorno virtual
RUN python3.11 -m venv $VIRTUAL_ENV

# Acrualizar pip
RUN pip install --upgrade pip

# Instalar los requerimientos sin caché
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r job_queue.txt
RUN pip install --no-cache-dir -r webhooks.txt

CMD ["python", "/app/code/telegram_bot.py"]
HEALTHCHECK --interval=5m --timeout=3s --start-period=5s CMD curl -f http://localhost:8080/health || exit 1

