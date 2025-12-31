## Tech Lead: Story Breakdown for Epic #18

@PO - Based on your approval of phased delivery, here are the 10 Stories for Epic #18. These will be created as individual issues.

---

## SPRINT 1: v0.3.0-alpha (Internal MVP) - 120 hours, 3 weeks

### ✅ Story #19: Database Setup + User Model
- **Created:** https://github.com/nsin08/autobots-calculator/issues/19
- **Estimate:** 6 hours
- **Dependencies:** None (foundation)
- **Delivers:** SQLAlchemy + SQLite setup, User model, bcrypt password hashing, test fixtures

---

### Story #20: Auth Backend (register/login/logout) 
- **Estimate:** 22 hours
- **Dependencies:** Story #19
- **API Endpoints:**
  - `POST /api/auth/register` - Create new user
  - `POST /api/auth/login` - Authenticate and create session
  - `GET /api/auth/logout` - Destroy session
  - `GET /api/auth/status` - Get current user info
- **Delivers:** Flask-Login integration, @login_required decorator, session management, password validation
- **Tests:** Registration success/failure, login/logout flows, session persistence

---

### Story #21: Auth Frontend (register/login pages)
- **Estimate:** 13 hours
- **Dependencies:** Story #20
- **Delivers:**
  - Registration page (username, email, password fields with validation)
  - Login page (username, password with error display)
  - Session persistence in localStorage/cookies
  - Redirect logic (unauthenticated → login, authenticated → calculator)
- **Tests:** Form validation, error handling, session flow

---

### Story #22: History Backend (API + storage)
- **Estimate:** 10 hours
- **Dependencies:** Story #19 (database)
- **Database Model:**
  ```
  calculation_history:
    - id, user_id, calculator_type, expression, result, created_at
  ```
- **API Endpoints:**
  - `GET /api/history?limit=50` - Get user's last 50 calculations
  - `POST /api/history` - Save calculation to history
  - `DELETE /api/history` - Clear all user history
- **Delivers:** History CRUD operations, user isolation (only see own history)
- **Tests:** Create, read, delete, user isolation

---

### Story #23: EMI Calculator (backend + frontend)
- **Estimate:** 22 hours  
- **Dependencies:** Story #19 (database)
- **Formula:** EMI = [P × r × (1+r)^n] / [(1+r)^n - 1]
  - Where r = annual_rate/12/100, n = tenure_years × 12
- **API Endpoint:**
  - `POST /api/calculate/emi`
  - Request: `{loan_amount, annual_rate, tenure_years}`
  - Response: `{emi, total_interest, total_payment}`
- **Frontend:**
  - EMI calculator form (3 inputs)
  - Result display (EMI, total interest, total payment)
  - Input validation (loan: $1k-$10M, rate: 0.1%-30%, tenure: 1-30 years)
- **Validation from PO:**
  - Test case: $100,000 @ 8.5% for 20 years → EMI = $867.82
- **Delivers:** EMI backend logic with Decimal precision, frontend form, tests with PO's exact example
- **Tests:** Happy path, edge cases (zero rate, boundary values), formula accuracy

---

### Story #24: History Frontend (basic UI)
- **Estimate:** 17 hours
- **Dependencies:** Story #21 (auth frontend), Story #22 (history backend)
- **Delivers:**
  - History panel (right sidebar desktop, bottom sheet mobile)
  - Display last 50 calculations chronologically
  - "Use Result" button (copies result to calculator input)
  - "Clear All History" button with confirmation dialog
  - Responsive layout (collapsible on mobile)
- **Tests:** History display, result copy, clear functionality

---

### Story #25: Menu Navigation (Basic, Scientific, Financial tabs)
- **Estimate:** 10 hours
- **Dependencies:** Story #21 (auth frontend), Story #23 (EMI calc exists)
- **Delivers:**
  - Horizontal tab bar (Basic | Scientific | Financial)
  - Tab switching clears current input
  - Active tab highlight
  - Responsive: stack vertically on mobile <768px
- **Tests:** Tab switching, state clearing, responsive breakpoints

---

### Story #26: Sprint 1 Integration Testing
- **Estimate:** 20 hours
- **Dependencies:** All Sprint 1 stories
- **Delivers:**
  - Full user flow integration tests:
    1. Register → login → calculate EMI → save to history → reuse result → logout
    2. Login → view history → clear history
  - Error handling polish (network errors, invalid inputs)
  - Cross-browser testing (Chrome, Firefox)
  - Mobile responsive testing (320px, 768px, 1024px)
- **Tests:** E2E user flows, error states

---

