# tallerdia2

Backend Web API con FastAPI que implementa autenticación JWT.

## Estructura

- `backend/`: aplicación FastAPI
- `backend/Dockerfile`: imagen de la API
- `docker-compose.yml`: despliegue con Docker Compose

## Requisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- Docker y Docker Compose (opcional, para despliegue en contenedores)

## Ejecución local con Poetry

1. Instalar dependencias:

   ```bash
   cd backend
   poetry install
   ```

2. Ejecutar la API:

   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Endpoints

### 1) Obtener token

- **URL**: `POST /token`
- **Body**:

  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

- **Respuesta (200)**:

  ```json
  {
    "access_token": "<jwt>",
    "refresh_token": "<jwt>",
    "token_type": "bearer",
    "expires_in": 300
  }
  ```

El `access_token` expira en **300 segundos**.

### 2) Refrescar token

- **URL**: `POST /token/refresh`
- **Body**:

  ```json
  {
    "refresh_token": "<jwt>"
  }
  ```

- **Respuesta (200)**:

  ```json
  {
    "access_token": "<jwt>",
    "token_type": "bearer",
    "expires_in": 300
  }
  ```

## Variables de entorno

- `JWT_SECRET_KEY`: clave secreta para firmar JWT (default: `change-this-secret-in-production`)
- `JWT_ALGORITHM`: algoritmo JWT (default: `HS256`)

## Despliegue con Docker

Desde la raíz del proyecto:

```bash
docker compose up --build
```

La API quedará disponible en `http://localhost:8000`.
