# 🛠️ Local Setup, Environment & Automated Testing

This document details local development setup, environment variables configuration, Docker container orchestration, and automated testing execution for **TeamBoard**.

---

## ⚙️ Environment Variables Configuration

The application uses `python-dotenv` to manage runtime configuration. Copy [.env.example](.env.example) to `.env`:

| Variable Name | Default Value | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Django secret key for session signing and token encryption |
| `DEBUG` | `True` | Debug flag (`True` for local development, `False` for production) |
| `ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hostnames |
| `USE_SQLITE` | `False` | Set to `True` for fast in-memory SQLite (used during testing) |
| `DB_ENGINE` | `django.db.backends.postgresql` | Database backend engine |
| `DB_NAME` | `teamboard_db` | PostgreSQL database name |
| `DB_USER` | `teamboard_user` | PostgreSQL database user |
| `DB_PASSWORD` | `teamboard_pass` | PostgreSQL database password |
| `DB_HOST` | `localhost` | PostgreSQL host server |
| `DB_PORT` | `5432` | PostgreSQL host port |

---

## 🛠️ Local Setup & Quick Start

### Prerequisites
- **Python 3.11+** installed
- **Docker & Docker Compose** installed
- **Git** installed

### Step-by-step Execution

1. **Clone repository:**
   ```bash
   git clone https://github.com/Shubhankart101/TeamBoard.git
   cd TeamBoard
   ```

2. **Setup environment configuration:**
   ```bash
   cp .env.example .env
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   # Windows PowerShell
   $env:USE_SQLITE="True"
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed Knowledge Base entries:**
   ```bash
   python manage.py seed_kb
   ```

6. **Start local development server:**
   ```bash
   python manage.py runserver
   ```
   Interactive Swagger UI is available at `http://127.0.0.1:8000/api/docs/`.

---

## 🐳 Docker Containerization

Run Django API and PostgreSQL 15 via Docker Compose using [docker-compose.yml](docker-compose.yml) and [Dockerfile](Dockerfile):

```bash
# Start container services in background
docker compose up -d

# Execute database migrations inside web container
docker compose exec web python manage.py migrate

# Seed KB entries inside web container
docker compose exec web python manage.py seed_kb
```

---

## 🧪 Automated Testing Framework

TeamBoard uses `pytest`, `pytest-django`, and `pytest-cov` configured via [pytest.ini](pytest.ini).

### Running Tests locally

```bash
# Execute Pytest suite with coverage report
$env:USE_SQLITE="True"
pytest
```

### Coverage Report Breakdown (97% Total)
```
Name                                Stmts   Miss  Cover
-------------------------------------------------------
api/admin.py                           17      0   100%
api/apps.py                             6      0   100%
api/models.py                          33      0   100%
api/permissions.py                      5      0   100%
api/serializers.py                     36      0   100%
api/signals.py                          9      0   100%
api/tests.py                          150      0   100%
api/urls.py                             4      0   100%
api/views.py                           78      0   100%
-------------------------------------------------------
TOTAL                                 357     12    97%
```