## SPRINT 2: v0.3.0-final (Public Release) - 46 hours, 2 weeks

### Story #27: Simple Interest Calculator
- **Estimate:** 8 hours
- **Dependencies:** Story #23 (EMI pattern established)
- **Formula:** I = P × R × T
- **API Endpoint:**
  - `POST /api/calculate/simple-interest`
  - Request: `{principal, rate, time_years}`
  - Response: `{interest, final_amount}`
- **Frontend:** Simple interest form + result display
- **Tests:** Formula accuracy, edge cases

---

### Story #28: Compound Interest Calculator
- **Estimate:** 10 hours
- **Dependencies:** Story #27
- **Formula:** A = P(1 + r/n)^(nt)
- **API Endpoint:**
  - `POST /api/calculate/compound-interest`
  - Request: `{principal, rate, time_years, frequency}`
  - Response: `{interest, final_amount}`
- **Frequencies:** Monthly, Quarterly, Annual
- **Validation from PO:**
  - Test case: $50,000 @ 6% for 5 years, monthly → Final = $67,409.09
- **Frontend:** Compound interest form with frequency dropdown
- **Tests:** All 3 frequencies, formula accuracy with PO's example

---

### Story #29: Menu Navigation Polish + User Preferences
- **Estimate:** 12 hours
- **Dependencies:** Story #25, Stories #27-28 (all calculators exist)
- **Database Model:**
  ```
  user_preferences:
    - user_id, last_calculator_type
  ```
- **Delivers:**
  - Remember last used calculator per user (persist to DB)
  - On login, restore last calculator type
  - Sub-tabs within Financial (EMI | Simple | Compound)
  - Professional styling polish (colors, spacing, transitions)
- **Tests:** Preference save/load, sub-tab switching

---

### Story #30: Sprint 2 Integration + Documentation
- **Estimate:** 16 hours
- **Dependencies:** All Sprint 2 stories
- **Delivers:**
  - Test all 3 financial calculators with history integration
  - Improve test coverage to >90% overall
  - Full QA: cross-browser (+ Safari), mobile testing
  - README updates:
    - Setup instructions (database init, dependencies)
    - API documentation (all endpoints)
    - User guide (how to use all calculators)
  - Deployment guide (environment config, SECRET_KEY setup)
  - Bug fixes from Sprint 1 feedback
- **Tests:** Full coverage, all user flows

---

## Story Summary

**Sprint 1 (120 hours):**
- Story #19: Database Setup (6h) ✅ CREATED
- Story #20: Auth Backend (22h)
- Story #21: Auth Frontend (13h)
- Story #22: History Backend (10h)
- Story #23: EMI Calculator (22h)
- Story #24: History Frontend (17h)
- Story #25: Menu Navigation (10h)
- Story #26: Integration Testing (20h)

**Sprint 2 (46 hours):**
- Story #27: Simple Interest (8h)
- Story #28: Compound Interest (10h)
- Story #29: Menu Polish + Preferences (12h)
- Story #30: Integration + Docs (16h)

**Total: 166 hours across 10 stories**

---

## Story Dependencies (Critical Path)

```
Story #19 (DB) → Story #20 (Auth Backend) → Story #21 (Auth Frontend)
                                             ↓
Story #19 (DB) ─────────────→ Story #22 (History Backend) → Story #24 (History Frontend)
                                             ↓
Story #19 (DB) ─────────────→ Story #23 (EMI Calculator)
                                             ↓
                                          Story #25 (Menu Nav)
                                             ↓
                                          Story #26 (Sprint 1 Integration)
                                             ↓
                                          Story #27 (Simple Interest)
                                             ↓
                                          Story #28 (Compound Interest)
                                             ↓
                                          Story #29 (Menu Polish)
                                             ↓
                                          Story #30 (Sprint 2 Integration + Docs)
```

**Parallel opportunities:**
- Stories #20, #22, #23 can run in parallel (all depend only on #19)
- Stories #27, #28 can run in parallel

---

## Next Steps

@PO - Please review this Story breakdown:

1. **Scope Check:** Does this match your vision for v0.3.0-alpha and v0.3.0-final?
2. **Priority Check:** Is Sprint 1 (EMI only) sufficient for internal validation?
3. **Estimate Check:** 120 + 46 = 166 hours as approved?

**I will:**
1. Create issues #20-30 (Stories 2-10) with detailed API contracts
2. Link all stories to Epic #18
3. Mark Epic #18 as "Spec Ready" after your approval
4. Assign Story #19 to implementer to kick off Sprint 1

**Your approval needed by tomorrow EOD** to maintain timeline.

Ready to create remaining stories! 🚀
