# EduNexus Backend Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT APPLICATIONS                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Flutter    │  │     Web      │  │   Mobile     │              │
│  │   (Mobile)   │  │  (Browser)   │  │   (Native)   │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼──────────────────┼──────────────────┼──────────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         BACKEND LAYER                                │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    FastAPI (Port 8000)                        │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────┐ │  │
│  │  │   Auth     │ │ Questions  │ │  Practice  │ │   Tests   │ │  │
│  │  │  /register │ │   /list    │ │  /session  │ │ /generate │ │  │
│  │  │   /login   │ │   /get     │ │  /attempt  │ │  /submit  │ │  │
│  │  │  /refresh  │ │            │ │  /history  │ │  /history │ │  │
│  │  │    /me     │ │            │ │            │ │           │ │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └───────────┘ │  │
│  │                                                               │  │
│  │  ┌─────────────────────────────────────────────────────────┐ │  │
│  │  │              JWT Authentication Layer                   │ │  │
│  │  │  • Bearer Token Validation                              │ │  │
│  │  │  • User Context Injection                               │ │  │
│  │  └─────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                     Flask (Port 5000)                         │  │
│  │  ┌──────────────────────┐  ┌──────────────────────────────┐  │  │
│  │  │   Health Dashboard   │  │    Question Import           │  │  │
│  │  │   /admin/health      │  │    /admin/questions/import   │  │  │
│  │  │  • API Status        │  │  • CSV Upload                │  │  │
│  │  │  • DB Status         │  │  • JSON Upload               │  │  │
│  │  │  • System Info       │  │  • Validation                │  │  │
│  │  │  • Auto-refresh      │  │  • Bulk Insert               │  │  │
│  │  └──────────────────────┘  └──────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Shared Components                          │  │
│  │  ┌────────────┐ ┌────────────┐ ┌─────────────┐              │  │
│  │  │   Models   │ │  Schemas   │ │   Security  │              │  │
│  │  │ SQLAlchemy │ │  Pydantic  │ │  JWT/Bcrypt │              │  │
│  │  └────────────┘ └────────────┘ └─────────────┘              │  │
│  └───────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   PostgreSQL Database                         │  │
│  │                                                               │  │
│  │  ┌──────────┐ ┌───────────┐ ┌─────────────┐ ┌───────────┐  │  │
│  │  │  users   │ │ questions │ │  practice   │ │   tests   │  │  │
│  │  │          │ │           │ │  _sessions  │ │           │  │  │
│  │  └──────────┘ └───────────┘ └─────────────┘ └───────────┘  │  │
│  │                                                               │  │
│  │  ┌──────────┐ ┌───────────┐                                  │  │
│  │  │ attempts │ │   test    │                                  │  │
│  │  │          │ │ _attempts │                                  │  │
│  │  └──────────┘ └───────────┘                                  │  │
│  │                                                               │  │
│  │  Managed by: Alembic (Unified Migrations)                    │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. FastAPI REST API (Port 8000)

#### Authentication Module
```
/api/auth
├── POST /register      → Create new user account
├── POST /login         → Authenticate and get JWT tokens
├── POST /refresh       → Refresh expired access token
└── GET  /me            → Get current user profile
```

#### Questions Module
```
/api/questions
├── GET  /              → List questions with filters
│                         • section: math|reading|writing
│                         • topic: string
│                         • subtopic: string
│                         • difficulty: easy|medium|hard
│                         • shuffle: boolean
│                         • limit: 1-100
└── GET  /{id}          → Get specific question by ID
```

#### Practice Module
```
/api/practice
├── POST /session/start → Start new practice session
│                         Input: {"topics": ["Algebra", "Geometry"]}
│                         Output: session_id
├── POST /attempt       → Submit answer for question
│                         Input: {session_id, question_id, user_answer, time_spent}
│                         Output: {is_correct, ...}
└── GET  /history       → Get user's practice history
                          Output: [{session_id, accuracy, ...}]
```

