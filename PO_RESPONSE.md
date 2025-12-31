## PO Response to Tech Lead Questions - MVP Scope Clarification

@tech-lead - Great questions! Let me clarify: **This is an MVP release** (v0.3.0) with a path to production-grade later. Here are my answers focused on getting to market quickly while keeping architecture clean for future enhancement.

---

### 1. User Management & Security - MVP Scope

**Authentication Approach:**
- **MVP:** Basic secure authentication (bcrypt password hashing, session-based with Flask-Login)
- **MVP:** HTTPS in production, but dev environment can be HTTP
- **NO password reset** in MVP - users contact admin if locked out (keep it simple)
- **NO rate limiting** in MVP - add in v0.4.0 when we have real traffic
- **Session timeout:** 24 hours, no "remember me" option in MVP

**User Data (MVP):**
- **Collect:** Username (unique), Email (for contact), Password (hashed)
- **NO full name, phone, address** - keep minimal
- **Privacy:** Simple ToS, no GDPR compliance in MVP (internal/trusted users only)
- **Account deletion:** Admin-only in MVP (users request via email)

**Registration Form (Concrete Example):**
```
Registration Page:
┌─────────────────────────────────────┐
│  Create Account                     │
├─────────────────────────────────────┤
│  Username: [________] (required)    │
│    • 3-20 chars, alphanumeric + _   │
│                                     │
│  Email: [________] (required)       │
│    • Valid email format             │
│                                     │
│  Password: [________] (required)    │
│    • Min 8 chars                    │
│                                     │
│  Confirm Password: [________]       │
│                                     │
│  [Register] [Cancel]                │
└─────────────────────────────────────┘

Login Page:
┌─────────────────────────────────────┐
│  Login                              │
├─────────────────────────────────────┤
│  Username: [________]               │
│  Password: [________]               │
│                                     │
│  [Login] [Register]                 │
│                                     │
│  Note: Forgot password? Contact admin│
└─────────────────────────────────────┘
```

**Production-grade path (v0.4.0+):**
- Add password reset with email verification
- Add rate limiting and 2FA
- Add GDPR compliance features
- Add self-service account deletion

---

### 2. Calculation History - MVP Scope

**Storage Design (MVP):**
- **Retention:** ALL calculations, no limits for MVP (will add limits when we hit performance issues)
- **Metadata to store:**
  - `id` (primary key)
  - `user_id` (foreign key)
  - `calculator_type` ('basic', 'scientific', 'financial')
  - `expression` (full expression like "5 + 3 * 2" for basic, or "EMI: 100000, 8.5%, 20y" for financial)
  - `result` (final result as string)
  - `timestamp` (created_at)
  - **NO device/session info** in MVP

**UI/UX (MVP):**
- **Display:** Simple chronological list (newest first), no grouping in MVP
- **Search/filter:** NO search in MVP - just paginated list (50 items per page)
- **"Reuse calculation":** Click a history item → copies **result** to current calculator input (simple copy, not re-execute)

**Performance (MVP):**
- **Target users:** <50 concurrent users
- **Query latency:** <2s acceptable for MVP
- **Pagination:** 50 items per page, load more button

**History Panel (Concrete Example):**
```
History Panel (right sidebar on desktop, bottom panel on mobile):
┌─────────────────────────────────────────────┐
│  Calculation History                        │
│  [Clear All History] (confirm dialog)       │
├─────────────────────────────────────────────┤
│  Dec 30, 2025 3:45 PM                       │
│  Basic: 125 + 75 = 200                      │
│  [Use Result ↗]                             │
├─────────────────────────────────────────────┤
│  Dec 30, 2025 3:42 PM                       │
│  Scientific: sin(45°) = 0.707               │
│  [Use Result ↗]                             │
├─────────────────────────────────────────────┤
│  Dec 30, 2025 3:40 PM                       │
│  Financial EMI: $100,000 @ 8.5% = $867.82  │
│  [Use Result ↗]                             │
├─────────────────────────────────────────────┤
│  ... (47 more items)                        │
│  [Load More]                                │
└─────────────────────────────────────────────┘
```

**Production-grade path (v0.4.0+):**
- Add search/filter by date, type, result range
- Add grouping by date or calculator type
- Add export to CSV
- Add retention policy (e.g., 1 year)

---

### 3. Financial Calculators - MVP Scope

**EMI Calculator (MVP):**
- **Formula:** Standard EMI = [P × r × (1+r)^n] / [(1+r)^n - 1]
  - Where r = monthly rate (annual_rate/12/100), n = months
- **Inputs:**
  - Loan Amount: $1,000 - $10,000,000 (USD)
  - Annual Interest Rate: 0.1% - 30% (reasonable range)
  - Tenure: 1 - 30 years (converted to months internally)
- **Output (MVP):** 
  - Monthly EMI (e.g., $867.82)
  - Total Interest (e.g., $108,276.40)
  - Total Payment (e.g., $208,276.40)
  - **NO amortization schedule** in MVP (add in v0.4.0)

