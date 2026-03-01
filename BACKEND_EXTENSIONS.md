# Backend Extension Implementation Guide

## Overview
This document describes the comprehensive backend extensions for the SAT Practice Platform, including dashboard analytics, question bank restructure, bookmarks, score prediction, and question import pipeline.

## Database Schema Changes

### New Tables

#### 1. **bookmarks**
Stores user-bookmarked questions for later review.

```sql
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    created_at TIMESTAMP NOT NULL,
    UNIQUE(user_id, question_id)
);
```

#### 2. **daily_statistics**
Aggregated daily performance metrics for dashboard.

```sql
CREATE TABLE daily_statistics (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    date DATE NOT NULL,
    questions_attempted INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    questions_incorrect INTEGER DEFAULT 0,
    math_attempted INTEGER DEFAULT 0,
    math_correct INTEGER DEFAULT 0,
    english_attempted INTEGER DEFAULT 0,
    english_correct INTEGER DEFAULT 0,
    total_time_spent FLOAT DEFAULT 0,
    tests_completed INTEGER DEFAULT 0,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(user_id, date)
);
```

#### 3. **mistake_logs**
Tracks incorrect answers for mistake review feature.

```sql
CREATE TABLE mistake_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    user_answer VARCHAR(1) NOT NULL,
    attempted_at TIMESTAMP NOT NULL,
    source_type VARCHAR(20) NOT NULL,  -- 'practice' or 'test'
    source_id INTEGER NOT NULL,
    reviewed BOOLEAN DEFAULT false,
    reviewed_at TIMESTAMP NULL,
    time_spent FLOAT NULL
);
```

#### 4. **score_predictions**
Stores SAT score predictions based on performance.

```sql
CREATE TABLE score_predictions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    predicted_total_score INTEGER NOT NULL,  -- 400-1600
    predicted_math_score INTEGER NOT NULL,   -- 200-800
    predicted_english_score INTEGER NOT NULL,  -- 200-800
    confidence_level FLOAT NOT NULL,  -- 0.0 to 1.0
    sample_size INTEGER NOT NULL,
    easy_accuracy FLOAT NULL,
    medium_accuracy FLOAT NULL,
    hard_accuracy FLOAT NULL,
    created_at TIMESTAMP NOT NULL,
    calculation_method VARCHAR(50) NOT NULL
);
```

### Extended Tables

#### **users** (new columns)
```sql
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);
ALTER TABLE users ADD COLUMN sat_exam_date DATE;
ALTER TABLE users ADD COLUMN target_score INTEGER;
```

#### **questions** (new columns)
```sql
ALTER TABLE questions ADD COLUMN category VARCHAR(100);
ALTER TABLE questions ADD COLUMN subcategory VARCHAR(100);
ALTER TABLE questions ADD COLUMN is_bluebook BOOLEAN DEFAULT false;
ALTER TABLE questions ADD COLUMN passage_text TEXT;
ALTER TABLE questions ADD COLUMN source_attribution VARCHAR(200);
ALTER TABLE questions ALTER COLUMN topic DROP NOT NULL;
```

## SAT English Hierarchy

The question bank now supports SAT-accurate English taxonomy:

### **Craft and Structure**
- Cross-Text Connections
- Text Structure and Purpose
- Words in Context

### **Expression of Ideas**
- Rhetorical Synthesis
- Transitions

### **Information and Ideas**
- Central Ideas and Details
- Command of Evidence
- Inferences

### **Standard English Conventions**
- Boundaries
- Form, Structure, and Sense

## New API Endpoints

### Dashboard Endpoints

#### `GET /api/dashboard/stats`
Get comprehensive dashboard statistics.

**Response:**
```json
{
  "questions_solved_today": 15,
  "correct_today": 12,
  "incorrect_today": 3,
  "time_spent_today": 45.5,
  "total_questions_solved": 250,
  "total_correct": 200,
  "total_incorrect": 50,
  "overall_accuracy": 80.0,
  "math_accuracy": 75.0,
  "english_accuracy": 85.0,
  "math_total": 120,
  "english_total": 130,
  "bookmarked_count": 10,
  "tests_completed": 3,
  "sat_exam_date": "2026-06-15",
  "days_until_exam": 142,
  "target_score": 1400,
  "recent_accuracy": 82.5,
  "recent_questions_count": 75
}
```

#### `GET /api/dashboard/performance-graph?days=7`
Get time-series performance data.

**Query Parameters:**
- `days`: 7, 30, or 90

