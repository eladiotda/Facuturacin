import os
from urllib.parse import quote_plus


def build_sql_server_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_user = os.getenv("DB_USER", "sa")
    db_password = quote_plus(os.getenv("DB_PASSWORD", "YourStrong@Passw0rd"))
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_name = os.getenv("DB_NAME", "facturacion_db")
    db_driver = quote_plus(os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"))

    return (
        f"mssql+pyodbc://{db_user}:{db_password}@{db_host}/{db_name}"
        f"?driver={db_driver}"
    )


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = build_sql_server_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    pass


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
