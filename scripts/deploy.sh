evs=(
	FLASK_APP
	FLASK_ENV
	SECRET_KEY
	POSTGRES_USER
	POSTGRES_PASSWORD
	POSTGRES_HOST
	POSTGRES_PORT
	POSTGRES_DB
	RECAPTCHA_PUBLIC_KEY
	RECAPTCHA_PRIVATE_KEY
	GOOGLE_OAUTH_CLIENT_ID
	GOOGLE_OAUTH_CLIENT_SECRET
	ADMIN_NAME
	ADMIN_PASSWORD
	ADMIN_EMAIL
)
for variable in "${evs[@]}"; do
	if [[ -z ${!variable+x} ]] || [[ -z ${!variable} ]] ; then
		echo -e "\e[93mEnvironmental variable \e[1m$variable\e[21m is undefined or empty.\e[0m"
		((undef++))
	fi
done
if [[ $undef -gt 0 ]]; then exit 1; fi

pipenv install gunicorn

echo $'
workers=4
bind="0.0.0.0:8000"
wsgi_app="blog_app:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
gunicorn