**Response:**
```json
{
  "daily_performance": [
    {
      "date": "2026-01-25",
      "questions_attempted": 15,
      "accuracy": 80.0,
      "math_accuracy": 75.0,
      "english_accuracy": 85.0
    }
  ],
  "period_days": 7
}
```

#### `GET /api/dashboard/error-logs?days=30&limit=100`
Get mistake logs grouped by date.

**Response:**
```json
[
  {
    "date": "2026-01-25",
    "mistakes": [
      {
        "question_id": 123,
        "question_text": "Which of the following...",
        "section": "english",
        "category": "craft_and_structure",
        "subcategory": "words_in_context",
        "difficulty": "hard",
        "user_answer": "B",
        "correct_answer": "C",
        "attempted_at": "2026-01-25T14:30:00",
        "source_type": "practice",
        "reviewed": false
      }
    ],
    "total_mistakes": 3
  }
]
```

#### `GET /api/dashboard/category-performance?section=english`
Get performance breakdown by category.

**Response:**
```json
[
  {
    "category": "information_and_ideas",
    "subcategory": "central_ideas_and_details",
    "total_questions": 25,
    "correct": 20,
    "accuracy": 80.0,
    "difficulty_breakdown": {
      "easy": 0.95,
      "medium": 0.80,
      "hard": 0.60
    }
  }
]
```

#### `GET /api/dashboard/score-prediction?recalculate=false`
Get SAT score prediction.

**Response:**
```json
{
  "predicted_total_score": 1380,
  "predicted_math_score": 680,
  "predicted_english_score": 700,
  "confidence_level": 0.85,
  "sample_size": 200,
  "easy_accuracy": 0.95,
  "medium_accuracy": 0.80,
  "hard_accuracy": 0.65,
  "created_at": "2026-01-25T10:00:00",
  "calculation_method": "weighted_accuracy",
  "strengths": ["Information And Ideas", "Standard English Conventions"],
  "weaknesses": ["Craft And Structure"],
  "recommended_study_areas": [
    "Focus on Craft and Structure questions",
    "Practice more challenging Math problems"
  ]
}
```

#### `POST /api/dashboard/update-daily-stats`
Manually trigger daily statistics update.

#### `POST /api/dashboard/mistakes/{mistake_id}/mark-reviewed`
Mark a mistake as reviewed.

### Bookmark Endpoints

#### `POST /api/bookmarks/`
Create a bookmark.

**Request:**
```json
{
  "question_id": 123
}
```

#### `GET /api/bookmarks/`
Get all bookmarks with question details.

#### `DELETE /api/bookmarks/{bookmark_id}`
Delete a bookmark.

#### `DELETE /api/bookmarks/question/{question_id}`
Delete bookmark by question ID.

#### `GET /api/bookmarks/check/{question_id}`
Check if question is bookmarked.

### Question Import Endpoints

#### `POST /api/admin/questions/import/csv`
Import questions from CSV file.

**Form Data:**
- `file`: CSV file

**Response:**
```json
{
  "success": true,
  "message": "Successfully imported 50 questions",
  "success_count": 50,
  "error_count": 2,
  "errors": [
    {
      "row": 15,
      "error": "Invalid difficulty: super_hard",
      "data": {...}
    }
  ]
}
```

#### `POST /api/admin/questions/import/json`
Import questions from JSON file.

#### `GET /api/admin/questions/import/template/csv`
Download CSV import template.

#### `GET /api/admin/questions/import/template/json`
Download JSON import template.

#### `GET /api/admin/questions/validation-rules`
Get import validation rules.

## Services

### AnalyticsService

Located in `app/services/analytics.py`

**Methods:**
- `get_dashboard_stats(db, user_id)` - Get comprehensive dashboard stats
- `get_performance_graph_data(db, user_id, days)` - Get time-series data
- `get_error_logs(db, user_id, days, limit)` - Get mistake logs
- `get_category_performance(db, user_id, section)` - Get category breakdown
- `update_daily_statistics(db, user_id, date)` - Update/create daily stats
- `log_mistake(db, user_id, question_id, ...)` - Log incorrect answer

### ScorePredictionService

Located in `app/services/score_prediction.py`

**Methods:**
- `calculate_score_prediction(db, user_id)` - Calculate new prediction
- `get_latest_prediction(db, user_id)` - Get cached prediction

**Algorithm:**
- Uses weighted accuracy (easy=1.0, medium=1.5, hard=2.0)
- Converts accuracy to SAT scores using simplified curve
- Identifies strengths/weaknesses by category
- Generates personalized recommendations

