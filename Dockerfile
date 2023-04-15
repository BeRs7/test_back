FROM python:3.8.2-slim-buster

# Устанавливаем пакеты
RUN apt-get update && apt-get install -y nginx \
                                         redis-server \
                                         python3-dev \
                                         libgettextpo-dev \
                                         gcc \
                                         locales

# Устанавливаем локали для системы
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
     dpkg-reconfigure --frontend=noninteractive locales && \
     update-locale LANG=ru_RU.UTF-8

# Удаляем стандартный конфиг nginx
RUN rm -f /etc/nginx/sites-enabled/default

# Устанавливаем необходимые пакеты
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Копируем все файлы проекта
COPY . /app/

WORKDIR /app


# Запуск контейнера
ENTRYPOINT ["/bin/bash", "/app/_CI/entrypoint.sh"]
