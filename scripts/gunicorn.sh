pipenv install gunicorn

echo $'
pythonpath="/project"
workers=4
bind="127.0.0.1:8080"
wsgi_app="blog_application:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
flask db_clear && flask db_fill
gunicorn
