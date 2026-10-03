
# 🔗 URL Shortener API

A production-ready URL Shortener API built with **FastAPI**, **PostgreSQL**, **Redis**, **SQLAlchemy**, and **JWT authentication**.

The project includes URL expiration, Redis caching, rate limiting, click analytics, database migrations, automated testing, Dockerization, CI, and cloud deployment.

---

## 🚀 Live API

**Live API:** `https://url-shortner-39ip.onrender.com`

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "database": "healthy",
  "redis": "healthy"
}
```

> Replace `YOUR-RENDER-URL.onrender.com` with your actual Render URL.

---

# ✨ Features

### 🔐 Authentication

- User registration
- User login
- JWT-based authentication
- Password hashing using Argon2
- Protected API endpoints
- User-specific URL management

### 🔗 URL Shortening

- Generate unique short URLs
- Redirect short URLs to original URLs
- Public redirect endpoint
- URL ownership
- URL activation/deactivation
- URL expiration support

### ⚡ Redis

- Redis-based URL caching
- Cache-aside pattern
- Redis-backed rate limiting
- Cache TTL
- Production Redis using Upstash

### 📊 Analytics

- Track URL clicks
- Store click timestamps
- URL-specific analytics
- Total click count

### 🗄️ Database

- PostgreSQL
- SQLAlchemy ORM
- Alembic migrations
- Foreign-key relationships
- Separate test database

### 🛡️ Security

- JWT authentication
- Argon2 password hashing
- Trusted Host middleware
- Security headers
- Environment-based secrets
- Redis rate limiting
- Protected management endpoints

### 🧪 Testing

- Pytest
- API tests
- Authentication tests
- Redis tests
- Rate-limit tests
- ~90% test coverage
- Separate PostgreSQL test database

### 🐳 DevOps

- Docker
- Docker Compose
- Non-root Docker container
- GitHub Actions CI
- Automated Alembic migrations
- Cloud deployment

### ☁️ Production Deployment

The application is deployed using:

- **Render** — FastAPI application
- **Neon** — PostgreSQL
- **Upstash** — Redis
- HTTPS provided by Render

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         │   Browser/Postman│
                         └────────┬─────────┘
                                  │
                                  │ HTTPS
                                  ▼
                         ┌──────────────────┐
                         │      Render      │
                         │    FastAPI API   │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
             ┌────────────────┐       ┌────────────────┐
             │      Neon      │       │    Upstash     │
             │   PostgreSQL   │       │     Redis      │
             └────────────────┘       └────────────────┘
```

---

# 🧱 Project Structure

```text
URL-Shortner/
│
├── src/
│   ├── models/
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
│   │   ├── url.py
│   │   └── health.py
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
│       ├── logger.py
│       ├── exceptions.py
│       └── security_headers.py
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
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Cache | Redis |
| Production Redis | Upstash |
| Production Database | Neon |
| Authentication | JWT |
| Password Hashing | Argon2 |
| Validation | Pydantic |
| Testing | Pytest |
| Coverage | pytest-cov |
| Containerization | Docker |
| CI | GitHub Actions |
| Deployment | Render |

---

# 🔐 Authentication Flow

```text
User
 │
 │ Register
 ▼
POST /auth/register
 │
 ▼
Password hashed using Argon2
 │
 ▼
PostgreSQL
```

Login:

```text
User
 │
 │ username + password
 ▼
POST /auth/login
 │
 ▼
Verify password
 │
 ▼
Generate JWT
 │
 ▼
Return access token
```

Protected requests:

```text
Client
 │
 │ Authorization: Bearer <JWT>
 ▼
FastAPI
 │
 ▼
JWT verification
 │
 ▼
Current User
 │
 ▼
Protected resource
```

---

# 🔗 API Endpoints

## Authentication

### Register

```http
POST /auth/register
```

Example:

```json
{
  "username": "aditya",
  "email": "aditya@example.com",
  "password": "your-password"
}
```

### Login

```http
POST /auth/login
```

Example:

```json
{
  "username": "aditya",
  "password": "your-password"
}
```

Returns an access token.

---

# 🔗 URL Endpoints

### Create Short URL

```http
POST /url/urls
Authorization: Bearer <token>
```

### Redirect

```http
GET /url/redirect/{short_code}
```

This endpoint is **public**.

Example:

```text
GET /url/redirect/aB92xK
```

The API redirects the user to the original URL.

### URL Details

```http
GET /url/detail/{url_id}
Authorization: Bearer <token>
```

### Get All URLs

```http
GET /url/all
Authorization: Bearer <token>
```

### Get My URLs

```http
GET /url/my-urls?page=1&limit=10
Authorization: Bearer <token>
```

### Deactivate URL

```http
PATCH /url/deactivate/{url_id}
Authorization: Bearer <token>
```

### Analytics

```http
GET /url/analytics/{url_id}
Authorization: Bearer <token>
```

### Health Check

```http
GET /health
```

---

# ⚡ Redis Caching

The redirect system uses the **cache-aside pattern**.

```text
Request
   │
   ▼
Redis
   │
   ├── HIT ────────► Return cached URL
   │
   └── MISS
        │
        ▼
    PostgreSQL
        │
        ▼
    Store in Redis
        │
        ▼
    Redirect
