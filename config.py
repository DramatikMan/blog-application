import os


psql_db = os.environ['PSQL_DB']
psql_user = os.environ['PSQL_USER']
psql_pswd = os.environ['PSQL_PASSWORD']


class Config():
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f'postgresql://{psql_user}:{psql_pswd}@postgres:5432/{psql_db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']

    # recaptcha v2 keys
    RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

    # Google OAuth2
    GOOGLE_OAUTH_CLIENT_ID = os.environ['GOOGLE_OAUTH_CLIENT_ID']
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ['GOOGLE_OAUTH_CLIENT_SECRET']
    OAUTHLIB_RELAX_TOKEN_SCOPE = True

    # blog admin account credentials:
    ADMIN_NAME = os.environ['ADMIN_NAME']
    ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
    ADMIN_EMAIL = os.environ['ADMIN_EMAIL']


class ProdConfig(Config):
    pass


class DeveConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    OAUTHLIB_INSECURE_TRANSPORT = True


class TestConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    OAUTHLIB_INSECURE_TRANSPORT = True

    TESTING = True
    WTF_CSRF_ENABLED = False
