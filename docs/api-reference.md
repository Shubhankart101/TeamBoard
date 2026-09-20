# 📡 API Reference & OpenAPI Documentation

This document provides a comprehensive API reference for **TeamBoard — B2B Knowledge Base API Platform**, including interactive OpenAPI 3.0 documentation endpoints, request/response schema specifications, HTTP status codes, error payload shapes, and the 11-scenario Postman test collection matrix.

---

## 📖 Interactive OpenAPI 3.0 Documentation

TeamBoard integrates `drf-spectacular` for OpenAPI 3.0 schema generation and interactive UI endpoints:

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/) (Interactive testing console)
- **ReDoc UI:** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/) (Clean structured API reference)
- **OpenAPI 3.0 Schema (JSON):** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/) (Raw schema definition)

---

## 🚀 API Endpoints Specification

### 1. Register a New Company
`POST /api/auth/register/` (Public Endpoint)

Registers a new user account, updates the automatically created `Company` profile, and assigns the `CLIENT` role. Generates and returns a 32-character API key alongside a fresh SimpleJWT access token.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Payload
```json
{
  "username": "acmecorp",
  "password": "securepass123",
  "company_name": "Acme Corp",
  "email": "dev@acmecorp.com"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | String | Yes | Unique login username for the company |
| `password` | String | Yes | Account password |
| `company_name` | String | Yes | Legal / display name of the company |
| `email` | String | No | Contact email address |

#### Responses

- **201 Created**: Registration successful.
  ```json
  {
    "username": "acmecorp",
    "company_name": "Acme Corp",
    "api_key": "gTk8_xX9vL2...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **400 Bad Request**: Missing mandatory fields or duplicate username.
  ```json
  {
    "error": "username, password, and company_name are required."
  }
  ```
  ```json
  {
    "error": "Username already exists."
  }
  ```

---

### 2. Company Login
`POST /api/auth/login/` (Public Endpoint)

Authenticates user credentials using Django's `authenticate()`. Upon success, returns a fresh SimpleJWT access token, the company name, and the auto-generated API key.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Payload
```json
{
  "username": "acmecorp",
  "password": "securepass123"
}
```

#### Responses

- **200 OK**: Authentication successful.
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "company_name": "Acme Corp",
    "api_key": "gTk8_xX9vL2..."
  }
  ```
- **400 Bad Request**: Missing username or password.
  ```json
  {
    "error": "username and password are required."
  }
  ```
- **401 Unauthorized**: Invalid username or password.
  ```json
  {
    "detail": "Invalid credentials"
  }
  ```

---

### 3. Query Knowledge Base
`POST /api/kb/query/` (Protected Endpoint — Requires SimpleJWT Bearer Token)

Searches Knowledge Base (`KBEntry`) records where `question` or `answer` contains the requested search term (case-insensitive `icontains` via `Q` objects). The search and query audit log creation are executed inside an atomic transaction (`transaction.atomic()`).

#### Request Headers
```http
Content-Type: application/json
Authorization: Bearer <access_token>
```

#### Request Payload
```json
{
  "search": "select_related"
}
```

#### Responses

- **200 OK**: Search executed successfully (returns count and matching results array).
  ```json
  {
    "search": "select_related",
    "count": 2,
    "results": [
      {
        "id": 1,
        "question": "What is select_related in Django ORM?",
        "answer": "select_related performs a SQL JOIN and fetches related single-valued relationships in a single query.",
        "category": "database"
      },
      {
        "id": 2,
        "question": "How to use select_related for query optimization?",
        "answer": "You can use select_related when accessing foreign keys to avoid N+1 query problems.",
        "category": "database"
      }
    ]
  }
  ```
- **200 OK (Zero Results)**: Search executed, 0 matches found (`QueryLog` entry is still committed).
  ```json
  {
    "search": "nonexistentterm9999",
    "count": 0,
    "results": []
  }
  ```
- **400 Bad Request**: Missing or empty `search` field in request body.
  ```json
  {
    "error": "Search field is required."
  }
  ```
- **401 Unauthorized**: Missing, expired, or malformed JWT Bearer token.
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

---

### 4. Admin Usage Summary Dashboard
`GET /api/admin/usage-summary/` (Protected Endpoint — Requires Admin SimpleJWT Bearer Token)

Returns platform-wide query statistics: total queries executed, number of distinct active companies, and top 5 most frequently searched terms. Restricted to companies with `role == 'admin'` via custom `IsAdminUser` permission.

#### Request Headers
```http
Authorization: Bearer <admin_access_token>
```

#### Responses

- **200 OK**: Usage summary retrieved successfully.
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
- **401 Unauthorized**: Missing or invalid Bearer token.
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```
- **403 Forbidden**: Requesting token belongs to a customer with `role == 'client'`.
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```

---

## 📮 Postman Test Collection Matrix

Import `TeamBoard.postman_collection.json` into Postman to run the 11-scenario automated test suite:

| # | Scenario Name | Endpoint | Auth | Request Summary | Expected Status Code & Assertions |
|---|---|---|---|---|---|
| 1 | Register a new company | `POST /api/auth/register/` | None | Valid registration details | `201 Created`: Contains `api_key` & `access` token; sets `client_token` collection variable |
| 2 | Register duplicate username | `POST /api/auth/register/` | None | Re-send existing username | `400 Bad Request`: Rejects duplicate registration |
| 3 | Login with valid credentials | `POST /api/auth/login/` | None | Valid username & password | `200 OK`: Returns fresh JWT `access` token, `company_name`, & `api_key` |
| 4 | Login with wrong password | `POST /api/auth/login/` | None | Invalid password | `401 Unauthorized`: Returns detail `"Invalid credentials"` |
| 5 | Query KB — no token | `POST /api/kb/query/` | None | Search payload without header | `401 Unauthorized`: Authentication required |
| 6 | Query KB — valid token with results | `POST /api/kb/query/` | Bearer | Search term `"select_related"` | `200 OK`: `count > 0` & non-empty `results` array |
| 7 | Query KB — valid token no results | `POST /api/kb/query/` | Bearer | Search term `"nonexistentterm9999"` | `200 OK`: `count == 0` & empty `results` array |
| 8 | Query KB — missing search field | `POST /api/kb/query/` | Bearer | Payload `{}` | `400 Bad Request`: Search field required error |
| 9 | Usage summary — CLIENT token | `GET /api/admin/usage-summary/` | Bearer (Client) | Request dashboard as client | `403 Forbidden`: Custom `IsAdminUser` blocks access |
| 10 | Usage summary — Admin token | `GET /api/admin/usage-summary/` | Bearer (Admin) | Request dashboard as admin | `200 OK`: Returns `total_queries`, `active_companies`, & `top_search_terms` |
| 11 | Verify QueryLog creation | Postman DB Check | None | Audit log verification | `200 OK`: Asserts `total_queries >= 1` after scenarios 6 & 7 |

