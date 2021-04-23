import os


# database
host = os.environ['PSQL_HOST']
port = os.environ['PSQL_PORT']
db = os.environ['PSQL_DB']
user = os.environ['PSQL_USER']
pswd = os.environ['PSQL_PASSWORD']


class Config():
    SECRET_KEY = os.environ['SECRET_KEY']

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pswd}@{host}:{port}/{db}'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    OAUTHLIB_INSECURE_TRANSPORT = True


class TestingConfig(Config):
    TEMPLATES_AUTO_RELOAD = True
    OAUTHLIB_INSECURE_TRANSPORT = True

    TESTING = True
    WTF_CSRF_ENABLED = False
