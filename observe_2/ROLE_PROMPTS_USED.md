# Role Prompts Used in Session - Epic #8

This document captures the exact role-based prompts and context that guided each phase of the v0.2.0 workflow.

## Base Context

All roles operated with the following context:
- Project: Autobots Calculator (existing v0.1.0 with basic operations)
- Repository: https://github.com/nsin08/autobots-calculator
- RULEBANK rules enforced
- Template-driven workflow
- 5-role lifecycle: Sponsor → Tech Lead → Implementer → Reviewer → Release
- Starting Point: v0.1.0 (basic calculator with +, -, ×, ÷)
- Target: v0.2.0 (add advanced features)

---

## Role 1: Sponsor/PO

### Prompt Template
```
[Role: Sponsor/PO]

Act as Sponsor/PO.

Task: Create an Idea Issue using the Story/Task template, but focused on "Problem + Success Criteria + Non-goals".
Also define a minimal Epic boundary if this is larger than 1 PR.

Deliver:
- 1 Idea Issue (or 1 Epic + 1 Story if needed)
- Clear success criteria that can be tested
- Non-goals to prevent scope creep

Do NOT:
- prescribe implementation details
- specify technology choices
- define how to implement

Focus on:
- WHAT problem needs solving
- WHY it matters
- WHAT success looks like (measurable)
- WHAT is explicitly out of scope
```

### User Input
> "as PO i want to add advanced features in calculator like scientific mode, history, multiline display"

### Execution Context
- Existing v0.1.0 calculator already deployed
- Need to extend functionality without breaking existing features
- Multiple features suggested → Epic needed
- Clear business value: enable technical users, improve productivity

### Deliverable
- Epic #8: "Advanced Calculator Features v0.2.0"
- Problem Statement: Current calculator limited to basic operations, technical users need more
- 6 Epic-level success criteria (measurable)
- Scope clearly defined (In: scientific, history, multiline / Out: unit conversion, graphing, etc.)
- Target release: v0.2.0

---

## Role 2: Tech Lead/Architect

### Prompt Template
```
[Role: Tech Lead/Architect]

Act as Tech Lead/Architect.

Input: the Idea Issue.

Task: Decide whether to create an Epic and split into Stories/Tasks.
Add minimal architecture notes: API contract, data shape, error handling, and test strategy.
Mark items "Spec Ready" only if DoR is satisfied.

Deliver:
- Epic (if needed) + Story/Task issues with test plans
- A short "Architecture Note" comment (5-10 bullets) on the Epic or Story
- Identify dependencies and branch plan (one branch per story)
- Validate Definition of Ready (DoR)

Architecture notes must include:
- API contracts (endpoints, payloads, status codes)
- Data models (minimal schema)
- Error handling strategy
- Test strategy (unit, integration, e2e scope)
- Dependencies between stories

Do NOT:
- implement code
- make decisions that belong to implementer (variable names, exact file structure)
```

