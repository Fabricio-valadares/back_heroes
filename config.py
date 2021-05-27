from os import getenv

class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv("SECRET_KEY")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")

class ProductionConfig(Config):
    ...

class TestConfig(Config):
    ...

selector_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig
}
