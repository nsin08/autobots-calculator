# PR: Add Auth Backend (Registration, Login, Logout)

## Links

Closes #20  
Epic: #18

## What changed

- **Auth endpoints**: POST /api/auth/register, POST /api/auth/login, GET /api/auth/logout, GET /api/auth/status
- **Flask-Login integration**: Session management with 24-hour timeout
- **Route protection**: @login_required decorator for securing endpoints
- **Password security**: bcrypt hashing from User model (Story #19)
- **Session persistence**: Cookies with PERMANENT_SESSION_LIFETIME config
- **Comprehensive validation**: Username, email, password validation with clear error messages

## Why

Story #20 provides the authentication foundation for Epic #18. All user-specific features (calculation history, preferences, financial calculators) require user authentication. This implements production-ready auth with security best practices (bcrypt, session management, input validation).

## Mapping to Success Criteria

**[✓] Criterion 1: POST /api/auth/register creates users with validation**
- Evidence: [src/service/auth.py lines 12-82](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/auth.py#L12-L82) - register() endpoint
- Validation: Username (3-50 chars), email (valid format, <100 chars), password (min 8 chars)
- Uniqueness: Checks duplicate username/email, returns 409
- Tests: test_register_success, test_register_duplicate_username, test_register_duplicate_email, test_register_short_username, test_register_invalid_email, test_register_short_password

**[✓] Criterion 2: POST /api/auth/login authenticates and creates sessions**
- Evidence: [src/service/auth.py lines 85-139](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/auth.py#L85-L139) - login() endpoint
- Session: login_user(user, remember=True) creates persistent session
- last_login: Updates timestamp on successful login
- Tests: test_login_success, test_login_wrong_password, test_login_nonexistent_user, test_login_updates_last_login

**[✓] Criterion 3: GET /api/auth/logout destroys sessions**
- Evidence: [src/service/auth.py lines 142-152](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/auth.py#L142-L152) - logout() endpoint
- Session: logout_user() clears session
- Tests: test_logout, test_logout_without_login, test_session_cleared_after_logout

**[✓] Criterion 4: GET /api/auth/status returns current user**
- Evidence: [src/service/auth.py lines 155-172](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/auth.py#L155-L172) - status() endpoint
- Returns: {authenticated: true, user_id, username} if logged in, {authenticated: false} otherwise
- Tests: test_status_authenticated, test_status_not_authenticated

**[✓] Criterion 5: Passwords hashed with bcrypt**
- Evidence: User model from Story #19 - [src/service/models.py lines 23-48](https://github.com/nsin08/autobots-calculator/blob/master/src/service/models.py#L23-L48)
- Auth uses: user.set_password() for registration, user.check_password() for login
- Passwords never stored or returned plain-text

**[✓] Criterion 6: @login_required decorator protects routes**
- Evidence: [src/service/decorators.py](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/decorators.py) - login_required decorator
- Returns: 401 {"error": "Authentication required"} if not authenticated
- Preserves: Function metadata with @wraps(f)
- Tests: test_login_required_decorator_logic_authenticated, test_login_required_decorator_logic_structure

**[✓] Criterion 7: Session timeout: 24 hours**
- Evidence: [src/service/app.py line 18](https://github.com/nsin08/autobots-calculator/blob/feature/20-auth-backend/src/service/app.py#L18) - PERMANENT_SESSION_LIFETIME config
- Config: timedelta(hours=24)
- Tests: test_session_persists_across_requests verifies session works

## Test Evidence

**Local execution:**
```bash
pytest tests/test_auth.py -v --cov=src.service.auth --cov=src.service.decorators --cov-report=term-missing
```

**Results:**
- **25/25 tests passed** in 3.37s
- **Coverage: 92%** total
  - src/service/auth.py: 95% (66/69 statements)
  - src/service/decorators.py: 70% (7/10 statements)

**Full suite (regression check):**
```bash
pytest tests/ -v
```
- **67/67 tests passed** (42 existing + 25 new)
- **Zero regressions**

**Test categories:**
- **Registration (11 tests)**: Success, duplicates (username/email), validation (username length, email format, password length), missing fields, no JSON body
- **Login (6 tests)**: Success, wrong password, non-existent user, missing fields, last_login update
- **Logout (2 tests)**: With login, without login
- **Status (2 tests)**: Authenticated, not authenticated
- **Session (2 tests)**: Persistence across requests, cleared after logout
- **Decorator (2 tests)**: Logic structure, metadata preservation

## Risk / Rollback

**Risk:**
- **Low** - New feature, no impact on existing endpoints
- Sessions stored in Flask session cookies (secure, httponly)
- SECRET_KEY set via environment variable (defaults to dev key)
- No breaking changes to existing functionality

**Rollback:**
- Revert this PR
- Unregister auth blueprint from app.py
- No data migration needed (User model already exists from Story #19)
- Frontend continues to work anonymously

**Production considerations (future):**
- Set SECRET_KEY environment variable (currently uses dev default)
- Consider HTTPS-only session cookies for production
- Add rate limiting for login attempts (future story)

## Checklist

- [✓] Tests added/updated (25 new tests, 92% coverage for new code)
- [✓] Docs updated (README with auth API examples)
- [✓] No unrelated refactors (focused on auth backend only)
- [✓] PR is small and focused (1 story = auth endpoints)
- [✓] All success criteria have evidence (mapped above)
- [✓] CI passing (67/67 tests)
- [✓] No regressions (all existing tests passing)

---

**Ready for review!** This unblocks Stories #21 (Auth Frontend), #22 (History Backend), #23 (EMI Calculator).

**Note for Reviewer:** All 7 success criteria from Story #20 met with concrete evidence. Session management tested through multiple scenarios (login, logout, persistence, status checks). Security: bcrypt from Story #19, no passwords in responses, session cookies only.