### User Input (Implicit)
> [Received Epic #8 from PO]
> Task: Break down into implementable stories

### Execution Context
- Need to balance backend vs frontend work
- Consider parallel development (3 developers could work simultaneously)
- Story #12 is integration story (must wait for #10, #11)
- Client-side vs backend trade-off for scientific functions
- SessionStorage vs database for history

### Key Architectural Decisions

**Decision 1: Client-side Scientific Functions**
- Rationale: JavaScript Math API sufficient, no backend changes needed, faster response
- Trade-off: No arbitrary precision, but acceptable for v0.2.0 scope
- Impact: Story #10 can be pure frontend, parallel with backend Story #9

**Decision 2: SessionStorage for History**
- Rationale: Ephemeral storage fits v0.2.0 scope, no database complexity
- Trade-off: History lost on browser close, but acceptable (documented in README)
- Impact: Story #11 can be pure frontend, no backend dependency

**Decision 3: Multiline Display as Integration Story**
- Rationale: Needs scientific + history features to test integration
- Dependencies: Must wait for Stories #10 and #11 to merge
- Impact: Story #12 cannot start until #10, #11 complete

**Decision 4: Backend API Extensions**
- Rationale: Factorial, power, modulo need server-side for consistency with v0.1.0 pattern
- Trade-off: Additional backend tests, but maintains API consistency
- Impact: Story #9 backend-only, can proceed immediately

### Deliverables
- Story #9: Backend API (factorial, power, modulo) - 10 criteria
- Story #10: Scientific mode UI (8 functions, client-side) - 10 criteria
- Story #11: History panel (sessionStorage) - 10 criteria
- Story #12: Multiline display (integration) - 10 criteria, depends on #10, #11
- Architecture Note comment on Epic #8

---

## Role 3: Implementer - Story #9 (Backend API)

### Prompt Template
```
[Role: Implementer]

Act as Implementer.

Input: one "Spec Ready" Task.

Task: Create branch, implement only what's required, add tests, update docs, open PR with PR template fully filled.

Deliver:
- Branch name: feature/<issue-id>-<slug> or chore/<issue-id>-<slug>
- Implementation that meets all success criteria
- Tests (unit + integration as specified in test plan)
- Updated documentation (README, API docs, etc.)
- PR that closes the issue
- PR template fully filled with evidence for each success criterion
- No extra scope; if discovered work is needed, create a follow-up task issue

Steps:
1. Read the task and success criteria carefully
2. Create appropriately named branch
3. Implement minimal solution
4. Add tests that prove criteria are met
5. Update docs
6. Open PR using template
7. Map each success criterion to evidence in PR

Do NOT:
- add features not in success criteria
- refactor unrelated code
- skip tests
- leave PR template with placeholders
```

### User Input (Implicit)
> [Picked Story #9 from Spec Ready state]

### Execution Context
- Backend-only changes (src/service/app.py, tests/test_calculate.py)
- Existing test suite: 20 tests passing
- Need to add 3 operations with validation
- Target: 10 new tests for edge cases
- Must maintain backward compatibility

### Implementation Strategy
1. **Factorial Operation:**
   - Validate: input must be integer 0-20
   - Error cases: negative, non-integer, too large (>20)
   - Use Python math.factorial()

2. **Power Operation:**
   - Validate: exponent bounds -100 to 100
   - Error case: exponent out of bounds
   - Use Python pow()

3. **Modulo Operation:**
   - Validate: divisor not zero
   - Error case: division by zero
   - Use Python % operator

4. **Testing Strategy:**
   - Happy path: 1 test each
   - Edge cases: factorial (0, negative, large, non-integer), power (negative exp, large exp), modulo (zero divisor)
   - Total: 10 tests

### Deliverable
- PR #13: "Add factorial, power, and modulo operations to calculate API"
- Evidence mapped for each criterion
- 30/30 tests passing (20 original + 10 new)
- README API section updated

---

## Role 4: Reviewer/QA - Story #9

### Prompt Template
```
[Role: Reviewer/QA]

Act as Reviewer/QA.

Input: PR + linked Issue + Epic.

Task: Verify PR meets criteria, run review checklist, request changes with concrete bullets or approve.

Deliver:
- Review comment structured as:
  - Pass/Fail against each success criterion
  - Missing tests/docs (if any)
  - Suggested minimal fixes
  - Code quality assessment
- If changes requested: move item back to In Progress with reason
- If approved: move to Done

Review checklist (from RULEBANK):
- [ ] PR links exactly one Issue and references Epic
- [ ] PR template complete (no placeholders)
- [ ] Each success criterion has evidence
- [ ] Tests exist and cover happy path + 1 edge case
- [ ] Tests passing (CI green)
- [ ] Docs updated (or "not needed" with reason)
- [ ] No unrelated refactors
- [ ] Naming / structure consistent

Provide concrete, actionable feedback:
- Point to specific lines/files
- Suggest exact fixes
- Link to standards/examples if relevant

Do NOT:
- approve without verifying all criteria
- request changes without concrete examples
- introduce new requirements not in original issue
```

### User Input (Implicit)
> [PR #13 ready for review]

### Execution Context
- Backend changes only (app.py, test_calculate.py, README.md)
- CI passing (30/30 tests)
- Need to verify each of 10 criteria
- Check for unrelated changes

### Review Process
1. **Retrieve Story #9 criteria** - All 10 success criteria documented
2. **Verify CI status** - gh pr checks 13 → All passing
3. **Code review:**
   - app.py: factorial logic with validation ✅
   - app.py: power logic with bounds checking ✅
   - app.py: modulo logic with zero check ✅
   - test_calculate.py: 10 new tests covering edge cases ✅
   - README.md: API documentation updated ✅
4. **Map criteria to evidence** - Each criterion linked to specific code
5. **Decision: APPROVED** - All criteria met, no issues

### Deliverable
- Review comment with detailed validation
- PR #13 merged via squash
- Story #9 auto-closed

---

## Role 3: Implementer - Story #10 (Scientific Mode UI)

### User Input (Implicit)
> [Picked Story #10 from Spec Ready state]

### Execution Context
- Frontend-only changes (HTML, CSS, JavaScript)
- Client-side implementation (no backend)
- Need 8 scientific functions
- DEG/RAD angle mode essential for trig functions
- Keyboard shortcuts for power users
- Responsive design for mobile/desktop

### Implementation Strategy
1. **UI Structure:**
   - Mode toggle buttons (Scientific, DEG/RAD, History)
   - Scientific panel with 8 function buttons
   - Hidden by default, toggled via button

2. **Functions:**
   - Trigonometric: sin, cos, tan (respect angle mode)
   - Mathematical: sqrt, log, ln, exp
   - Constant: π (pi)

3. **Angle Conversion:**
   - DEG mode: convert to radians before Math.sin/cos/tan
   - RAD mode: pass directly to Math functions
   - Helper functions: toRadians(), toDegrees()

4. **Error Handling:**
   - sqrt of negative → error
   - log/ln of non-positive → error
   - Display error message without breaking UI

5. **Keyboard Shortcuts:**
   - s = sin, o = cos (c conflicts with clear), t = tan
   - q = sqrt (square root), l = log

6. **Responsive Design:**
   - Mobile (<768px): Panel stacks below calculator
   - Desktop (>=768px): Panel displays beside calculator
   - Buttons resize appropriately

### Deliverable
- PR #14: "Add scientific mode with 8 functions and DEG/RAD toggle"
- Manual testing evidence (each function tested in browser)
- README scientific mode section

---

## Role 4: Reviewer/QA - Story #10

### Execution Context
- Frontend changes require manual browser testing
- CI only checks backend (30/30 tests passing, no regressions)
- Need to test each function in DEG and RAD modes
- Verify responsive layouts at multiple breakpoints

### Manual Testing Process
1. **Function Testing:**
   - sin(30) DEG → 0.5 ✅
   - cos(60) DEG → 0.5 ✅
   - tan(45) DEG → 1.0 ✅
   - sqrt(16) → 4 ✅
   - log(100) → 2 ✅
   - ln(e) → 1 ✅
   - exp(1) → 2.718... ✅
   - π → 3.14159... ✅

2. **Angle Mode:**
   - Toggle DEG/RAD → button text changes ✅
   - sin(π/2) RAD → 1.0 ✅

3. **Error Handling:**
   - sqrt(-1) → error message ✅
   - log(-10) → error message ✅

4. **Keyboard Shortcuts:**
   - Press 's' → sin function ✅
   - Press 'o' → cos function ✅
   - Press 'q' → sqrt function ✅

5. **Responsive:**
   - 320px: panel stacked, buttons readable ✅
   - 768px: side-by-side layout ✅

### Deliverable
- Review comment with manual testing results
- PR #14 approved and merged
- Story #10 closed

---

## Role 3: Implementer - Story #11 (History Panel)

### User Input (Implicit)
> [Picked Story #11 from Spec Ready state]

### Execution Context
- Frontend-only changes (HTML, CSS, JavaScript)
- SessionStorage for persistence
- 20-entry FIFO queue (oldest removed when 21st added)
- Click-to-load functionality
- Integration with existing calculation flow

### Implementation Strategy
1. **Data Structure:**
   - Array: calculationHistory = []
   - Entry: { expression, result, timestamp }
   - Max: 20 entries (MAX_HISTORY constant)

2. **Storage:**
   - sessionStorage.setItem('calculatorHistory', JSON.stringify(array))
   - sessionStorage.getItem('calculatorHistory') on page load
   - Error handling for storage failures

3. **FIFO Queue:**
   - Use array.unshift() to add at beginning
   - Use array.slice(0, MAX_HISTORY) to enforce limit
   - Oldest entries automatically removed

4. **UI:**
   - History panel with header (title + Clear button)
   - History list with items
   - Each item: expression + result
   - Empty state: "No history" message

5. **Interactions:**
   - Click item → load result to display
   - Click Clear → empty history
   - Toggle button → show/hide panel

6. **Integration:**
   - Modify performCalculation() to call addToHistory() after successful calc
   - Expression format: "${previousValue} ${operator} ${inputValue}"

### Deliverable
- PR #15: "Add calculation history panel with sessionStorage"
- Manual testing evidence (FIFO, persistence, responsive)
- README history section

---

## Role 4: Reviewer/QA - Story #11

### Manual Testing Process
1. **History Display:**
   - Perform 5 calculations → all displayed ✅

2. **FIFO Queue:**
   - Add 21st calculation → oldest removed ✅
   - Verify order (newest at top) ✅

3. **Click to Load:**
   - Click history item → result loads to display ✅

4. **Clear:**
   - Click Clear button → history emptied ✅
   - "No history" message appears ✅

5. **Toggle:**
   - Click History button → panel shows ✅
   - Click again → panel hides ✅

6. **Persistence:**
   - Add calculations → refresh page → history persisted ✅

7. **Responsive:**
   - 320px: history stacks below calculator ✅
   - 768px: history side-by-side with calculator ✅

### Deliverable
- Review comment with testing results
- PR #15 approved and merged
- Story #11 closed

---

## Role 3: Implementer - Story #12 (Multiline Display)

### User Input (Implicit)
> [Picked Story #12 from Spec Ready state after #10, #11 merged]

### Execution Context
- Integration story (depends on scientific mode + history)
- Requires display restructuring
- Previous result line + current input line
- Operation preview during calculation
- Full expression after result

### Implementation Strategy
1. **Display Structure:**
   - Replace single display div with display-container
   - Line 1: calculator-previous (previous result/operation)
   - Line 2: calculator-display (current input)

2. **State Management:**
   - Add variable: previousDisplay = ''
   - Update on: operator selection, calculation, history load
   - Clear on: new calculation start

3. **Operation Preview:**
   - appendOperator(): previousDisplay = "${value} ${operator}"
   - Example: User enters 5, clicks + → Previous shows "5 +"

4. **Full Expression:**
   - calculate(): previousDisplay = "${expression} ="
   - Example: 5 + 3 = → Previous shows "5 + 3 =", Current shows "8"

5. **History Integration:**
   - loadFromHistory(): previousDisplay = entry.expression
   - Shows original expression when loading from history

6. **Styling:**
   - Previous line: 1rem, color #a0aec0 (gray)
   - Current line: 2.5rem, color white
   - Container: min-height 100px, max-height 150px, overflow-y auto

7. **Responsive:**
   - Same breakpoints as existing features
   - Display adapts with word-wrap

### Deliverable
- PR #16: "Add multiline display with operation preview"
- Manual testing evidence (integration with scientific + history)
- README multiline display section

---

## Role 4: Reviewer/QA - Story #12

### Manual Testing Process
1. **Basic Calculation Sequence:**
   - Enter 5 → Previous: '' / Current: '5' ✅
   - Click + → Previous: '5 +' / Current: '5' ✅
   - Enter 3 → Previous: '5 +' / Current: '3' ✅
   - Click = → Previous: '5 + 3 =' / Current: '8' ✅
   - Click + → Previous: '8 +' / Current: '8' ✅

2. **Scientific Integration:**
   - Enter 30, click sin → Previous shows function context ✅

3. **History Integration:**
   - Click history item → Previous shows original expression ✅

4. **Responsive:**
   - 320px: All three features (calc, scientific, history) stack ✅
   - 768px: Side-by-side layout maintained ✅

5. **Overflow:**
   - Long number (20 digits) → Wraps correctly ✅

### Deliverable
- Review comment: "Final story for Epic #8. Ready to merge and release v0.2.0."
- PR #16 approved and merged
- Story #12 closed
- All 4 stories complete

---

## Role 5: Release/DevOps

### Prompt Template
```
[Role: Release/DevOps]

Act as Release/DevOps.

Input: Approved PR(s) merged to main.

Task: Ensure release hygiene: tags, changelog/release notes, build artifact, and move items to Released.

Deliver:
- Tag v<major>.<minor>.<patch> following SemVer
- Release notes (from merged PR titles + linked issues)
- Verify CI green on main
- Mark Epic "Released" when all child stories are Released
- Update CHANGELOG.md

Release notes format:
## v0.2.0 - YYYY-MM-DD

### Features
- Feature description (#pr-number, closes #issue-number)

### Changes
- Change description (#pr-number)

### Fixes
- Fix description (#pr-number, closes #issue-number)

Steps:
1. Verify all PRs for Epic are merged
2. Verify CI is green
3. Create git tag
4. Generate release notes from PR metadata
5. Create GitHub release with notes
6. Update project board (move to Released)
7. Close Epic if all stories complete

Do NOT:
- release if CI is not green
- skip release notes
- forget to update project board
```

### User Input (Implicit)
> [All 4 stories merged, ready to release]

### Execution Context
- All PRs merged to master
- CI green (30/30 tests passing)
- Epic #8 has 4 complete stories
- Need to validate epic-level success criteria
- Create comprehensive release notes

### Release Process
1. **Update Master Branch:**
   ```bash
   git checkout master
   git pull
   ```

2. **Verify Epic Complete:**
   - Story #9: ✅ Merged (PR #13)
   - Story #10: ✅ Merged (PR #14)
   - Story #11: ✅ Merged (PR #15)
   - Story #12: ✅ Merged (PR #16)

3. **Post Epic Completion Comment:**
   - All 4 stories summary
   - Epic-level criteria validation (all 6 met)
   - Measurable goals achieved
   - Feature summary
   - Stats (4 PRs, ~450 lines, 30/30 tests)

4. **Create Git Tag:**
   ```bash
   git tag v0.2.0 -m "Release v0.2.0: Advanced Calculator Features..."
   git push origin v0.2.0
   ```

5. **Generate Release Notes:**
   - Overview
   - New Features (detailed breakdown)
   - Changes by Story
   - Testing summary
   - Documentation updates
   - Breaking Changes (none)
   - Known Limitations
   - Upgrade Notes

6. **Create GitHub Release:**
   ```bash
   gh release create v0.2.0 --title "v0.2.0 - Advanced Calculator Features" --notes-file release_notes_v0.2.0.md
   ```

7. **Close Epic #8:**
   ```bash
   gh issue close 8 --comment "🎉 Epic #8 Complete - v0.2.0 Released!..."
   ```
   - Final summary with links
   - Epic-level criteria validation
   - Workflow demonstration confirmed

8. **Verify Final State:**
   ```bash
   gh issue list --label epic --state all
   gh release list
   ```

### Deliverable
- Git tag v0.2.0 created and pushed
- GitHub Release v0.2.0 published
- Epic #8 closed with full traceability
- All success criteria validated
- v0.2.0 in production

---

## Key Prompt Patterns Used

### Evidence-Based Validation
Every PR review included explicit evidence mapping:
```
Success Criterion 1: [Description]
Evidence: [file.ext](path/to/file.ext#L10-L20) - [specific code or test name]
```

### PowerShell Multi-line Handling
For PR bodies and comments:
```powershell
$body = @'
Multi-line
content
here
'@
gh pr create --title "..." --body $body
```

### Manual Testing Protocol
Frontend changes required structured manual testing:
1. Function testing (each feature)
2. Integration testing (features together)
3. Responsive testing (breakpoints: 320px, 480px, 768px, 1024px)
4. Error handling (edge cases)
5. Keyboard shortcuts (if applicable)

### Dependency Management
Story #12 explicitly waited for #10, #11:
```
Dependencies: MUST WAIT for Stories #10 and #11 to merge first (integration story)
```

### Scope Control
Each role reinforced scope boundaries:
- PO: Non-goals explicitly listed
- Tech Lead: Architecture notes clarified what's in/out
- Implementer: "Only what's in success criteria, no extra scope"
- Reviewer: "No scope creep" in DoD checklist

---

## Prompts vs. Execution Summary

| Role | Prompt Focus | Execution Focus | Key Constraint |
|------|-------------|-----------------|----------------|
| Sponsor/PO | Problem + Success Criteria | Epic #8 with measurable goals | No implementation details |
| Tech Lead | Architecture + Dependencies | 4 stories with 10 criteria each | No coding |
| Implementer | Minimal solution + Tests | Code + Tests + Docs for each story | Only what's in criteria |
| Reviewer | Validate + Evidence | Manual testing + Code review | Concrete feedback only |
| Release/DevOps | Tag + Release Notes + Close | v0.2.0 release with full notes | CI must be green |

---

## Session Completion

**All role prompts successfully executed:**
- ✅ Sponsor created Epic with scope
- ✅ Tech Lead split into 4 stories with architecture
- ✅ Implementer built all 4 stories (4 PRs)
- ✅ Reviewer validated all 4 PRs (approved, merged)
- ✅ Release shipped v0.2.0 (tagged, documented, closed)

**Full lifecycle demonstrated with role discipline maintained throughout!** 🎉
