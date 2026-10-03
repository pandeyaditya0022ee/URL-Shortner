
# 🔗 URL Shortener API

A production-oriented URL Shortener REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **Redis**, **JWT Authentication**, **Pytest**, and **Docker**.

The project provides authenticated URL management, short-code based redirection, URL expiration, deactivation, click analytics, Redis caching, IP-based rate limiting, database migrations, automated testing, and containerized development.

---

## ✨ Features

- 🔐 JWT-based authentication
- 👤 User registration and login
- 🔑 Password hashing with Argon2
- 🔗 Unique short URL generation
- ↗️ Short URL redirection
- ⏳ URL expiration support
- 🚫 URL deactivation
- 👤 User ownership validation
- 📊 Click analytics
- ⚡ Redis caching
- 🛡️ Redis-based IP rate limiting
- 📄 Pagination for user URLs
- 🗄️ PostgreSQL database
- 🔄 Alembic database migrations
- 📝 Application logging
- 🧪 Automated testing with Pytest
- 📈 Approximately 90% test coverage
- 🐳 Dockerized application
- 🐘 Dockerized PostgreSQL
- 🔴 Dockerized Redis
- 📚 Automatic Swagger/OpenAPI documentation

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **Python** | Backend programming language |
| **PostgreSQL** | Relational database |
| **SQLAlchemy** | ORM |
| **Alembic** | Database migrations |
| **Redis** | Caching and rate limiting |
| **JWT** | Authentication |
| **Pydantic** | Request/response validation |
| **Argon2** | Password hashing |
| **Pytest** | Automated testing |
| **pytest-cov** | Test coverage |
| **Docker** | Containerization |
| **Docker Compose** | Multi-container orchestration |
| **Uvicorn** | ASGI server |

---

# 🏗️ Architecture

```text
                         ┌───────────────┐
                         │     Client    │
                         │   Postman /   │
                         │    Browser    │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    FastAPI    │
                         │      API      │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
       │ PostgreSQL  │    │    Redis    │    │    JWT      │
       │             │    │             │    │    Auth     │
       │ Users       │    │ URL Cache   │    │             │
       │ URLs        │    │ Rate Limit  │    │             │
       │ Clicks      │    │             │    │             │
       └─────────────┘    └─────────────┘    └─────────────┘
              │
              ▼
       ┌─────────────┐
       │ SQLAlchemy  │
       │    ORM      │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │   Alembic   │
       │  Migration  │
       └─────────────┘
```

---

# 📁 Project Structure

```text
url_shortner/
│
├── src/
│   ├── __init__.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── url.py
│   │   └── click.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── url.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   └── url.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── url_service.py
│   │
│   └── utils/
│       ├── db.py
│       ├── security.py
│       ├── settings.py
│       ├── dependencies.py
│       ├── redis_client.py
│       └── logger.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_login.py
│   ├── test_url.py
│   ├── test_redis.py
│   └── test_rate_limit.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── main.py
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

---

# 🔐 Authentication

The API uses **JWT-based authentication**.

The authentication flow is:

```text
                Registration
                     │
                     ▼
              Password Hashing
                     │
                     ▼
                PostgreSQL
                     │
                     │
                  Login
                     │
                     ▼
              Verify Password
                     │
                     ▼
                Generate JWT
                     │
                     ▼
              Access Protected
                  Endpoints
```

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

Passwords are never stored as plaintext. They are hashed before being stored in PostgreSQL.

---

# 📡 API Endpoints

## 🔐 Authentication

### Register User

```http
POST /auth/register
```

Authentication required:

```text
No
```

Example request:

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "password123"
}
```

Response:

```text
201 Created
```

---

### Login

```http
POST /auth/login
```

Authentication required:

```text
No
```

Example request:

```json
{
  "username": "user1",
  "password": "password123"
}
```

Response:

```text
200 OK
```

The response contains a JWT access token.

---

# 🔗 URL Management

