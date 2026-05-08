from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
server = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "")
user = os.getenv("DB_USER", "")
pwd = os.getenv("DB_PASSWORD", "")
db = os.getenv("DB_NAME", "")

server_addr = f"{server}:{port}" if port else server
if user and pwd:
    conn_str = f"DRIVER={{{driver}}};SERVER={server_addr};UID={user};PWD={pwd};"
else:
    conn_str = f"DRIVER={{{driver}}};SERVER={server_addr};Trusted_Connection=yes;"

print("Usando cadena ODBC:", conn_str)
try:
    conn = pyodbc.connect(conn_str, timeout=5)
    print("CONECTADO al servidor")
    if db:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = ?", (db,))
        existe = cursor.fetchone()[0] > 0
        print(f"La base de datos '{db}' existe: {existe}")
        cursor.close()
    conn.close()
except Exception as e:
    print("ERROR al conectar:", e)
