# EduNexus Backend

SAT Practice Platform Backend - Hybrid FastAPI + Flask Architecture

## Architecture Overview

This backend uses a **hybrid architecture**:

- **FastAPI** (Port 8000): REST API for mobile/web clients
- **Flask** (Port 5000): Admin dashboard and health monitoring
- **PostgreSQL**: Shared database
- **SQLAlchemy**: Shared ORM and models
- **Alembic**: Unified database migrations

## Project Structure

```
backend/
├── app/
│   ├── core/              # Configuration and security
│   │   ├── config.py      # Settings and environment variables
│   │   └── security.py    # JWT and password hashing
│   ├── db/                # Database setup
│   │   ├── base.py        # SQLAlchemy base and engine
│   │   └── session.py     # Session management
│   ├── models/            # SQLAlchemy models
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── practice.py
│   │   └── test.py
│   ├── schemas/           # Pydantic schemas
│   │   ├── user.py
│   │   ├── question.py
│   │   ├── practice.py
│   │   └── test.py
│   ├── api/               # FastAPI routers
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── questions.py   # Question bank endpoints
│   │   ├── practice.py    # Practice mode endpoints
│   │   ├── tests.py       # Test mode endpoints
│   │   └── health.py      # Health check endpoint
│   ├── admin/             # Flask admin (placeholder)
│   └── main.py            # FastAPI application entry
├── alembic/               # Database migrations
│   ├── versions/          # Migration scripts
│   └── env.py             # Alembic environment
├── scripts/
│   └── seed_questions.py  # Sample data seeding
├── flask_app.py           # Flask application entry
├── alembic.ini            # Alembic configuration
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Virtual environment tool (venv)

### 2. Environment Setup

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/edunexus
SECRET_KEY=your-super-secret-key-min-32-characters
```

### 4. Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE edunexus;
```

Run migrations:

```cmd
alembic upgrade head
```

### 5. Seed Sample Data

```cmd
python scripts\seed_questions.py
```

This creates 30+ sample SAT questions across Math, Reading, and Writing sections.

### 6. Run Servers

**Terminal 1 - FastAPI (REST API):**
```cmd
venv\Scripts\activate
python app\main.py
```

Access at: http://localhost:8000
API Docs: http://localhost:8000/docs

**Terminal 2 - Flask (Admin Dashboard):**
```cmd
venv\Scripts\activate
python flask_app.py
```

Access at: http://localhost:5000
Health Dashboard: http://localhost:5000/admin/health

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT tokens |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user info |

### Questions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/questions` | Get questions with filters |
| GET | `/api/questions/{id}` | Get specific question |

**Query Parameters:**
- `section`: math, reading, writing
- `topic`: Algebra, Geometry, etc.
- `subtopic`: Linear Equations, etc.
- `difficulty`: easy, medium, hard
- `shuffle`: true/false
- `limit`: 1-100

### Practice Mode

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/practice/session/start` | Start practice session |
| POST | `/api/practice/attempt` | Submit answer attempt |
| GET | `/api/practice/history` | Get practice history |

### Test Mode

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tests/generate` | Generate new test |
| POST | `/api/tests/submit` | Submit completed test |
| GET | `/api/tests/history` | Get test history |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API and database status |

## Flask Admin Endpoints

### Health Dashboard

- **GET** `/admin/health` - Visual health monitoring dashboard
  - Shows FastAPI status
  - Database connectivity
  - System timestamp
  - Auto-refreshes every 30 seconds

### Question Import

- **POST** `/admin/questions/import` - Import questions from CSV/JSON

**CSV Format:**
```csv
section,topic,subtopic,difficulty,question_text,choice_a,choice_b,choice_c,choice_d,correct_answer,explanation
math,Algebra,Linear Equations,easy,"If 2x = 10, what is x?",3,5,7,10,B,"2x = 10, so x = 5"
```

**JSON Format:**
```json
[
  {
    "section": "math",
    "topic": "Algebra",
    "subtopic": "Linear Equations",
    "difficulty": "easy",
    "question_text": "If 2x = 10, what is x?",
    "choices": ["3", "5", "7", "10"],
    "correct_answer": "B",
    "explanation": "2x = 10, so x = 5"
  }
]
```

## Question Data Contract

