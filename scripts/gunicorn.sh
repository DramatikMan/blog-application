pipenv install gunicorn

echo $'
workers=4
bind="0.0.0.0:8080"
wsgi_app="blog_app:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
gunicorn
