web: gunicorn savings.wsgi --log-file -
python manage.py collectstatic --noinput
manage.py makemigations
manage.py migrate