### Required Fields

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| section | string | Question section | Enum: "math", "reading", "writing" |
| topic | string | Main topic | Max 100 chars |
| subtopic | string | Subtopic (optional) | Max 100 chars |
| difficulty | string | Difficulty level | Enum: "easy", "medium", "hard" |
| question_text | string | Question text | Required, non-empty |
| choices | array | Answer choices | Exactly 4 non-empty strings |
| correct_answer | string | Correct answer | Enum: "A", "B", "C", "D" |
| explanation | string | Explanation (optional) | Text |

### Validation Rules

1. **Choices**: Must be exactly 4 non-empty strings
2. **Correct Answer**: Must be A, B, C, or D
3. **Section**: Must be one of the allowed enums
4. **Difficulty**: Must be one of the allowed enums

## Database Models

### User
- `id`: Primary key
- `email`: Unique email address
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `created_at`: Registration timestamp

### Question
- `id`: Primary key
- `section`: math | reading | writing
- `topic`: Main topic
- `subtopic`: Optional subtopic
- `difficulty`: easy | medium | hard
- `question_text`: Question content
- `choices`: JSON array of 4 strings
- `correct_answer`: A | B | C | D
- `explanation`: Optional explanation
- `created_at`: Creation timestamp

### PracticeSession
- `id`: Primary key
- `user_id`: Foreign key to User
- `topics`: Comma-separated topic list
- `started_at`: Session start time
- `ended_at`: Session end time (nullable)

### Attempt
- `id`: Primary key
- `session_id`: Foreign key to PracticeSession
- `question_id`: Foreign key to Question
- `user_answer`: User's answer (A-D)
- `is_correct`: Boolean correctness
- `time_spent`: Time in seconds
- `attempted_at`: Timestamp

### Test
- `id`: Primary key
- `user_id`: Foreign key to User
- `test_type`: Test type identifier
- `questions`: JSON array of question IDs
- `started_at`: Test start time
- `submitted_at`: Test submission time (nullable)
- `score`: Calculated score (nullable)

### TestAttempt
- `id`: Primary key
- `test_id`: Foreign key to Test
- `question_id`: Foreign key to Question
- `user_answer`: User's answer (nullable)
- `is_correct`: Boolean correctness (nullable)
- `time_spent`: Time in seconds (nullable)
- `answered_at`: Answer timestamp (nullable)

## Database Migrations

### Create Migration

```cmd
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```cmd
alembic upgrade head
```

### Rollback Migration

```cmd
alembic downgrade -1
```

### Check Current Version

```cmd
alembic current
```

## Authentication Flow

1. **Register**: POST `/api/auth/register` with email and password
2. **Login**: POST `/api/auth/login` → Returns access_token and refresh_token
3. **Use API**: Include `Authorization: Bearer {access_token}` header
4. **Refresh**: POST `/api/auth/refresh` with refresh_token when access expires
5. **Get User**: GET `/api/auth/me` with valid access_token

## Development Guidelines

### Adding New Endpoints

1. Create router in `app/api/`
2. Define Pydantic schemas in `app/schemas/`
3. Include router in `app/main.py`
4. Test with FastAPI docs at `/docs`

### Adding New Models

1. Create model in `app/models/`
2. Import in `app/models/__init__.py`
3. Import in `alembic/env.py`
4. Generate migration: `alembic revision --autogenerate`
5. Apply migration: `alembic upgrade head`

### Running Tests

```cmd
pytest
```

## Troubleshooting

### Database Connection Error

- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database exists: `CREATE DATABASE edunexus;`

### Migration Errors

- Check all models are imported in `alembic/env.py`
- Verify database is empty or current with migrations
- Use `alembic stamp head` to mark current state

### Import Errors

- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check PYTHONPATH includes backend directory

## Production Deployment

### Security Checklist

- [ ] Change SECRET_KEY to strong random string (min 32 chars)
- [ ] Set ENVIRONMENT=production
- [ ] Use strong database password
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS allowed origins
- [ ] Set up rate limiting
- [ ] Enable database backups
- [ ] Use environment variables (not .env file)

### Recommended Stack

- **Web Server**: Nginx
- **ASGI Server**: Uvicorn with Gunicorn
- **WSGI Server**: Gunicorn (for Flask)
- **Database**: PostgreSQL with connection pooling
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or CloudWatch

## License

Proprietary - EduNexus SAT Practice Platform

## Support

For issues or questions, contact the development team.