All URL-management endpoints require JWT authentication.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/url/urls` | Create a short URL |
| `GET` | `/url/redirect/{short_code}` | Redirect using short code |
| `GET` | `/url/detail/{url_id}` | Get URL details |
| `GET` | `/url/all` | Get URLs |
| `GET` | `/url/my-urls` | Get authenticated user's URLs |
| `PATCH` | `/url/deactivate/{url_id}` | Deactivate a URL |
| `GET` | `/url/analytics/{url_id}` | Get URL analytics |

---

## ➕ Create Short URL

```http
POST /url/urls
Authorization: Bearer <access_token>
```

Creates a new shortened URL for the authenticated user.

Response:

```text
201 Created
```

---

## ↗️ Redirect to Original URL

```http
GET /url/redirect/{short_code}
Authorization: Bearer <access_token>
```

Response:

```text
307 Temporary Redirect
```

The redirect flow uses Redis caching before querying PostgreSQL.

The endpoint also performs:

- URL existence validation
- Active status validation
- Expiration validation
- Click recording
- Rate limiting

---

## 🔎 Get URL Details

```http
GET /url/detail/{url_id}
Authorization: Bearer <access_token>
```

Returns details for a URL owned by the authenticated user.

Response:

```text
200 OK
```

---

## 📋 Get All URLs

```http
GET /url/all
Authorization: Bearer <access_token>
```

Returns URLs according to the application's URL service logic.

Response:

```text
200 OK
```

---

## 📑 Get My URLs

```http
GET /url/my-urls
Authorization: Bearer <access_token>
```

Supports pagination.

### Query Parameters

| Parameter | Default | Constraint |
|---|---:|---|
| `page` | `1` | `>= 1` |
| `limit` | `10` | `1 - 50` |

Example:

```http
GET /url/my-urls?page=1&limit=10
```

---

## 🚫 Deactivate URL

```http
PATCH /url/deactivate/{url_id}
Authorization: Bearer <access_token>
```

Deactivates a URL owned by the authenticated user.

Response:

```text
200 OK
```

---

## 📊 URL Analytics

```http
GET /url/analytics/{url_id}
Authorization: Bearer <access_token>
```

Returns click analytics for the requested URL.

Response:

```text
200 OK
```

Each successful redirect creates a click record.

---

# ⚡ Redis Caching

Redis is used to reduce repeated database queries for frequently accessed short URLs.

The cache follows a **cache-aside** strategy.

```text
                  Request
                     │
                     ▼
                 Redis GET
                     │
             ┌───────┴───────┐
             │               │
           CACHE HIT      CACHE MISS
             │               │
             │               ▼
             │          PostgreSQL
             │               │
             │               ▼
             │          Store in Redis
             │               │
             └───────┬───────┘
                     ▼
              Validate URL
                     │
                     ▼
               Record Click
                     │
                     ▼
                 Redirect
```

Cache keys follow the pattern:

```text
url:{short_code}
```

Cached URL information includes:

- URL ID
- Original URL
- Active status
- Expiration time

Cached entries use a TTL to prevent stale data from remaining indefinitely.

---

# 🛡️ Rate Limiting

Redis is also used for IP-based rate limiting.

The redirect endpoint maintains a request counter using the client's IP address.

```text
Incoming Request
       │
       ▼
   Client IP
       │
       ▼
Redis INCR
       │
       ▼
Check Request Count
       │
    ┌──┴──┐
    │     │
 Allowed  Limit Exceeded
    │          │
    ▼          ▼
 Process      429
 Request      Too Many Requests
```

The rate-limit key automatically expires after the configured time window.

---

# ⏳ URL Expiration

URLs can have an optional expiration time.

During redirection:

```text
Request
   │
   ▼
Find URL
   │
   ▼
Is Active?
   │
   ▼
Has Expired?
   │
   ├── Yes → Reject
   │
   └── No
        │
        ▼
     Redirect
```

This validation is performed whether the URL is retrieved from Redis or PostgreSQL.

---

# 📊 Click Analytics

Every successful redirect creates a record in the click table.

```text
Short URL Request
       │
       ▼
URL Validation
       │
       ▼
Create Click Record
       │
       ▼
PostgreSQL
```

The click model stores:

```text
click_table
├── id
├── url_id
└── clicked_at
```

Analytics can then aggregate clicks for a specific URL.

---

# 🗄️ Database Design

The project uses PostgreSQL with SQLAlchemy ORM.

## User Table

```text
user_table
├── id
├── username
├── email
├── hash_password
└── created_at
```

## URL Table

```text
url_table
├── id
├── original_url
├── short_code
├── created_at
├── expires_at
├── is_active
└── user_id
```

## Click Table

```text
click_table
├── id
├── url_id
└── clicked_at
```

### Relationships

```text
User
 │
 │ 1
 │
 └─────────── N
             │
            URL
             │
             │ 1
             │
             └─────────── N
                         │
                        Click
```

---

# 🔄 Database Migrations

**Alembic** is used as the source of truth for database schema changes.

Create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback one migration:

```bash
alembic downgrade -1
```

When the Docker application starts, Alembic automatically runs:

```bash
alembic upgrade head
```

before starting Uvicorn.

---

# 🧪 Testing

The project uses **Pytest** for automated testing.

Tests cover:

- User registration
- Authentication
- Login
- JWT authentication
- URL creation
- URL redirection
- URL expiration
- URL deactivation
- URL ownership
- Redis cache hit
- Redis cache miss
- Redis TTL
- Rate limiting
- Analytics

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

The current test suite achieves approximately:

```text
90% coverage
```

---

# 🐳 Docker

The project is fully containerized using Docker Compose.

The application consists of three services:

```text
┌─────────────────────────────┐
│       Docker Compose        │
│                             │
│  ┌─────────┐                │
│  │ FastAPI │                │
│  │   App   │                │
│  └────┬────┘                │
│       │                     │
│  ┌────┴────┐    ┌────────┐ │
│  │Postgres │    │ Redis  │ │
│  └─────────┘    └────────┘ │
│                             │
└─────────────────────────────┘
```

---

# 🚀 Running the Project

## Prerequisites

Make sure you have installed:

- Python 3.12+
- Docker
- Docker Compose
- Git

---

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd url_shortner
```

