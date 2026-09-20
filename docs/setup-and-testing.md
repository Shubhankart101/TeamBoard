# 🛠️ Local Setup, Environment & Automated Testing

This document details local development environment configuration, environment variables management, Docker container orchestration, database seeding commands, and automated test suite execution for **TeamBoard**.

---

## ⚙️ Environment Variables Configuration

The application uses `python-dotenv` to manage secrets and environment flags. Copy [.env.example](.env.example) to `.env` in the root directory:

| Variable Name | Type | Default Value | Description & Production Guidance |
|---|---|---|---|
| `SECRET_KEY` | String | `django-insecure-...` | Cryptographic signing key for sessions & JWT tokens. Set a random 50+ char secret in production. |
| `DEBUG` | Boolean | `True` | Debug mode. Must be set to `False` in production to prevent technical stack trace exposure. |
| `ALLOWED_HOSTS` | List | `*` | Comma-separated domain names or IP addresses allowed to serve the Django app. |
| `USE_SQLITE` | Boolean | `False` | When set to `True` or `1`, overrides PostgreSQL configuration with an in-memory SQLite database (used during local Pytest runs). |
| `DB_ENGINE` | String | `django.db.backends.postgresql` | Django database backend driver. |
| `DB_NAME` | String | `teamboard_db` | Name of the target PostgreSQL database. |
| `DB_USER` | String | `teamboard_user` | User account for PostgreSQL database access. |
| `DB_PASSWORD` | String | `teamboard_pass` | Password for PostgreSQL database user. |
| `DB_HOST` | String | `localhost` | Host address of PostgreSQL server (`db` inside Docker Compose). |
| `DB_PORT` | Integer | `5432` | TCP port for PostgreSQL server connection. |

---

## 🛠️ Step-by-Step Local Setup Guide

### 1. Prerequisites
- **Python:** Version 3.11 or higher
- **Docker & Docker Compose:** Installed and running
- **Git:** Installed

### 2. Repository Cloning & Virtual Environment Setup

```bash
# Clone the repository
git clone https://github.com/Shubhankart101/TeamBoard.git
cd TeamBoard

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt
```

### 3. Database Migration & Knowledge Base Seeding

```bash
# Create and apply database schema migrations
# Note: Set USE_SQLITE=True if testing locally without PostgreSQL running
$env:USE_SQLITE="True"   # Windows PowerShell
# export USE_SQLITE="True" # Linux / macOS

python manage.py makemigrations
python manage.py migrate

# Seed pre-populated Knowledge Base (KBEntry) records
python manage.py seed_kb
```

### 4. Running Development Server

```bash
python manage.py runserver
```

Once started, access the application endpoints at:
- **API Base URL:** `http://127.0.0.1:8000/api/`
- **Interactive Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **ReDoc UI:** `http://127.0.0.1:8000/api/redoc/`
- **Django Admin Console:** `http://127.0.0.1:8000/admin/`

---

## 🐳 Docker Containerization

TeamBoard provides a containerized setup for local development and cloud production deployments via [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml).

### Multi-Container Stack Setup
- **`web` Service:** Python 3.11 slim container running Gunicorn / Django `runserver` on port 8000.
- **`db` Service:** Official `postgres:15-alpine` container listening on port 5432 with persistent volume storage (`postgres_data`).

```bash
# Start full container stack in detached mode
docker compose up -d --build

# Run migrations inside the web container
docker compose exec web python manage.py migrate

# Seed Knowledge Base entries inside the web container
docker compose exec web python manage.py seed_kb

# Check logs of running services
docker compose logs -f web

# Stop container stack
docker compose down
```

---

## 🧪 Automated Testing Framework

TeamBoard includes a comprehensive automated test suite built with `pytest`, `pytest-django`, and `pytest-cov`.

### Test Suite Organization (`api/tests.py`)
- **Unit Tests:** Model string representations, custom permission evaluation (`IsAdminUser`), signal receiver execution (`create_company_profile`).
- **Integration Tests:** Public endpoint auth flow (`register_view`, `login_view`), JWT access token validation, duplicate username handling, missing payload errors.
- **Transactional Tests:** `query_kb_view` ORM filtering (`Q` objects), atomic transaction integrity, `QueryLog` generation (both positive and 0-result searches).
- **Security Tests:** Permission denial (`403 Forbidden`) when client tokens attempt access to `/api/admin/usage-summary/`, `401 Unauthorized` for missing tokens, Swagger/ReDoc schema endpoints availability.

### Executing Pytest Locally

```bash
# Set USE_SQLITE for ultra-fast in-memory test execution
$env:USE_SQLITE="True"

# Execute pytest with code coverage output
pytest
```

### Statement Coverage Report Matrix (97% Total Coverage)

```
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
api\__init__.py                           0      0   100%
api\admin.py                             17      0   100%
api\apps.py                               6      0   100%
api\management\__init__.py                0      0   100%
api\management\commands\__init__.py       0      0   100%
api\management\commands\seed_kb.py       12     12     0%   (Management CLI script)
api\migrations\0001_initial.py            7      0   100%
api\migrations\__init__.py                0      0   100%
api\models.py                            33      0   100%
api\permissions.py                        5      0   100%
api\serializers.py                       36      0   100%
api\signals.py                            9      0   100%
api\tests.py                            150      0   100%
api\urls.py                               4      0   100%
api\views.py                             78      0   100%
-------------------------------------------------------------------
TOTAL                                   357     12    97%
```

