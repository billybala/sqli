import sqlite3
from pathlib import Path

# RUTAS
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = (BASE_DIR / "app.db").resolve()

# Función encargada de conectarse a la base de datos
def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Función que crea la base de datos, la tabla de usuarios
# y datos de prueba si no existen
def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)

        conn.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)", ("admin", "admin123", "admin"))
        conn.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES(?,?,?)", ("user", "user123", "user"))

        conn.commit()