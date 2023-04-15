#!/bin/bash

# // Копируем файлы переменной окружения и конфиг nginx
cp -R /app/_CI/nginx/$ENVIRONMENT.conf /etc/nginx/conf.d/default.conf
cp -R /app/_CI/envs/$ENVIRONMENT.env   /app/.env

echo "
SECRET_KEY=$SECRET_KEY
DATABASE_URL=$DATABASE_URL
       " >> /app/.env

# // Экспортируем переменные окружения из файла
export $(egrep -v '^#' /app/.env | xargs)

# // Перезапускаем сервисы
service nginx restart
service redis-server start

# // Миграции и статика
cd /app/
python /app/manage.py migrate
python /app/manage.py collectstatic --no-input

celery --app=config worker -l info --logfile=/celery.log -Q emails -n emails_worker &
celery --app=config worker -l info --logfile=/celery.log -Q default -n default &
celery --app=config beat -l info --logfile=/celery_beat.log &

celery flower -A config --address=127.0.0.1 --port=5555 --url_prefix=flower &

uwsgi --ini uwsgi.ini
#gunicorn --timeout 60 --bind 0.0.0.0:8010 --chdir /app config.wsgi:application --workers=2
