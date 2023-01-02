FROM python:3.8.5-alpine

# Install dependencies
RUN apk add --no-cache mariadb-connector-c-dev
RUN apk update && apk add python3 python3-dev mariadb-dev build-base musl-dev gcc g++ tzdata && pip3 install mysqlclient && apk del python3-dev mariadb-dev
RUN apk add --no-cache freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    bash \
    dcron

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apk add netcat-openbsd git
RUN pip3 install django-mysql django-postgresql gunicorn gevent


# Copy code
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN /usr/bin/crontab /app/crontab

EXPOSE 80

CMD ["bash", "/app/docker/start.sh"]