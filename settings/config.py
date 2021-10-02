class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    USER = "production"
    PASSWORD = "production"
    SERVER = "production"
    DATABASE = "production"
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{SERVER}/{DATABASE}'


class DevelopmentConfig(Config):
    USER = "root"
    PASSWORD = "pacheco98"
    SERVER = "localhost"
    DATABASE = "monicovid"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DATABASE}'
    SQLALCHEMY_ECHO = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = 'super secret'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = 'monicovid.no.reply@gmail.com'
    MAIL_USERNAME = 'monicovid.no.reply@gmail.com'
    MAIL_PASSWORD = 'bgzdagkdujcjxmag'
    SCHEDULER_API_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory"
    SQLALCHEMY_ECHO = False
