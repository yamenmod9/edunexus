# Database Migration Guide

## Overview

This project uses **Alembic** for unified database migrations shared between FastAPI and Flask.

## Initial Setup

### 1. Create Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE edunexus;

-- Verify
\l
```

### 2. Configure Database URL

Update `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/edunexus
```

### 3. Run Initial Migration

```cmd
cd C:\Programming\Flutter\edunexus\backend
venv\Scripts\activate
alembic upgrade head
```

This creates all tables:
- users
- questions
- practice_sessions
- attempts
- tests
- test_attempts

## Common Migration Commands

### Check Current Version
```cmd
alembic current
```

### View Migration History
```cmd
alembic history --verbose
```

### Create New Migration (Auto-generate)
```cmd
alembic revision --autogenerate -m "Add new field to User table"
```

### Apply Migrations
```cmd
alembic upgrade head
```

### Rollback One Migration
```cmd
alembic downgrade -1
```

### Rollback to Specific Version
```cmd
alembic downgrade <revision_id>
```

### Mark Current Database State (Without Running)
```cmd
alembic stamp head
```

## Adding New Models

### Step 1: Create Model

Create new model in `app/models/`:

```python
# app/models/example.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
```

### Step 2: Register Model

Add to `app/models/__init__.py`:

```python
from app.models.example import Example

__all__ = [
    # ... existing exports
    "Example",
]
```

### Step 3: Import in Alembic

Add to `alembic/env.py`:

```python
from app.models import (
    User,
    Question,
    # ... existing imports
    Example,  # Add new model
)
```

### Step 4: Generate Migration

```cmd
alembic revision --autogenerate -m "Add Example table"
```

Review the generated file in `alembic/versions/`.

### Step 5: Apply Migration

```cmd
alembic upgrade head
```

## Modifying Existing Models

### Step 1: Modify Model

```python
# app/models/user.py
class User(Base):
    # ... existing fields
    phone_number = Column(String(20), nullable=True)  # New field
```

### Step 2: Generate Migration

```cmd
alembic revision --autogenerate -m "Add phone_number to User"
```

### Step 3: Review Generated Migration

Check `alembic/versions/<revision>_add_phone_number_to_user.py`:

```python
def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone_number')
```

### Step 4: Apply Migration

```cmd
alembic upgrade head
```

## Manual Migrations

Sometimes auto-generate doesn't work perfectly. Create manual migration:

```cmd
alembic revision -m "Custom migration"
```

Edit the generated file:

```python
def upgrade():
    # Custom SQL or operations
    op.execute("""
        UPDATE users 
        SET is_active = true 
        WHERE is_active IS NULL
    """)

def downgrade():
    # Reverse operation
    pass
```

## Migration Best Practices

### 1. Always Review Auto-Generated Migrations
- Alembic may miss renames (shows as drop + add)
- Check for data loss operations
- Verify indexes and constraints

### 2. Test Migrations
```cmd
# Test upgrade
alembic upgrade head

# Test downgrade
alembic downgrade -1

# Test upgrade again
alembic upgrade head
```

### 3. Backup Before Production Migrations
```bash
pg_dump -U postgres edunexus > backup_$(date +%Y%m%d).sql
```

### 4. Use Descriptive Messages
```cmd
# Good
alembic revision --autogenerate -m "Add email_verified field to User table"

# Bad
alembic revision --autogenerate -m "Update"
```

### 5. Keep Migrations Linear
- Avoid branching (multiple heads)
- Use `alembic merge` if branches occur

## Troubleshooting

### Problem: "Target database is not up to date"

**Solution:**
```cmd
alembic current
alembic upgrade head
```

### Problem: "Can't locate revision identified by 'abc123'"

**Solution:**
```cmd
# Check history
alembic history

# Stamp current state
alembic stamp head
```

### Problem: Auto-generate creates empty migration

**Solution:**
- Ensure models are imported in `alembic/env.py`
- Check that `target_metadata = Base.metadata` is set
- Verify database connection

### Problem: Migration fails halfway

**Solution:**
```cmd
# Check current state
alembic current

# Downgrade to known good state
alembic downgrade <previous_revision>

# Fix migration file
# Re-run upgrade
alembic upgrade head
```

### Problem: "Multiple heads detected"

**Solution:**
```cmd
# List heads
alembic heads

# Merge branches
alembic merge -m "Merge branches" <head1> <head2>

# Upgrade
alembic upgrade head
```

## Seeding Data After Migrations

After running migrations, seed the database:

```cmd
python scripts\seed_questions.py
```

## Checking Migration Status

### From Python
```python
from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")
command.current(alembic_cfg)
```

### From Application Startup

Add to `app/main.py`:

```python
from alembic.config import Config
from alembic import command

def check_migrations():
    """Check if migrations are up to date."""
    try:
        alembic_cfg = Config("alembic.ini")
        command.current(alembic_cfg, verbose=False)
        return True
    except Exception as e:
        print(f"Migration check failed: {e}")
        return False

# In startup event
@app.on_event("startup")
async def startup_event():
    if not check_migrations():
        print("⚠️  WARNING: Database migrations may not be up to date")
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] Backup production database
- [ ] Test migrations on staging environment
- [ ] Review all migration files
- [ ] Check for data loss operations
- [ ] Verify rollback procedures
- [ ] Document any manual steps

### Deployment Steps

1. **Backup Database**
   ```bash
   pg_dump -U user dbname > backup_pre_migration.sql
   ```

2. **Stop Application**
   ```bash
   systemctl stop edunexus-api
   systemctl stop edunexus-admin
   ```

3. **Run Migrations**
   ```bash
   cd /path/to/backend
   source venv/bin/activate
   alembic upgrade head
   ```

4. **Verify Migration**
   ```bash
   alembic current
   psql -U user dbname -c "\d users"  # Check table structure
   ```

5. **Start Application**
   ```bash
   systemctl start edunexus-api
   systemctl start edunexus-admin
   ```

6. **Verify Application**
   ```bash
   curl http://localhost:8000/api/health
   ```

### Rollback Procedure

If migration fails:

```bash
# Restore database
psql -U user dbname < backup_pre_migration.sql

# Or rollback migration
alembic downgrade -1

# Restart application with old code
systemctl start edunexus-api
```

## Migration Workflow Summary

```
┌─────────────────────────────────────────┐
│  1. Modify SQLAlchemy Model             │
│     (app/models/*.py)                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  2. Import Model in alembic/env.py      │
│     (if new model)                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  3. Generate Migration                  │
│     alembic revision --autogenerate     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  4. Review Generated File               │
│     alembic/versions/<rev>_*.py         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  5. Apply Migration                     │
│     alembic upgrade head                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  6. Verify in Database                  │
│     psql / pgAdmin                      │
└─────────────────────────────────────────┘
```

## Reference

- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

*Last Updated: January 24, 2026*
*EduNexus Backend Migration Guide*
