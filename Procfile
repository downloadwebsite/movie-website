web: sh -c "python manage.py collectstatic --noinput --clear && python manage.py migrate --noinput && gunicorn moviedl.wsgi --bind 0.0.0.0:$PORT"
