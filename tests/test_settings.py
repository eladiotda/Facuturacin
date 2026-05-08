from config.settings import (
    build_database_uri,
    build_sql_server_query_params,
    build_sql_server_uri,
    build_sqlite_uri,
)


def test_build_database_uri_uses_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")

    assert build_database_uri() == "sqlite:///test.db"


def test_build_sqlite_uri_uses_sqlite_database_uri(monkeypatch):
    monkeypatch.setenv("SQLITE_DATABASE_URI", "sqlite:///mi_app.db")

    assert build_sqlite_uri() == "sqlite:///mi_app.db"


def test_build_sql_server_uri_builds_sql_server_connection(monkeypatch):
    monkeypatch.setenv("DB_HOST", "192.168.1.10")
    monkeypatch.setenv("DB_PORT", "1433")
    monkeypatch.setenv("DB_NAME", "facturacion")
    monkeypatch.setenv("DB_USER", "sa")
    monkeypatch.setenv("DB_PASSWORD", "Password123!")
    monkeypatch.setenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_uri = build_sql_server_uri()

    assert connection_uri.startswith("mssql+pyodbc://sa:Password123%21@192.168.1.10:1433/facturacion")
    assert "driver=ODBC+Driver+17+for+SQL+Server" in connection_uri


def test_build_database_uri_supports_sqlite_engine(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_ENGINE", "sqlite")
    monkeypatch.setenv("SQLITE_DATABASE_URI", "sqlite:///dev.db")

    assert build_database_uri() == "sqlite:///dev.db"


def test_build_database_uri_supports_sqlserver_engine(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_ENGINE", "sqlserver")
    monkeypatch.setenv("DB_HOST", "192.168.1.10")
    monkeypatch.setenv("DB_PORT", "1433")
    monkeypatch.setenv("DB_NAME", "facturacion")
    monkeypatch.setenv("DB_USER", "sa")
    monkeypatch.setenv("DB_PASSWORD", "Password123!")
    monkeypatch.setenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_uri = build_database_uri()

    assert connection_uri.startswith("mssql+pyodbc://sa:Password123%21@192.168.1.10:1433/facturacion")


def test_build_sql_server_query_params_supports_encrypt_options(monkeypatch):
    monkeypatch.setenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    monkeypatch.setenv("DB_ENCRYPT", "yes")
    monkeypatch.setenv("DB_TRUST_SERVER_CERTIFICATE", "yes")
    monkeypatch.setenv("DB_MARS_CONNECTION", "yes")

    query_params = build_sql_server_query_params()

    assert "driver=ODBC+Driver+17+for+SQL+Server" in query_params
    assert "Encrypt=yes" in query_params
    assert "TrustServerCertificate=yes" in query_params
    assert "MARS_Connection=yes" in query_params
