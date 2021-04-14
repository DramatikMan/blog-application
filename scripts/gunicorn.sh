pipenv install gunicorn

echo $'
workers=4
bind="unix:/tmp/blog_app/gunicorn.sock"
wsgi_app="blog_app:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
gunicorn
