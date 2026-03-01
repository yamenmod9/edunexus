# EduNexus Backend - Score Calculator

## Quick Start

### Start Server (Easy Way)
```bash
START_BACKEND.bat
```

### Start Server (Manual)
```bash
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

### Run Tests
```bash
python test_score_calculator.py
```

### API Documentation
http://localhost:8000/docs

## Score Calculator Endpoints

### Calculate Score (No Auth Required)
```bash
curl -X POST http://localhost:8000/api/scores/calculate \
  -H "Content-Type: application/json" \
  -d '{"reading_correct": 45, "writing_correct": 38, "math_correct": 50}'
```

### Save Score (Auth Required)
```bash
curl -X POST http://localhost:8000/api/scores/save \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reading_correct": 45,
    "writing_correct": 38,
    "math_correct": 50,
    "reading_writing_score": 680,
    "math_score": 720,
    "total_score": 1400,
    "percentile": 93,
    "notes": "Practice test"
  }'
```

### Get Score History
```bash
curl http://localhost:8000/api/scores/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Score Statistics
```bash
curl http://localhost:8000/api/scores/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Score Calculation

### SAT Score Ranges
- **Reading + Writing:** 200-800 (combined)
- **Math:** 200-800
- **Total:** 400-1600

### Question Counts
- **Reading:** 52 questions
- **Writing:** 44 questions
- **Math:** 58 questions

### Percentiles
- 1st-99th percentile based on College Board data

## Files

### Core Files
- `app/utils/score_calculator.py` - Calculation engine
- `app/models/score.py` - Database model
- `app/schemas/score.py` - API schemas
- `app/api/scores.py` - API endpoints

### Testing
- `test_score_calculator.py` - Test suite

### Startup
- `START_BACKEND.bat` - Easy startup script

## Database

### Migration
```bash
alembic upgrade head
```

### Create New Migration
```bash
alembic revision --autogenerate -m "description"
```

## Documentation

See parent directory:
- `STEP_9_FINAL_COMPLETE.md` - Complete guide
- `SCORE_CALCULATOR_API_REFERENCE.md` - API docs
- `STEP_9B_FRONTEND_CHECKLIST.md` - Frontend guide

## Status

✅ **Backend: PRODUCTION READY**  
✅ **All Tests: PASSING (5/5)**  
✅ **API: FULLY FUNCTIONAL**
