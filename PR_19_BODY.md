# PR: Add Database Setup and User Model

## Links
Closes #19  
Epic: #18

## What changed
- Added SQLAlchemy integration with SQLite database
- Created User model with password hashing (bcrypt)
- Integrated Flask-Login UserMixin for authentication support
- Created test fixtures for in-memory testing
- Added 12 comprehensive tests for User model
- Updated dependencies (Flask-SQLAlchemy, Flask-Login, bcrypt)
- Updated README with database documentation
- Added database files to .gitignore

## Why
Story #19 is the foundation for Epic #18 - all auth, history, and user preference features require the database and User model. This implements the MVP database layer with production-ready patterns (ORM, password security, test fixtures).

## Mapping to Success Criteria

- [x] **Criterion 1:** SQLAlchemy configured with SQLite database
  - **Evidence:** `src/service/database.py` implements `init_db()` with SQLAlchemy configuration, SQLite URI, and auto table creation
  
- [x] **Criterion 2:** User model created with: id, username, email, password_hash, created_at, last_login
  - **Evidence:** `src/service/models.py` User class has all required fields with proper types and constraints (lines 12-18)
  
- [x] **Criterion 3:** Password hashing with bcrypt implemented
  - **Evidence:** `src/service/models.py` `set_password()` and `check_password()` methods use bcrypt (lines 20-39)
  
- [x] **Criterion 4:** Database initialization on app startup
  - **Evidence:** `src/service/app.py` calls `init_db(app)` on line 11, `database.py` calls `db.create_all()` in `init_db()` (line 19)
  
- [x] **Criterion 5:** Test fixtures with in-memory SQLite database
  - **Evidence:** `tests/conftest.py` provides `app`, `db`, `client`, and `test_user` fixtures with in-memory database (lines 9-51)
  
- [x] **Criterion 6:** Migration-ready structure (easy to switch to PostgreSQL later)
  - **Evidence:** Using SQLAlchemy ORM (database-agnostic), just change SQLALCHEMY_DATABASE_URI config to migrate

## Test Evidence

- **Local:** 
  ```bash
  pytest tests/test_models.py -v --cov=src.service.models --cov=src.service.database --cov-report=term-missing
  
  Results:
  - 12 tests passed (test_models.py)
  - Coverage: 100% for models.py and database.py (26/26 statements)
  - All existing tests still passing: 42/42 total tests passed
  ```

**Test Coverage Breakdown:**
- User creation and field validation
- Password hashing (not stored plain)
- Password verification (success + failure)
- Username uniqueness constraint
- Email uniqueness constraint  
- User queries (by username, by email)
- Last login timestamp updates
- Flask-Login UserMixin integration
- Database session management
- User repr method

## Risk / Rollback

**Risk:** 
- Low - New feature, no impact on existing endpoints
- Database file created on first run (calculator.db in project root)
- Migration from PostgreSQL later requires data migration script

**Rollback:** 
- Revert this PR
- Delete calculator.db file
- Downgrade dependencies: `pip install -r requirements.txt` from main branch
- No data loss (no users exist yet)

## Checklist
- [x] Tests added/updated (12 new tests, 100% coverage)
- [x] Docs updated (README with database setup section)
- [x] No unrelated refactors
- [x] PR is small and focused (1 story = database setup only)
- [x] All success criteria have evidence (mapped above)

---

**Ready for review!** This unblocks Stories #20-23 (auth backend, history, EMI calculator).