---

## 2. Create Environment File

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Configure your environment variables.

Example:

```env
DB_CONNECTION=postgresql://postgres:<password>@postgres:5432/url_shortener

JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

TEST_DB_CONNECTION=postgresql://postgres:<password>@localhost:5432/url_shortener_test
```

> Never commit `.env` or production secrets to GitHub.

---

## 3. Start the Application

```bash
docker compose up --build
```

Docker Compose starts:

```text
FastAPI
PostgreSQL
Redis
```

Alembic automatically applies pending migrations before FastAPI starts.

---

## 4. Open Swagger Documentation

Once the application is running:

```text
http://localhost:8000/docs
```

FastAPI also provides the OpenAPI specification:

```text
http://localhost:8000/openapi.json
```

---

# 📝 Environment Variables

| Variable | Description |
|---|---|
| `DB_CONNECTION` | PostgreSQL connection string |
| `TEST_DB_CONNECTION` | PostgreSQL test database connection |
| `JWT_SECRET_KEY` | Secret used for JWT signing |
| `JWT_ALGORITHM` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration duration |

Use `.env.example` as the template for local configuration.

---

# 🔒 Security Considerations

The project implements several security mechanisms:

### Password Security

Passwords are hashed before storage using Argon2.

### JWT Authentication

Protected endpoints require a valid JWT access token.

### Authorization

URL ownership is checked before performing protected URL operations.

### Rate Limiting

Redis-based rate limiting helps restrict excessive requests.

### Environment Variables

Sensitive configuration is kept outside the source code using environment variables.

### Database Constraints

Foreign keys and unique constraints help maintain data integrity.

---

# 📝 Logging

The application uses Python's logging system for application-level logging.

Important operations include logging information around:

- URL creation
- Redis cache hits
- Redis cache misses

Logs can be viewed through Docker:

```bash
docker compose logs app
```

---

# 🧩 Service Layer Architecture

The project separates API routes from business logic.

```text
Request
   │
   ▼
Route
   │
   ▼
Service Layer
   │
   ├──────────────┐
   ▼              ▼
Database        Redis
```

For example:

```text
src/routes/url.py
        │
        ▼
src/services/url_service.py
        │
        ├── PostgreSQL
        │
        └── Redis
```

This keeps route handlers lightweight and separates business logic from HTTP-specific code.

---

# 🧪 Test Database

Tests use a separate PostgreSQL database instead of the development database.

```text
Application
     │
     ▼
Development DB

Tests
     │
     ▼
Test DB
```

FastAPI's database dependency is overridden during testing so that tests operate against the dedicated test database.

Redis state is also cleaned where required to prevent rate-limit and cache state from leaking between tests.

---

# 📈 Project Metrics

Current project characteristics:

```text
Backend Framework      → FastAPI
Database               → PostgreSQL
ORM                    → SQLAlchemy
Cache                  → Redis
Authentication         → JWT
Password Hashing       → Argon2
Migration Tool         → Alembic
Testing                → Pytest
Coverage               → ~90%
Containerization       → Docker
Orchestration          → Docker Compose
```

---

# 🎯 Engineering Concepts Demonstrated

This project was built to practice practical backend engineering concepts including:

- REST API design
- Authentication and authorization
- Password hashing
- JWT tokens
- Dependency injection
- SQLAlchemy ORM
- PostgreSQL relationships
- Database constraints
- Database migrations
- Redis caching
- Cache-aside pattern
- Rate limiting
- Pagination
- URL expiration
- Click analytics
- Service-layer architecture
- Automated testing
- Test database isolation
- Docker containerization
- Multi-container orchestration
- Environment-based configuration
- Application logging

---

# 🚧 Future Improvements

Possible future improvements include:

- [ ] GitHub Actions CI/CD
- [ ] Production deployment
- [ ] Health-check endpoint
- [ ] Structured JSON logging
- [ ] Advanced analytics
- [ ] QR code generation
- [ ] Custom short aliases
- [ ] API versioning
- [ ] Background jobs
- [ ] Monitoring and metrics
- [ ] Reverse proxy configuration
- [ ] Improved Redis failure handling
- [ ] Production-grade deployment configuration

---

# 📌 Project Status

```text
Core API                 ✅
Authentication           ✅
PostgreSQL               ✅
SQLAlchemy               ✅
Alembic                  ✅
Redis Cache              ✅
Rate Limiting            ✅
Click Analytics          ✅
URL Expiration           ✅
URL Deactivation         ✅
Pagination               ✅
Testing                  ✅
~90% Coverage            ✅
Docker                   ✅
Docker Compose           ✅
API Documentation        ✅
```

---

# 👨‍💻 Author

**Aditya Kumar Pandey**

Backend engineering project focused on building a production-oriented URL shortening service with FastAPI, PostgreSQL, Redis, authentication, testing, migrations, and Docker.

---

## ⭐ If you found this project useful

Feel free to explore the source code, raise issues, or suggest improvements.
```