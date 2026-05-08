from config.settings import build_sql_server_uri


def test_build_sql_server_uri_uses_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")

    assert build_sql_server_uri() == "sqlite:///test.db"


def test_build_sql_server_uri_builds_sql_server_connection(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DB_HOST", "192.168.1.10")
    monkeypatch.setenv("DB_NAME", "facturacion")
    monkeypatch.setenv("DB_USER", "sa")
    monkeypatch.setenv("DB_PASSWORD", "Password123!")
    monkeypatch.setenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    connection_uri = build_sql_server_uri()

    assert connection_uri.startswith("mssql+pyodbc://sa:Password123%21@192.168.1.10/facturacion")
    assert "driver=ODBC+Driver+17+for+SQL+Server" in connection_uri