```

Redis key format:

```text
url:{short_code}
```

Cached data contains information such as:

```json
{
  "id": 1,
  "original_url": "https://example.com",
  "is_active": true,
  "expires_at": null
}
```

The cache uses a TTL to prevent stale data from remaining indefinitely.

---

# 🚦 Rate Limiting

The public redirect endpoint uses Redis-based rate limiting.

Current configuration:

```text
10 requests / IP / 60 seconds
```

Redis key:

```text
rate_limit:{ip}
```

When the limit is exceeded:

```http
429 Too Many Requests
```

is returned.

---

# 📊 Click Analytics

Every successful URL redirect creates a click record.

```text
Click
 ├── id
 ├── url_id
 └── clicked_at
```

This allows the application to calculate:

- Total clicks
- Click history
- Future time-based analytics

---

# ⏳ URL Expiration

URLs can optionally have an expiration timestamp.

When an expired URL is requested:

```text
URL
 ↓
Check expiration
 ↓
Expired
 ↓
Reject redirect
```

This prevents expired short URLs from remaining active indefinitely.

---

# 🗄️ Database Design

### User

```text
user_table
├── id
├── username
├── email
├── hash_password
└── created_at
```

### URL

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

### Click

```text
click_table
├── id
├── url_id
└── clicked_at
```

Relationships:

```text
User
 │
 └── 1 ──────── N ─── URL
                       │
                       └── 1 ──────── N ─── Click
```

---

# 🔄 Database Migrations

Alembic is used for database schema management.

Create a migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

Production containers automatically run:

```bash
alembic upgrade head
```

before starting the FastAPI server.

---

# 🧪 Running Tests

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

The project maintains approximately **90% test coverage**.

---

# 🐳 Run Locally with Docker

Start the complete local stack:

```bash
docker compose up --build
```

This starts:

```text
FastAPI
PostgreSQL
Redis
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

Stop containers:

```bash
docker compose down
```

---

# ⚙️ Environment Variables

Create a `.env` file for local development.

Example:

```env
DB_CONNECTION=postgresql://postgres:password@localhost:5432/url_shortener

SECRET_KEY=your-secret-key
ALGORITHM=HS256

TEST_DB_CONNECTION=postgresql://postgres:password@localhost:5432/url_shortener_test

EXPIRATION_TIME=30

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_SSL=false

CORS_ORIGINS=*
ALLOWED_HOSTS=localhost,127.0.0.1
```

Production credentials should be configured through the hosting platform's environment variables.

**Never commit `.env` or production secrets to GitHub.**

---

# 🔒 Security

The project implements several security practices:

- JWT authentication
- Argon2 password hashing
- Environment-based secret management
- Trusted Host middleware
- Security response headers
- Redis-based rate limiting
- Protected URL management endpoints
- Public redirect endpoint separated from management APIs
- Non-root Docker container
- Secrets excluded from Git

---

# 📋 CI Pipeline

GitHub Actions automatically runs the test suite on pushes and pull requests.

```text
Git Push / Pull Request
          │
          ▼
    GitHub Actions
          │
          ├── Python setup
          ├── Install dependencies
          ├── PostgreSQL service
          ├── Redis service
          └── Run Pytest + Coverage
```

---

# ☁️ Production Architecture

The deployed architecture uses managed infrastructure:

```text
                         Internet
                            │
                            ▼
                     Render HTTPS
                            │
                            ▼
                    ┌──────────────┐
                    │   FastAPI    │
                    │    Docker    │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │     Neon     │          │    Upstash   │
       │  PostgreSQL  │          │     Redis    │
       └──────────────┘          └──────────────┘
```

### Production services

**Application**

```text
Render
```

**Database**

```text
Neon PostgreSQL
```

**Redis**

```text
Upstash Redis
```

---

# 🧠 Engineering Concepts Demonstrated

This project was built to understand practical backend engineering concepts including:

- REST API design
- Layered architecture
- Service layer pattern
- Dependency injection
- Authentication and authorization
- JWT
- Password hashing
- SQLAlchemy ORM
- PostgreSQL
- Database migrations
- Cache-aside pattern
- Redis
- Rate limiting
- URL expiration
- Analytics
- Centralized exception handling
- Structured logging
- Health checks
- Automated testing
- Test database isolation
- Docker
- CI/CD
- Cloud deployment
- Environment-based configuration

---

# 🚀 Future Improvements

Possible future improvements include:

- Custom short codes
- QR code generation
- Advanced click analytics
- Geographic analytics
- Device/browser analytics
- Background jobs
- Celery/RQ integration
- API versioning
- Prometheus metrics
- Grafana monitoring
- Distributed rate limiting
- Custom domains
- Frontend dashboard
- OpenAPI documentation improvements

---

# 📌 Project Highlights

```text
Backend Framework     → FastAPI
Database              → PostgreSQL
Cache                 → Redis
Authentication        → JWT
Password Hashing      → Argon2
ORM                   → SQLAlchemy
Migration             → Alembic
Testing               → Pytest
Containerization      → Docker
CI                    → GitHub Actions
Cloud                  → Render
Managed PostgreSQL    → Neon
Managed Redis         → Upstash
```

---

# 👨‍💻 Author

**Aditya Pandey**

Built as a backend engineering project to explore production-oriented API development, caching, authentication, database design, testing, containerization, and cloud deployment.
```