#### Tests Module
```
/api/tests
├── POST /generate      → Generate SAT-style test
│                         Input: {test_type, num_questions}
│                         Output: {test_id, question_ids}
├── POST /submit        → Submit completed test
│                         Input: {test_id, answers[]}
│                         Output: {score, correct_count}
└── GET  /history       → Get user's test history
                          Output: [{test_id, score, ...}]
```

#### Health Module
```
/api/health
└── GET  /              → System health check
                          Output: {status, api, database, timestamp}
```

### 2. Flask Admin Panel (Port 5000)

#### Health Dashboard
```
/admin/health
└── GET  /              → Visual monitoring dashboard
                          • API health status
                          • Database connectivity
                          • System timestamp
                          • Auto-refresh (30s)
```

#### Question Management
```
/admin/questions
└── POST /import        → Bulk import questions
                          • Accepts: CSV, JSON
                          • Validates: Schema, constraints
                          • Returns: Success/error report
```

### 3. Database Schema

```
┌─────────────────────────┐
│         users           │
├─────────────────────────┤
│ id (PK)                 │
│ email (UNIQUE)          │
│ hashed_password         │
│ is_active               │
│ created_at              │
└───────┬─────────────────┘
        │
        │ 1:N
        │
        ├─────────────────────────┬─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         │
┌──────────────────┐    ┌──────────────────┐              │
│ practice_sessions│    │      tests       │              │
├──────────────────┤    ├──────────────────┤              │
│ id (PK)          │    │ id (PK)          │              │
│ user_id (FK)     │    │ user_id (FK)     │              │
│ topics           │    │ test_type        │              │
│ started_at       │    │ questions (JSON) │              │
│ ended_at         │    │ started_at       │              │
└───────┬──────────┘    │ submitted_at     │              │
        │               │ score            │              │
        │ 1:N           └───────┬──────────┘              │
        │                       │                         │
        ▼                       │ 1:N                     │
┌──────────────────┐            ▼                         │
│    attempts      │    ┌──────────────────┐              │
├──────────────────┤    │  test_attempts   │              │
│ id (PK)          │    ├──────────────────┤              │
│ session_id (FK)  │    │ id (PK)          │              │
│ question_id (FK) │◄───┤ test_id (FK)     │              │
│ user_answer      │    │ question_id (FK) │              │
│ is_correct       │    │ user_answer      │              │
│ time_spent       │    │ is_correct       │              │
│ attempted_at     │    │ time_spent       │              │
└──────────────────┘    │ answered_at      │              │
                        └──────────────────┘              │
                                                          │
┌─────────────────────────────────────────────────────────┘
│
│ Referenced by attempts & test_attempts
▼
┌──────────────────────────┐
│       questions          │
├──────────────────────────┤
│ id (PK)                  │
│ section (ENUM)           │  ← math, reading, writing
│ topic                    │
│ subtopic                 │
│ difficulty (ENUM)        │  ← easy, medium, hard
│ question_text            │
│ choices (JSON)           │  ← Array of 4 strings
│ correct_answer (ENUM)    │  ← A, B, C, D
│ explanation              │
│ created_at               │
└──────────────────────────┘
```

## Data Flow

### User Registration & Authentication Flow
```
1. Client                 2. FastAPI              3. Database
   │                         │                         │
   ├─ POST /auth/register ──►│                         │
   │  {email, password}      │                         │
   │                         ├─ Hash password          │
   │                         ├─ Create User ──────────►│
   │                         │                         ├─ INSERT users
   │                         │◄────────────────────────┤
   │◄─ 201 Created ──────────┤                         │
   │  {id, email, ...}       │                         │
   │                         │                         │
   ├─ POST /auth/login ─────►│                         │
   │  {email, password}      │                         │
   │                         ├─ Query User ───────────►│
   │                         │◄────────────────────────┤
   │                         ├─ Verify password        │
   │                         ├─ Generate JWT           │
   │◄─ 200 OK ───────────────┤                         │
   │  {access_token,         │                         │
   │   refresh_token}        │                         │
```

