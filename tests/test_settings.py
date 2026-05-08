from config.settings import (
    build_database_uri,
    build_sql_server_query_params,
    build_sql_server_uri,
)


def test_build_database_uri_uses_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "mssql+pyodbc://user:pass@host/db")

    assert build_database_uri() == "mssql+pyodbc://user:pass@host/db"


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
