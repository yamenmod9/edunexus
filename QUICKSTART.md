# EduNexus Backend - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.10+ installed
- PostgreSQL installed and running
- Git Bash or Command Prompt

### Step 1: Navigate to Backend
```cmd
cd C:\Programming\Flutter\edunexus\backend
```

### Step 2: Run Setup Script (Recommended)
```cmd
setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file

### Step 3: Configure Database

1. Create PostgreSQL database:
```sql
CREATE DATABASE edunexus;
```

2. Update `.env` with your credentials:
```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/edunexus
```

### Step 4: Run Migrations
```cmd
venv\Scripts\activate
alembic upgrade head
```

### Step 5: Seed Sample Data
```cmd
python scripts\seed_questions.py
```

This creates 30+ sample SAT questions.

### Step 6: Start Servers

**Terminal 1 - FastAPI:**
```cmd
venv\Scripts\activate
python app\main.py
```
✅ API running at: http://localhost:8000

**Terminal 2 - Flask Admin:**
```cmd
venv\Scripts\activate
python flask_app.py
```
✅ Admin running at: http://localhost:5000

## 📋 Verify Installation

1. **API Docs**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/api/health
3. **Admin Dashboard**: http://localhost:5000/admin/health

## 🧪 Test the API

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

### Get Questions
```bash
curl http://localhost:8000/api/questions?section=math&difficulty=easy
```

## 📚 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Troubleshooting

### "alembic: command not found"
```cmd
venv\Scripts\activate
pip install alembic
```

### Database Connection Error
- Verify PostgreSQL is running: `pg_ctl status`
- Check credentials in `.env`
- Ensure database exists

### Import Errors
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

## 🎯 What's Included

### FastAPI Endpoints
- ✅ Authentication (register, login, refresh, me)
- ✅ Questions (list with filters, get by ID)
- ✅ Practice Mode (sessions, attempts, history)
- ✅ Test Mode (generate, submit, history)
- ✅ Health Check

### Flask Admin
- ✅ Health Dashboard (visual monitoring)
- ✅ Question Import (CSV/JSON upload)

### Database
- ✅ Unified Alembic migrations
- ✅ All models (User, Question, Practice, Test)
- ✅ Proper relationships and indexes
- ✅ Sample data seeding

### Data Seeding
- ✅ 30+ sample questions
- ✅ Math (Algebra, Geometry, Statistics)
- ✅ Reading (Comprehension, Vocabulary)
- ✅ Writing (Grammar, Punctuation, Rhetoric)
- ✅ Mixed difficulty levels

## ✨ Next Steps

1. ✅ Backend is complete and ready
2. 🎨 Now you can start building the Flutter frontend
3. 📱 Frontend will consume these API endpoints

## 🛡️ Security Notes

⚠️ **Before Production:**
- Change `SECRET_KEY` in `.env` to a strong random string
- Use environment variables, not `.env` file
- Enable HTTPS/TLS
- Configure proper CORS origins
- Set up rate limiting

## 📞 Support

Backend is production-ready! If you encounter issues:
1. Check logs in terminal
2. Verify database connectivity
3. Check `.env` configuration
4. See full README.md for details