**Simple Interest (MVP):**
- **Formula:** I = P × R × T
- **Inputs:** Principal, Rate (annual %), Time (years)
- **Output:** Interest amount + Final amount

**Compound Interest (MVP):**
- **Formula:** A = P(1 + r/n)^(nt)
- **Compounding frequency (MVP):** Monthly, Quarterly, Annual (3 options only)
- **Inputs:** Principal, Rate (annual %), Time (years), Frequency
- **Output:** Interest amount + Final amount (with breakdown)

**Edge Cases (MVP):**
- **Zero rate:** Valid (returns principal only for compound, 0 interest for simple)
- **Negative values:** ERROR - display "Values must be positive"
- **Very large numbers:** Support up to 1 billion, scientific notation if result > 1 trillion
- **Precision:** Round to 2 decimal places for currency display

**Concrete Examples with Expected Results:**
```
EMI Example:
Input: Loan $100,000, Rate 8.5% annual, Tenure 20 years (240 months)
Calculation: r = 8.5/12/100 = 0.00708333
Output:
  Monthly EMI: $867.82
  Total Interest: $108,276.40
  Total Payment: $208,276.40

Compound Interest Example:
Input: Principal $50,000, Rate 6% annual, Time 5 years, Frequency: Monthly
Calculation: A = 50000(1 + 0.06/12)^(12*5) = 50000(1.005)^60
Output:
  Final Amount: $67,409.09
  Interest Earned: $17,409.09
  Principal: $50,000.00
```

**Production-grade path (v0.4.0+):**
- Add amortization schedule for EMI
- Add loan comparison tool
- Add investment calculators (SIP, NPV, IRR)
- Add currency selection

---

### 4. Menu-Based Navigation - MVP Scope

**Layout (MVP):**
- **Structure:** Horizontal tabs at top (Basic | Scientific | Financial)
- **NO sidebar** in MVP - keep it simple
- **Mode persistence:** YES - remember last used calculator per user (store in DB user_preferences)
- **Responsive:** Same layout for desktop/mobile, just stacked vertically on mobile (<768px)

**User Flow (MVP):**
- Switching calculator types **clears current input** (fresh start, prevents confusion)
- History is in **separate panel** (right sidebar desktop, bottom sheet mobile) - always visible, can collapse
- **NO split view** in MVP - too complex

**Professional Polish (MVP):**
- **Design inspiration:** Google Calculator (clean, minimal) + Calculator.net (organized)
- **Branding:** Generic professional theme (blue/gray palette, no logo in MVP)
- **Accessibility (MVP):** Basic keyboard navigation only (Tab, Enter, Esc), NO screen reader in MVP

**Financial Calculator Layout (Concrete Example):**
```
Desktop Layout (Financial > EMI Calculator):
┌─────────────────────────────────────────────────────────────┐
│  [Basic] [Scientific] [Financial] ← Tabs         [Logout]   │
├─────────────────────────────────────────────────────────────┤
│  Financial Calculator          │  History Panel             │
│  ┌─ EMI ─────────────────────┐ │  ┌──────────────────────┐ │
│  │ [EMI] [Simple] [Compound] │ │  │ Recent Calculations  │ │
│  └───────────────────────────┘ │  │ ────────────────────  │ │
│                                 │  │ Dec 30, 3:45 PM      │ │
│  Loan Amount: [_______] USD    │  │ Basic: 125+75 = 200  │ │
│                                 │  │ [Use ↗]              │ │
│  Annual Rate: [_______] %      │  │ ────────────────────  │ │
│                                 │  │ ...                  │ │
│  Tenure: [_______] years       │  └──────────────────────┘ │
│                                 │                           │
│  [Calculate]                    │                           │
│                                 │                           │
│  Monthly EMI: $ ______          │                           │
│  Total Interest: $ ______       │                           │
│  Total Payment: $ ______        │                           │
└─────────────────────────────────────────────────────────────┘

Mobile Layout (<768px):
┌──────────────────────────────┐
│ [☰] Financial Calculator     │
│ [Basic] [Scientific] [Fin] ← │
├──────────────────────────────┤
│ EMI Calculator               │
│ [EMI] [Simple] [Compound]    │
│                              │
│ Loan Amount: [_______] USD   │
│ Annual Rate: [_______] %     │
│ Tenure: [_______] years      │
│                              │
│ [Calculate]                  │
│                              │
│ Monthly EMI: $ ______        │
│ Total Interest: $ ______     │
│ Total Payment: $ ______      │
├──────────────────────────────┤
│ History ▼ (collapsible)      │
│ Dec 30 3:45 PM               │
│ Basic: 125+75 = 200 [Use]    │
│ ...                          │
└──────────────────────────────┘
```

**Production-grade path (v0.4.0+):**
- Add sidebar navigation with categorization
- Add advanced theming/branding
- Add full ARIA/screen reader support
- Add drag-and-drop history items

---

### 5. Technical Implementation - MVP Decisions

