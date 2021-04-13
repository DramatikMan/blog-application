pipenv install gunicorn

echo $'
workers=4
bind="0.0.0.0:8080"
wsgi_app="blog_application:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
gunicorn
