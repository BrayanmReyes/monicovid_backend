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
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USER}:{PASSWORD}@{SERVER}/{DATABASE}'
    SQLALCHEMY_ECHO = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = 'super secret'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory"
    SQLALCHEMY_ECHO = False