**Database (MVP):**
- **Choice:** SQLite (file-based, zero config, perfect for MVP <100 users)
- **ORM:** SQLAlchemy (standard, easy migration to PostgreSQL later)
- **Migration:** New database, no migration needed (currently no DB)

**Authentication (MVP):**
- **Library:** Flask-Login (simple session-based, mature, well-documented)
- **NO JWT** in MVP - add if we need mobile app later
- **NO API keys** in MVP - web UI only

**Frontend (MVP):**
- **Continue vanilla JS** - no framework overhead for MVP
- **User context:** Store username in sessionStorage + cookie for auth
- **NO complex state management** - simple enough without framework

**API Design (MVP):**
```
New endpoints:
POST /api/auth/register
  Body: {username, email, password}
  Response: {success, user_id, message}

POST /api/auth/login
  Body: {username, password}
  Response: {success, user_id, username, message}

GET /api/auth/logout
  Response: {success, message}

GET /api/history?page=1&limit=50
  Response: {calculations: [{id, type, expression, result, timestamp}], total, page}

POST /api/history/clear
  Response: {success, message}

POST /api/calculate/emi
  Body: {loan_amount, annual_rate, tenure_years}
  Response: {emi, total_interest, total_payment}

POST /api/calculate/simple-interest
  Body: {principal, rate, time}
  Response: {interest, final_amount}

POST /api/calculate/compound-interest
  Body: {principal, rate, time, frequency}
  Response: {interest, final_amount}
```

**Versioning (MVP):** Keep existing `/api/calculate`, add new endpoints - NO versioning in MVP

**Backward Compatibility (MVP):**
- **YES** - existing endpoints `/health`, `/metrics`, `/api/calculate` unchanged
- **Anonymous usage:** NO - require login for all calculator features (simplifies MVP)

**Production-grade path (v0.4.0+):**
- Migrate to PostgreSQL when >100 users
- Add JWT for mobile app support
- Add API versioning (/api/v2/)
- Consider Vue.js for richer interactivity

---

### 6. Testing & Deployment - MVP Strategy

**Test Coverage (MVP):**
- **Unit tests:** Business logic (EMI formulas, auth validation, history CRUD)
- **Integration tests:** Critical user flows (register → login → calculate → history → logout)
- **NO security penetration testing** in MVP - basic auth validation sufficient
- **NO performance/load testing** in MVP - add when scaling

**Phased Rollout (MVP = v0.3.0 all-at-once):**
- **NO phasing** - ship all features together in v0.3.0
- **Rationale:** Features are tightly coupled (user management needed for history), better to validate whole MVP at once
- **Timeline:** 4-6 weeks for full MVP

**Deployment (MVP):**
- **Environment:** Single server deployment (can be local, VPS, or Heroku)
- **Database:** SQLite file (include in deployments)
- **Backup:** Manual database file backup weekly
- **Feature flags:** Simple config flag `REQUIRE_AUTH=True/False` in environment

**Production-grade path (v0.4.0+):**
- Docker containerization
- PostgreSQL with automated backups
- CI/CD pipeline with automated testing
- Feature flag service (LaunchDarkly, etc.)

---

## MVP Prioritization - Must Have vs Nice to Have

### Must Have for v0.3.0 (MVP):
- [x] User registration + login + logout
- [x] Calculation history storage + display + pagination
- [x] EMI calculator with accurate formula
- [x] Simple interest calculator
- [x] Compound interest calculator (3 frequencies)
- [x] Menu tabs navigation (Basic, Scientific, Financial)
- [x] History panel with "Use Result" button
- [x] Responsive layout (mobile + desktop)
- [x] Basic error handling + validation
- [x] Tests for financial formulas + auth flows

### Nice to Have (defer to v0.4.0):
- Password reset
- Search/filter history
- Amortization schedule
- Dark mode
- Advanced accessibility
- Export history to CSV
- Rate limiting
- Admin dashboard

---

## Final Answers to Key Questions

1. **Timeline:** 4-6 weeks for v0.3.0 MVP (can we commit resources?)
2. **MVP Scope:** User auth + history + 3 financial calculators + menu navigation
3. **Technical Stack:** Flask + SQLAlchemy + SQLite + Flask-Login + Vanilla JS
4. **Target Users:** <50 concurrent, internal/trusted users, no public internet exposure
5. **Success Metric:** Can user register, calculate EMI, view history, and reuse results? ✅

---

## Approval for Tech Lead Next Steps

@tech-lead - With these clarifications:

1. ✅ **You have my approval** to create Stories based on above requirements
2. ✅ **Use SQLite + Flask-Login** as technical approach
3. ✅ **Ship all features in v0.3.0** (no phasing)
4. ✅ **Estimated 130 hours = 3-4 weeks** with 1 full-time implementer (acceptable)

**Please:**
- Create ~8-10 Stories with detailed API contracts per above endpoints
- Add test plans validating formulas with concrete examples above
- Post Story list for my review before marking "Spec Ready"
- Consult implementer on SQLite/SQLAlchemy approach before finalizing Stories

**I am available** for any follow-up questions. Let's ship this MVP! 🚀
