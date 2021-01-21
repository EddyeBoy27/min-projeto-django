web: gunicorn --pythonpath estoque_project estoque_project.wsgi --log-file -
release: --pythonpath estoque_project python manage.py makemigrations
release: --pythonpath estoque_project python manage.py migrate