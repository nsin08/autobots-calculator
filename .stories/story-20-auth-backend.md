# Story: Auth Backend (register/login/logout)

**Parent Epic:** #18  
**Sprint:** Sprint 1 (v0.3.0-alpha)  
**Depends on:** #19 (Database Setup)  
**Estimate:** 22 hours

## Success Criteria
- [ ] POST /api/auth/register creates users with validation
- [ ] POST /api/auth/login authenticates and creates sessions
- [ ] GET /api/auth/logout destroys sessions
- [ ] GET /api/auth/status returns current user
- [ ] Passwords hashed with bcrypt
- [ ] @login_required decorator protects routes
- [ ] Session timeout: 24 hours

## API Contracts
POST /api/auth/register: {username, email, password} → 201 {success, user_id, username}  
POST /api/auth/login: {username, password} → 200 {success, user_id, username}  
GET /api/auth/logout → 200 {success, message}

## Tests
Registration (success, duplicate username, duplicate email), Login (success, wrong password), Logout, Session persistence, @login_required decorator. Coverage >90%.

## Deliverables
src/service/auth.py, decorators.py, update app.py, tests/test_auth.py

## Branch
feature/20-auth-backend
