# Project Repository

A simple notes application backend (Flask) providing JWT-based auth and CRUD for user-owned notes.

## Backend (fastapi_backend)

- Framework: Flask + flask-smorest (OpenAPI docs at /docs)
- Auth: JWT (PyJWT)
- Database: SQLite by default (DATABASE_URL env can point to PostgreSQL)
- Endpoints:
  - POST /register
  - POST /login
  - GET /notes
  - POST /notes
  - GET /notes/{id}
  - PUT /notes/{id}
  - PATCH /notes/{id}
  - DELETE /notes/{id}

### Environment variables (configure via .env; do not commit secrets)
- FLASK_SECRET_KEY: Secret for Flask session (not used for auth)
- JWT_SECRET_KEY: Secret key to sign JWTs
- JWT_ALGORITHM: HS256 (default)
- JWT_ACCESS_TOKEN_EXPIRES_MIN: Minutes until token expiry (default 60)
- DATABASE_URL: SQLAlchemy URL. Examples:
  - sqlite:///notes.db
  - postgresql+psycopg2://user:pass@host:5432/dbname
- CORS_ORIGINS: Allowed origins for CORS (default "*")

### Install and run
```bash
pip install -r fastapi_backend/requirements.txt
cd fastapi_backend
python run.py
```

Open API docs at: http://localhost:5000/docs

### Security notes
- Passwords are hashed using Werkzeug security helpers.
- JWT tokens are Bearer tokens. Include header: Authorization: Bearer <token>.
- Ensure strong secrets are set in production.
