## Tech Lead Review - Phase 1.5 Clarification

@PO - Initial review of Epic #18. This is ambitious and well-structured! Before creating Stories and marking Spec Ready, I need clarification on several points:

### 1. User Management Scope & Security

**Authentication Approach:**
- Q: Do we need full secure authentication (bcrypt password hashing, HTTPS-only sessions) or is this internal-only with basic security acceptable?
- Q: Should users be able to reset forgotten passwords? If yes, email verification required?
- Q: Rate limiting on login attempts? (prevent brute force)
- Q: Session timeout duration? (remember me option?)

**User Data:**
- Q: What user info to collect? (username only, or email, full name, etc.?)
- Q: Privacy requirements? GDPR considerations or simple ToS?
- Q: Can users delete their account and all history?

**Concrete example needed:** When user registers, what does the form look like? (fields, validation rules)

---

### 2. Calculation History Storage & Performance

**Storage Design:**
- Q: Retention policy - ALL calculations forever, or limits? (e.g., last 1000 calculations, or last 6 months)
- Q: What metadata to store for each calculation?
  - Timestamp, user_id, calculator_type (basic/scientific/financial)
  - Full expression (e.g., "5 + 3 * 2") or just inputs/result?
  - Device/session info?

**UI/UX:**
- Q: How should history be displayed? (chronological list, grouped by date, grouped by calculator type?)
- Q: Search/filter requirements: by date range only, or also by result value, operation type?
- Q: "Reuse calculation" - what does this mean exactly? Copy result to current input, or re-execute with same inputs?

**Performance:**
- Q: How many concurrent users are we targeting? (10, 100, 1000?)
- Q: Acceptable query latency for history page? (<500ms, <2s?)

**Concrete example needed:** Show me a mockup/description of what the history panel looks like when a user has 50 calculations.

---

### 3. Financial Calculators - Formula & Validation

**EMI Calculator:**
- Q: Standard formula: EMI = [P × R × (1+R)^N] / [(1+R)^N-1]? Any variations?
- Q: Inputs: Principal, Rate (annual %), Tenure (months/years?) - what units?
- Q: Output: Just monthly EMI, or also total interest, total payment, amortization schedule?
- Q: Input constraints: Min/max loan amount? Rate range? Tenure limits?

**Interest Calculators:**
- Q: Simple Interest: I = P × R × T - straightforward?
- Q: Compound Interest: A = P(1 + r/n)^(nt) - need to support different compounding frequencies (monthly, quarterly, annual)?
- Q: Output format: Just final amount, or show principal + interest breakdown?

**Edge Cases:**
- Q: Zero rate? (valid or error?)
- Q: Negative values? (valid for some scenarios or always error?)
- Q: Very large numbers? (precision limits, scientific notation?)
- Q: Decimal precision: round to 2 places for currency, or more?

**Concrete examples needed:** 
- EMI: Loan $100,000 at 8.5% annual for 20 years → EMI = ?
- Compound: $50,000 at 6% annual, compounded monthly, 5 years → Final = ?

---

### 4. Menu-Based Navigation & UX

**Layout:**
- Q: Menu structure - horizontal tabs (Basic | Scientific | Financial), or sidebar navigation?
- Q: Should calculator mode persist per user? (remember last used calculator on login)
- Q: Mobile vs desktop - different layouts or same responsive design?

**User Flow:**
- Q: Does switching calculator types clear current input, or preserve state?
- Q: Should history be visible alongside calculator (split view) or separate page?
- Q: Menu location: top bar, left sidebar, or dropdown?

**Professional Polish:**
- Q: Design inspiration - any specific calculator apps/sites to reference? (Google Calculator, Calculator.net, financial sites?)
- Q: Branding - company logo/colors, or generic professional theme?
- Q: Accessibility requirements - keyboard navigation, screen reader support?

**Concrete example needed:** Sketch or describe the layout when user is on "Financial > EMI Calculator" page.

---

### 5. Technical Implementation Approach

**Database:**
- Q: SQLite (simple, file-based, good for <100 users) vs PostgreSQL (production-grade, requires server)?
- Q: ORM preference? (SQLAlchemy, Peewee, raw SQL?)
- Q: Migration strategy from current (no DB) to new (with DB)?

**Authentication Library:**
- Q: Flask-Login (simple session-based) vs JWT tokens (stateless)?
- Q: Do we need API keys for programmatic access, or just web UI?

**Frontend State Management:**
- Q: Current static JS - continue with vanilla JS, or introduce framework? (Vue, React, Alpine?)
- Q: User context - store in cookies, localStorage, or always fetch from server?

**API Design:**
- Q: New endpoints needed:
  - POST /api/auth/register
  - POST /api/auth/login
  - GET /api/history (with pagination?)
  - POST /api/calculate/emi
  - POST /api/calculate/interest
  - Others?
- Q: Versioning: keep /api/calculate, add new endpoints, or version to /api/v2/?

**Backward Compatibility:**
- Q: Must existing /health, /metrics, /api/calculate remain unchanged?
- Q: Anonymous usage - still allow calculator without login, or require auth?

---

### 6. Testing & Deployment Strategy

**Test Coverage:**
- Q: Unit test focus: business logic (EMI formulas, auth validation), or also integration (API flows)?
- Q: Security testing: penetration testing, or basic auth validation sufficient?
- Q: Performance testing: load testing with concurrent users needed?

**Phased Rollout:**
- Q: You mentioned v0.3.0 → v0.3.1 → v0.3.2 phasing. Is this:
  - Phase 1: Backend only (API + DB), no UI?
  - Phase 2: UI for history + menu?
  - Phase 3: Financial calculators?
- Q: Or should we do vertical slices (complete user management story, then complete history story, etc.)?

**Deployment:**
- Q: Environment - single server, Docker container, cloud platform (Heroku, AWS)?
- Q: Database backup/restore procedures needed?
- Q: Feature flags - how to toggle user management on/off?

---

## Feasibility Assessment (Preliminary)

**Complexity Estimate:**
- User management: ~40 hours (auth system, DB setup, security)
- History feature: ~20 hours (backend + UI)
- Financial calculators: ~30 hours (3 calculators + validation)
- Menu/UX polish: ~20 hours (responsive design, navigation)
- Testing + docs: ~20 hours
- **Total: ~130 hours** (rough estimate, need implementer validation)

**Risks Identified:**
- 🔴 **Security**: User auth is critical - mistakes = vulnerabilities
- 🟡 **Data migration**: Existing users/sessions need migration path
- 🟡 **Formula accuracy**: Financial calcs must be precise - need validation
- 🟢 **UI complexity**: Manageable with incremental approach

**Dependencies:**
- Database setup blocks everything
- Auth system blocks history feature
- Menu system can be built in parallel

---

## Next Steps (Before Spec Ready)

**Required from PO:**
1. ✅ Answer clarification questions above (especially concrete examples)
2. ✅ Prioritize features (must-have vs nice-to-have for v0.3.0)
3. ✅ Validate phasing approach (all-at-once vs incremental)

**Tech Lead will then:**
1. Consult with implementer on technical approach (DB, auth library, etc.)
2. Create detailed Stories with API contracts and test plans
3. Request PO sign-off on Story breakdown
4. Mark "Spec Ready" only after PO approval

**Blocking:** Cannot proceed to Story creation until concrete examples and technical approach are clarified.

CC: @implementer - FYI on upcoming work, will need your input on technical feasibility once PO clarifies requirements.
