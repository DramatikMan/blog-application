evs=(
	FLASK_APP
	FLASK_ENV
	SECRET_KEY
	PSQL_HOST
	PSQL_PORT
	PSQL_DB
	PSQL_USER
	PSQL_PASSWORD
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
		echo -e "\e[93mEnvironmental variable \e[1m$variable\e[21m is not defined or is empty.\e[0m"
		((undef++))
	fi
done
if [[ $undef -gt 0 ]]; then exit 1; fi

pipenv install gunicorn

echo $'
workers=4
bind="unix:/tmp/blog_app/gunicorn.sock"
wsgi_app="blog_app:create_app()"' > gunicorn.conf.py

source .venv/bin/activate
gunicorn
