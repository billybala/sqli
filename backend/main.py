from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel

from .db import get_conn, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[APP] Starting up - init_db()")
    init_db() # Inicialización de la base de datos al iniciar la aplicación
    yield
    print("[APP] Shutting down")

# Genera una aplicación básica con FastAPI
app = FastAPI(title="SQL Injection (SQLite + FastAPI)", lifespan=lifespan)

# Middleware que evita errores de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginBody(BaseModel):
    username: str
    password: str


# Endpoint vulnerable
@app.post("/login-vuln")
def login_vuln(body: LoginBody):
    """
    VULNERABLE: construye SQL concatenando strings.
    Permite bypass con payload tipo: ' OR '1'='1
    """

    username = body.username
    password = body.password

    query = (
        "SELECT id, username, role FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )

    try:
        with get_conn() as conn:
            row = conn.execute(query).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    if not row:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"ok": True, "user": dict(row), "note": "Sesión iniciada via endpoint VULNERABLE"}

# Endpoint seguro
@app.post("/login-safe")
def login_safe(body: LoginBody):
    """
    MITIGADO: consulta parametrizada.
    La SQLi no funciona.
    """

    username = body.username
    password = body.password

    query = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
    
    with get_conn() as conn:
        row = conn.execute(query, (username, password)).fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {"ok": True, "user": dict(row), "note": "Sesión iniciada via endpoint SEGURO"}