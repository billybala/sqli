# SQL Injection con FastAPI + SQLite

Este proyecto demuestra una vulnerabilidad del tipo **SQL Injection (SQLi)** en un sistema de autenticación y su correspondiente mitigación utilizando **FastAPI** y **SQLite**.

El objetivo es mostrar cómo la contrucción insegura de consultas SQL mediante concatenación de strings permite el bypass de autenticación, y cómo el uso de consultas parametrizadas elimina la vulnerabilidad.

---

## 📌 Arquitectura del proyecto

- **Backend (FastAPI + SQLite)**  
  Expone dos endpoints:
  - `/login-vuln` → Endpoint vulnerable a SQL Injection
  - `/login-safe` → Endpoint corregido con sonsultas parametrizadas

- **Base de datos SQLite**
  - Tabla `users` con usuarios de prueba

- **Frontend (HTML + CSS + JavaScript)**
  - Interfaz visual para probar credenciales normales y payloads SQLi

---

## 📂 Estructura de carpetas

```
sqli/
│
├── backend/
│ ├── main.py
│ ├── db.py
│ ├── app.db
│ └── requirements.txt
│
├── frontend/
│ ├── index.html
│ ├── styles.css
│ └── script.js
│
└── README.md
```

---

## ⚙️ Requisitos

- Python
- Navegador web moderno

---

## 🚀 Puesta en marcha

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/billybala/sqli.git
cd sqli
```

### 2️⃣ Backend FastAPI (entorno virtual)

```bash
python -m venv .venv
.venv\Scripts\activate # SO Windows
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend disponible en `http://127.0.0.1:8000`.

### 3️⃣ Frontend (servidor estático)

```bash
cd frontend
python -m http.server 8080
```

Abrir en el navegador `http://127.0.0.1:8080`.

## 🧪 Pruebas de la vulnerabilidad SQLi

### 🔴 Endpoint vulnerable

```bash
POST /login-vuln
```

Payload de inyección clásico en el campo password:

```bash
' OR '1'='1
```

Este payload modifica la consulta SQL original y permite el bypass de autenticación.

Resultado esperado:

- Autenticación exitosa sin credenciales válidas.

### 🟢 Endpoint mitigado

```bash
POST /login-safe
```

Utiliza consulta parametrizadas:

```sql
SELECT * FROM users WHERE username = ? AND password = ?
```

Resultado esperado:

- El mismo payload SQLi no produce bypass y devuelve error 401.

### 🛡️ Medidas de mitigación implementadas

- Uso de consultas parametrizadas (prepared statements)

- Eliminación de concatenación dinámica de strings

- Inicialización segura de la base de datos

- Separación de lógica de base de datos y endpoints
