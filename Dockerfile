# 1 definimos la imagen base: un sistema linux con python 3.9 preisntalado
# especificamos -slim para una version ligera donde la seguridad y rapidez so idelaes
FROM python:3.9-slim

# 2 definimos el directorio de trabajo dentro del cotenedor 
# es como hacer mkdir /app && cd/app todo lo que se haga ocurrira aca
RUN apt-get update && apt-get install -y \
    iptables \
    sudo \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3 copia elarchivo del script desde el servidor aws hacia la carpeta /app del contenedor
# usamos el nombre exacto centinela.py para seguir el principio de minimo privilegio "solo copiar lo necesario"

COPY . .

# 4 ejecuta un comando en la construccion de la imagen
# aca instalamos la libreria requests, es necesaria para que el bot pueda enviar alertas a telegram

RUN pip install requests psycopg2-binary

# 5 definde el comando que se ejecutara AUTOMATICAMENTE cuando el contenedor se encienda 
# a diferencia de RUN este no se ejecuta al consturir sino cuadno el proceso cobra vida

CMD ["python","centinela_3.0.py"]

