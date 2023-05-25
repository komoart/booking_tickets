#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Postgres еще не запущен..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Postgres успешно запущен."
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.local', 'admin')"
python3 manage.py loaddata movies/fixtures/movies.json

exec "$@"
