import os
from urllib.parse import quote_plus


def build_sql_server_query_params() -> str:
    params = {
        "driver": os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server"),
    }

    db_encrypt = os.getenv("DB_ENCRYPT")
    db_trust_server_certificate = os.getenv("DB_TRUST_SERVER_CERTIFICATE")
    db_mars = os.getenv("DB_MARS_CONNECTION")

    if db_encrypt:
        params["Encrypt"] = db_encrypt
    if db_trust_server_certificate:
        params["TrustServerCertificate"] = db_trust_server_certificate
    if db_mars:
        params["MARS_Connection"] = db_mars

    return "&".join(
        f"{key}={quote_plus(str(value))}"
        for key, value in params.items()
    )


def build_sql_server_uri() -> str:
    db_user = os.getenv("DB_USER", "sa")
    db_password = quote_plus(os.getenv("DB_PASSWORD", "YourStrong@Passw0rd"))
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME", "facturacion_db")
    query_params = build_sql_server_query_params()
    db_server = f"{db_host}:{db_port}" if db_port else db_host

    return (
        f"mssql+pyodbc://{db_user}:{db_password}@{db_server}/{db_name}"
        f"?{query_params}"
    )


def build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    return build_sql_server_uri()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = build_sql_server_uri()


class ProductionConfig(BaseConfig):
    pass


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
