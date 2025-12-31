## Tech Lead → Implementer: Feasibility Check for Epic #18

@implementer - PO has clarified Epic #18 requirements (see comments above). Before creating Stories, I need your input on technical feasibility and effort estimation.

---

## Proposed Technical Approach (Based on PO Requirements)

### Stack Decisions:
- **Backend:** Flask (existing) + SQLAlchemy ORM + Flask-Login
- **Database:** SQLite (file-based, no server setup)
- **Frontend:** Vanilla JS (no framework) + existing HTML/CSS
- **Auth:** bcrypt password hashing, session-based (cookies)

### New Dependencies:
```python
# Add to requirements.txt:
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
bcrypt==4.1.2
```

---

## Architecture Overview

### Database Schema (Proposed):
```sql
-- users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- calculation_history table
CREATE TABLE calculation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calculator_type VARCHAR(20) NOT NULL,  -- 'basic', 'scientific', 'financial'
    expression TEXT NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- user_preferences table (for remembering last calculator)
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    last_calculator_type VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### New File Structure:
```
src/service/
├── app.py (existing - add auth routes, DB init)
├── models.py (NEW - SQLAlchemy models)
├── auth.py (NEW - login/register logic)
├── calculators/
│   ├── __init__.py
│   ├── financial.py (NEW - EMI, simple, compound)
│   └── basic.py (existing calculate logic)
├── history.py (NEW - CRUD operations)

static/
├── index.html (MODIFY - add login/register pages)
├── app.js (MODIFY - add auth + history UI)
├── style.css (MODIFY - add menu tabs + history panel)

tests/
├── test_auth.py (NEW)
├── test_history.py (NEW)
├── test_financial.py (NEW)
├── conftest.py (NEW - test fixtures with DB)
```

---

## Feasibility Questions for Implementer

### 1. Technical Approach Validation
**Q:** Is SQLite + SQLAlchemy + Flask-Login the right choice for MVP?
- Any concerns with this stack?
- Alternative recommendations?
- Have you used Flask-Login before, or need ramp-up time?

**Q:** File structure above - does it make sense?
- Would you organize differently?
- Concerns about modularizing calculators?

---

### 2. Effort Estimation (Be realistic!)

Please estimate hours for each component:

**Auth System:**
- [ ] Database models (User, History, Preferences): ___ hours
- [ ] Registration endpoint + validation: ___ hours
- [ ] Login/logout endpoints + session management: ___ hours
- [ ] Password hashing with bcrypt: ___ hours
- [ ] Auth decorators (@login_required): ___ hours
- [ ] Tests for auth flows: ___ hours
- **Subtotal: ___ hours**

**History Feature:**
- [ ] History CRUD operations: ___ hours
- [ ] History API endpoints (list, clear): ___ hours
- [ ] Frontend history panel UI: ___ hours
- [ ] Pagination logic: ___ hours
- [ ] "Use Result" button integration: ___ hours
- [ ] Tests for history: ___ hours
- **Subtotal: ___ hours**

**Financial Calculators:**
- [ ] EMI calculator logic + validation: ___ hours
- [ ] Simple interest calculator: ___ hours
- [ ] Compound interest calculator: ___ hours
- [ ] Frontend UI for financial tab: ___ hours
- [ ] Input validation + error handling: ___ hours
- [ ] Tests with concrete examples from PO: ___ hours
- **Subtotal: ___ hours**

**Menu Navigation:**
- [ ] Tab switching UI (Basic/Sci/Financial): ___ hours
- [ ] Responsive layout adjustments: ___ hours
- [ ] User preference persistence: ___ hours
- [ ] Mobile layout testing: ___ hours
- **Subtotal: ___ hours**

**Integration & Polish:**
- [ ] Database initialization + migrations: ___ hours
- [ ] Integration tests (register→login→calculate→history): ___ hours
- [ ] Error handling + edge cases: ___ hours
- [ ] README updates + API documentation: ___ hours
- [ ] Manual QA testing: ___ hours
- **Subtotal: ___ hours**

**TOTAL ESTIMATE: ___ hours**

---

### 3. Technical Risks & Blockers

**Q:** Do you see any technical risks or blockers?
- Security concerns with the approach?
- Performance issues with SQLite for 50 users?
- Frontend complexity without a framework?
- Testing challenges?

**Q:** Any unknowns that need a spike/prototype first?
- Flask-Login integration complexity?
- Financial formula validation approach?
- History panel UI complexity?

---

### 4. Dependencies & Ordering

**Q:** What's the critical path? Suggested Story order:
1. Database setup + User model + auth backend
2. Auth frontend (register/login pages)
3. History backend (API + storage)
4. History frontend (panel UI)
5. Financial calculators backend
6. Financial calculators frontend
7. Menu navigation + preferences
8. Integration + polish

Does this order make sense, or would you sequence differently?

**Q:** Any parallel work opportunities?
- Can financial calculator logic be built before history is done?
- Can menu UI be built independently?

---

### 5. Testing Strategy

**Q:** How should we approach testing?
- Separate test database (SQLite in-memory)?
- Mock Flask-Login for unit tests?
- Selenium for frontend testing, or manual QA sufficient?

**Q:** Coverage target: PO wants >90%. Is this achievable?
- Which areas hardest to test?
- Need any testing infrastructure changes?

---

### 6. Backward Compatibility Concerns

**Q:** PO wants existing endpoints unchanged. Any issues?
- `/health`, `/metrics`, `/api/calculate` - can remain anonymous?
- Or should we require auth everywhere?
- Migration path for existing anonymous users?

---

## My Preliminary Assessment (Tech Lead)

**Based on PO requirements, I estimate:**
- Auth: ~30 hours
- History: ~25 hours  
- Financial: ~35 hours
- Menu/UI: ~20 hours
- Integration: ~20 hours
- **Total: ~130 hours = 3-4 weeks with 1 FTE**

**This seems feasible IF:**
- ✅ You're familiar with Flask + SQLAlchemy
- ✅ No major unknowns
- ✅ Scope stays fixed (no feature creep)

**Red flags would be:**
- 🚩 Estimate >200 hours (too complex for MVP)
- 🚩 Major unknowns requiring spikes
- 🚩 Security concerns with approach

---

## Deliverable: Your Response Needed

Please respond with:
1. **Validation:** Is the technical approach sound?
2. **Estimate:** Fill in effort hours above (be realistic!)
3. **Risks:** Flag any blockers or unknowns
4. **Sequencing:** Confirm or adjust Story order

Once I have your input, I'll:
1. Create detailed Stories with API contracts
2. Post Story list for PO review
3. Request PO sign-off
4. Mark "Spec Ready" after approval

**Timeline:** Need your response in next 24-48 hours to keep momentum.

Thanks! 🛠️