### QuestionImporter

Located in `app/services/question_importer.py`

**Methods:**
- `import_from_csv(csv_content, db)` - Import from CSV
- `import_from_json(json_content, db)` - Import from JSON
- `get_csv_template()` - Generate CSV template
- `get_json_template()` - Generate JSON template

**Validation:**
- Required fields validation
- Section/difficulty/answer enum validation
- English category/subcategory hierarchy validation
- Duplicate prevention
- Detailed error reporting with row/item numbers

## Migration

Run the migration to apply schema changes:

```bash
cd backend
python -m alembic upgrade head
```

Migration file: `2a45f89bc123_add_dashboard_analytics_and_english_hierarchy.py`

## Integration Points

### Practice Session Flow
1. User answers question
2. System checks correctness
3. If incorrect → log to `mistake_logs`
4. Update `daily_statistics` for today
5. Return result to user

### Test Submission Flow
1. User submits test
2. System grades all answers
3. Log all mistakes to `mistake_logs`
4. Update `daily_statistics`
5. Optionally calculate score prediction
6. Return detailed results

### Daily Statistics Update
Called automatically after:
- Practice attempt submission
- Test submission
- Can also be triggered manually via API

### Score Prediction
- Auto-calculated on first request
- Cached for performance
- Can force recalculation with `recalculate=true`
- Recommended after significant practice (e.g., 50+ new questions)

## Question Import CSV Format

```csv
section,question_text,choice_a,choice_b,choice_c,choice_d,correct_answer,difficulty,category,subcategory,topic,subtopic,explanation,is_bluebook,passage_text,source_attribution
english,"Which of the following...","Option A","Option B","Option C","Option D",A,medium,information_and_ideas,central_ideas_and_details,Reading,Main Idea,"Because...",true,"Passage text...","Author, Work"
```

## Question Import JSON Format

```json
[
  {
    "section": "english",
    "question_text": "Which of the following...",
    "choices": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "A",
    "difficulty": "medium",
    "category": "information_and_ideas",
    "subcategory": "central_ideas_and_details",
    "topic": "Reading",
    "subtopic": "Main Idea",
    "explanation": "Because...",
    "is_bluebook": true,
    "passage_text": "Passage text...",
    "source_attribution": "Author, Work"
  }
]
```

## Security Considerations

### Authentication
- All dashboard/bookmark endpoints require Bearer token
- Token extracted from `Authorization` header
- Invalid/expired tokens return 401

### Admin Endpoints
- Question import currently requires authentication
- TODO: Add proper admin role check
- Consider rate limiting for bulk imports

### Data Privacy
- Users can only access their own data
- Mistake logs and bookmarks are user-scoped
- Statistics queries filtered by user_id

## Performance Optimizations

### Database Indexes
- Composite indexes on frequently queried columns
- `user_id + date` for daily statistics
- `user_id + attempted_at` for mistake logs
- `section + category + subcategory` for questions

### Caching Strategy
- Score predictions cached in database
- Daily statistics pre-aggregated
- Consider Redis for frequently accessed dashboard data

### Query Optimization
- Use joins to minimize database round-trips
- Aggregate queries using SQL functions
- Limit error logs to recent data (30 days default)

## Testing

### Manual Testing
1. Run backend: `python -m uvicorn app.main:app --reload`
2. Access API docs: `http://localhost:8000/docs`
3. Test each endpoint with sample data
4. Verify dashboard stats update after attempts

### Test Data
Use the question import feature to load sample questions:
1. Download CSV/JSON template
2. Fill with test data
3. Import via `/api/admin/questions/import/csv`

## Next Steps

1. **Frontend Integration** - Implement Flutter UI for dashboard
2. **Admin Panel** - Build admin interface for question management
3. **Advanced Analytics** - Add more detailed performance insights
4. **Score Prediction** - Refine algorithm with more data
5. **Caching Layer** - Add Redis for high-traffic endpoints
6. **Testing** - Write unit and integration tests
7. **Documentation** - Add API documentation with examples

## Breaking Changes

### Section Enum
- Old: `reading`, `writing` (separate)
- New: `english` (combined)
- Migration: Existing questions remain compatible
- Recommendation: Migrate old questions to `english` section

### Question Model
- `topic` field now nullable (use `category` for SAT taxonomy)
- New required field: `category` for English questions
- Consider data migration for existing questions

## Support

For questions or issues:
- Check API documentation at `/docs`
- Review error messages in import responses
- Verify database migration completed successfully
- Check logs for detailed error information