### Practice Session Flow
```
1. Client                 2. FastAPI              3. Database
   │                         │                         │
   ├─ POST /practice/       │                         │
   │  session/start ────────►│ (Auth: Bearer token)    │
   │  {topics: [...]}        │                         │
   │                         ├─ Validate JWT           │
   │                         ├─ Get User               │
   │                         ├─ Create Session ───────►│
   │                         │                         ├─ INSERT
   │◄─ 200 OK ───────────────┤◄────────────────────────┤
   │  {session_id, ...}      │                         │
   │                         │                         │
   ├─ GET /questions ───────►│                         │
   │  ?section=math&         │                         │
   │   difficulty=easy       │                         │
   │                         ├─ Query Questions ──────►│
   │◄─ 200 OK ───────────────┤◄────────────────────────┤
   │  [{question}, ...]      │                         │
   │                         │                         │
   ├─ POST /practice/        │                         │
   │  attempt ───────────────►│                         │
   │  {session_id,           │                         │
   │   question_id,          │                         │
   │   user_answer: "B"}     │                         │
   │                         ├─ Get Question ─────────►│
   │                         │◄────────────────────────┤
   │                         ├─ Check correctness      │
   │                         ├─ Save Attempt ─────────►│
   │◄─ 200 OK ───────────────┤◄────────────────────────┤
   │  {is_correct: true}     │                         │
```

### Test Generation & Submission Flow
```
1. Client                 2. FastAPI              3. Database
   │                         │                         │
   ├─ POST /tests/          │                         │
   │  generate ─────────────►│ (Auth: Bearer token)    │
   │  {test_type,            │                         │
   │   num_questions: 50}    │                         │
   │                         ├─ Query Questions ──────►│
   │                         │  (Random sample)        │
   │                         │◄────────────────────────┤
   │                         ├─ Create Test ──────────►│
   │                         ├─ Create TestAttempts ──►│
   │◄─ 200 OK ───────────────┤◄────────────────────────┤
   │  {test_id,              │                         │
   │   questions: [ids]}     │                         │
   │                         │                         │
   │ ... user takes test ... │                         │
   │                         │                         │
   ├─ POST /tests/submit ───►│                         │
   │  {test_id,              │                         │
   │   answers: [{           │                         │
   │     question_id,        │                         │
   │     user_answer         │                         │
   │   }, ...]}              │                         │
   │                         ├─ Get Questions ────────►│
   │                         │◄────────────────────────┤
   │                         ├─ Check each answer      │
   │                         ├─ Calculate score        │
   │                         ├─ Update Test ──────────►│
   │                         ├─ Update TestAttempts ──►│
   │◄─ 200 OK ───────────────┤◄────────────────────────┤
   │  {score: 82.5,          │                         │
   │   correct: 41/50}       │                         │
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Input Validation Layer (Pydantic)                  │
│     ┌────────────────────────────────────────┐         │
│     │ • Email format validation              │         │
│     │ • Password strength (min 8 chars)      │         │
│     │ • Question choices (exactly 4)         │         │
│     │ • Answer validation (A-D only)         │         │
│     │ • Enum validation (section, difficulty)│         │
│     └────────────────────────────────────────┘         │
│                                                         │
│  2. Authentication Layer (JWT)                         │
│     ┌────────────────────────────────────────┐         │
│     │ • Access token (30 min expiry)         │         │
│     │ • Refresh token (7 day expiry)         │         │
│     │ • HS256 algorithm                      │         │
│     │ • Token type validation                │         │
│     │ • User context injection               │         │
│     └────────────────────────────────────────┘         │
│                                                         │
│  3. Authorization Layer                                │
│     ┌────────────────────────────────────────┐         │
│     │ • User ownership validation            │         │
│     │ • Session ownership check              │         │
│     │ • Test ownership check                 │         │
│     │ • Protected endpoint enforcement       │         │
│     └────────────────────────────────────────┘         │
│                                                         │
│  4. Password Security (Bcrypt)                         │
│     ┌────────────────────────────────────────┐         │
│     │ • Bcrypt hashing (auto-salt)           │         │
│     │ • No plaintext storage                 │         │
│     │ • Secure comparison                    │         │
│     └────────────────────────────────────────┘         │
│                                                         │
│  5. Database Security (SQLAlchemy)                     │
│     ┌────────────────────────────────────────┐         │
│     │ • ORM prevents SQL injection           │         │
│     │ • Parameterized queries                │         │
│     │ • Connection pooling                   │         │
│     │ • Environment-based credentials        │         │
│     └────────────────────────────────────────┘         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌───────────────────────────────────────────────────────────┐
│                   Production Stack                        │
└───────────────────────────────────────────────────────────┘

┌─────────────┐
│   Nginx     │  ← Reverse Proxy & Load Balancer
│  (Port 80)  │  • SSL/TLS termination
└──────┬──────┘  • Rate limiting
       │         • Static file serving
       │
       ├─────────────────────┬─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Uvicorn    │      │  Uvicorn    │      │  Gunicorn   │
│  (FastAPI)  │      │  (FastAPI)  │      │   (Flask)   │
│  Instance 1 │      │  Instance 2 │      │   :5000     │
│    :8001    │      │    :8002    │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
       │                     │                     │
       └─────────────────────┴─────────────────────┘
                             │
                             ▼
                   ┌─────────────────┐
                   │   PostgreSQL    │
                   │  (Primary DB)   │
                   │  Connection     │
                   │  Pool: 20       │
                   └─────────────────┘
```

