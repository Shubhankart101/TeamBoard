# 📡 API Reference & OpenAPI Documentation

This document describes the API endpoints, Swagger/ReDoc interactive documentation, and Postman test collection for **TeamBoard**.

---

## 📖 Interactive Documentation Endpoints

TeamBoard uses `drf-spectacular` to generate OpenAPI 3.0 schemas and interactive UIs:

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc UI:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI 3.0 Schema (JSON):** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 🚀 Endpoints Reference

### 1. Register a New Company
`POST /api/auth/register/` (Public)

Creates a new Django `User` and updates the auto-generated `Company` profile. Returns auto-generated `api_key` and JWT `access` token.

**Request Body:**
```json
{
  "username": "acmecorp",
  "password": "securepass123",
  "company_name": "Acme Corp",
  "email": "dev@acmecorp.com"
}
```

**Response (201 Created):**
```json
{
  "username": "acmecorp",
  "company_name": "Acme Corp",
  "api_key": "gTk8...auto-generated...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

---

### 2. Company Login
`POST /api/auth/login/` (Public)

Authenticates user credentials and returns a fresh JWT access token, company name, and API key.

**Request Body:**
```json
{
  "username": "acmecorp",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "company_name": "Acme Corp",
  "api_key": "gTk8..."
}
```

---

### 3. Query Knowledge Base
`POST /api/kb/query/` (Protected — Requires `Authorization: Bearer <access_token>`)

Searches `KBEntry` records where `question` or `answer` contains the search term. Atomically creates a `QueryLog` entry.

**Request Body:**
```json
{
  "search": "select_related"
}
```

**Response (200 OK):**
```json
{
  "search": "select_related",
  "count": 2,
  "results": [
    {
      "id": 1,
      "question": "What is select_related in Django ORM?",
      "answer": "select_related performs a SQL JOIN and fetches...",
      "category": "database"
    }
  ]
}
```

---

### 4. Admin Usage Summary Dashboard
`GET /api/admin/usage-summary/` (Protected — Requires `Authorization: Bearer <admin_access_token>`)

Platform-wide usage metrics reserved for companies with `role == 'admin'`.

**Response (200 OK):**
```json
{
  "total_queries": 254,
  "active_companies": 7,
  "top_search_terms": [
    { "search_term": "select_related", "count": 42 },
    { "search_term": "transaction atomic", "count": 31 },
    { "search_term": "JWT authentication", "count": 28 },
    { "search_term": "Q objects", "count": 19 },
    { "search_term": "signals django", "count": 14 }
  ]
}
```

---

## 📮 Postman Collection Scenarios

Import [TeamBoard.postman_collection.json](TeamBoard.postman_collection.json) into Postman to execute all 11 test scenarios:

| # | Scenario Name | Endpoint | Expected Result |
|---|---|---|---|
| 1 | Register a new company | `POST /api/auth/register/` | `201 Created` + `api_key` + JWT access token |
| 2 | Register with duplicate username | `POST /api/auth/register/` | `400 Bad Request` |
| 3 | Login with valid credentials | `POST /api/auth/login/` | `200 OK` + JWT token + `company_name` + `api_key` |
| 4 | Login with wrong password | `POST /api/auth/login/` | `401 Unauthorized` |
| 5 | Query KB - no token | `POST /api/kb/query/` | `401 Unauthorized` |
| 6 | Query KB - valid token, keyword with results | `POST /api/kb/query/` | `200 OK` + results list (`count > 0`) |
| 7 | Query KB - valid token, no matching results | `POST /api/kb/query/` | `200 OK` + empty results list (`count = 0`) |
| 8 | Query KB - missing search field | `POST /api/kb/query/` | `400 Bad Request` |
| 9 | Usage summary - CLIENT token | `GET /api/admin/usage-summary/` | `403 Forbidden` |
| 10 | Usage summary - Admin token | `GET /api/admin/usage-summary/` | `200 OK` + usage stats dashboard |
| 11 | Verify QueryLog created | Postman DB Check | QueryLog records created in `query_logs` table |