## File Structure Tree

```
backend/
│
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI entry point
│   │
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py             # Settings & env variables
│   │   └── security.py           # JWT & password hashing
│   │
│   ├── db/                       # Database configuration
│   │   ├── __init__.py
│   │   ├── base.py               # SQLAlchemy base & engine
│   │   └── session.py            # Session management
│   │
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── question.py           # Question model
│   │   ├── practice.py           # Practice models
│   │   └── test.py               # Test models
│   │
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py               # User schemas
│   │   ├── question.py           # Question schemas
│   │   ├── practice.py           # Practice schemas
│   │   └── test.py               # Test schemas
│   │
│   ├── api/                      # FastAPI routers
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication (4 endpoints)
│   │   ├── questions.py          # Questions (2 endpoints)
│   │   ├── practice.py           # Practice (3 endpoints)
│   │   ├── tests.py              # Tests (3 endpoints)
│   │   └── health.py             # Health check (1 endpoint)
│   │
│   ├── services/                 # Business logic (placeholder)
│   │
│   └── admin/                    # Flask admin (placeholder)
│       └── __init__.py
│
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   │   └── .gitkeep
│   ├── env.py                    # Alembic environment
│   └── script.py.mako            # Migration template
│
├── scripts/                      # Utility scripts
│   ├── seed_questions.py         # Seed 33 SAT questions
│   └── sample_questions.csv      # CSV import template
│
├── flask_app.py                  # Flask entry point
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
│
├── setup.bat                     # Setup automation
├── start_servers.bat             # Server startup
├── test_installation.bat         # Installation test
│
└── Documentation/
    ├── README.md                 # Main documentation
    ├── QUICKSTART.md             # Quick start guide
    ├── IMPLEMENTATION_SUMMARY.md # Implementation details
    ├── MIGRATIONS.md             # Migration guide
    ├── CHECKLIST.md              # Implementation checklist
    └── ARCHITECTURE.md           # This file
```

---

**Created**: January 24, 2026  
**Status**: Production-Ready  
**Version**: 1.0.0  

*EduNexus SAT Practice Platform Backend*
