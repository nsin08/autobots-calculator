# QA in the Loop - Quality Gates Guide

This document details how QA/Reviewer role acts as a critical quality gate in the 5-role workflow, ensuring all deliverables meet standards before progressing.

## Overview

**QA Role Position in Workflow:**
```
Sponsor/PO (Intake) 
    ↓
Tech Lead (Spec Ready)
    ↓
Implementer (In Progress)
    ↓
>>> QA/Reviewer (In Review) <<<  ⚠️ QUALITY GATE
    ↓
Release/DevOps (Released)
```

**QA is the gatekeeper between implementation and release.**

---

## QA's Responsibilities

### 1. **Pre-Review Validation**
Before diving into code review:
- [ ] Verify PR is linked to exactly one Issue
- [ ] Verify Issue is linked to parent Epic
- [ ] Confirm PR template is fully filled (no placeholders)
- [ ] Check CI/CD checks are passing (green builds)
- [ ] Verify branch naming follows convention

**Stop Criteria:** If any of these fail, request changes immediately without detailed code review.

### 2. **Success Criteria Validation**
For each criterion in the original story:
- [ ] Map criterion to specific evidence (code line, test name, doc section)
- [ ] Verify implementation meets the requirement
- [ ] Check edge cases are covered
- [ ] Validate error handling exists

**Example Mapping:**
```
Criterion 1: "Endpoint returns 200 status"
Evidence: 
  - Code: src/service/app.py lines 45-50 (@app.route('/health'))
  - Test: tests/test_health.py::test_health_returns_200 (PASSING)
  ✅ VALIDATED
```

### 3. **Test Coverage Review**
- [ ] All success criteria have corresponding tests
- [ ] Happy path covered (expected inputs → expected outputs)
- [ ] At least 1 edge case per criterion
- [ ] Error conditions tested (invalid inputs, boundary conditions)
- [ ] Test names are descriptive (test_<feature>_<behavior>)
- [ ] Tests actually assert the behavior (not just code coverage)

**Coverage Target:** >90% for new code (from RULEBANK)

### 4. **Code Quality Assessment**
- [ ] No unrelated changes (scope discipline)
- [ ] Naming conventions followed (consistent with codebase)
- [ ] No commented-out code or TODOs without issue references
- [ ] Error messages are clear and actionable
- [ ] Code is readable (complexity appropriate to task)

**Not QA's job:** Nitpicking style if lint passes. Focus on correctness and maintainability.

### 5. **Documentation Review**
- [ ] README updated with new features/endpoints
- [ ] API contracts documented (if backend changes)
- [ ] Usage examples included
- [ ] Known limitations noted (if any)

### 6. **Integration & Regression Check**
- [ ] New feature doesn't break existing functionality
- [ ] CI green (all tests passing, not just new ones)
- [ ] Dependencies updated appropriately (if needed)
- [ ] No new security vulnerabilities introduced

---

## QA Review Process (Step-by-Step)

### Step 1: Retrieve Context
```bash
# Get the PR details
gh pr view <pr-number>

# Get linked story
gh issue view <story-number>

# Get CI status
gh pr checks <pr-number>
```

**Collect:**
- Story success criteria (the contract)
- Architecture notes from Epic/Story
- Test plan from story
- PR evidence mapping

### Step 2: Validate CI
```bash
gh pr checks <pr-number>
```

**If CI failing:** Request changes immediately:
```
Changes Requested: CI checks failing

Please fix the following before code review:
- [ ] Tests: <test-name> failing (see CI logs)
- [ ] Lint: <file> has style issues

Re-request review when CI is green.
```

### Step 3: Checkout and Test Locally
```bash
# Checkout PR branch
gh pr checkout <pr-number>

# Run tests locally
pytest tests/ -v

# Run service (if applicable)
python -m src.service.app

# Manual testing (for frontend/API changes)
curl http://localhost:5000/<endpoint>
```

**Document test results** for review comment.

### Step 4: Code Review
Review each changed file:
- Does it implement the success criteria?
- Are edge cases handled?
- Is error handling present?
- Are changes minimal (no scope creep)?

**Use inline comments** for specific issues:
```
File: src/service/app.py
Line 45: Missing error handling for invalid input
Suggestion: Add try/except or validation before processing
```

### Step 5: Review PR Template
Check that implementer filled these sections:
- [ ] Summary (clear description of changes)
- [ ] Mapping to Success Criteria (evidence for each)
- [ ] Test Evidence (test output or screenshots)
- [ ] Risk Assessment (rollback plan)
- [ ] DoD Checklist (all items checked)

**If missing:** Request completion before approval.

### Step 6: Make Decision

#### Option A: Approve ✅
```bash
gh pr review <pr-number> --approve --body "<approval-comment>"
```

**Approval comment structure:**
```markdown
## QA Review: Approved ✅

### Success Criteria Validation
1. ✅ Criterion 1: <evidence>
2. ✅ Criterion 2: <evidence>
...

### Test Coverage
- ✅ <X> tests added
- ✅ Happy path covered
- ✅ Edge cases: <list>
- ✅ Error handling tested

### Code Quality
- ✅ No unrelated changes
- ✅ Naming conventions followed
- ✅ Documentation updated

### CI Status
- ✅ All checks passing (<X> tests in <Y>s)

**Approved for merge.**
```

#### Option B: Request Changes 🔄
```bash
gh pr comment <pr-number> --body "<changes-comment>"
```

**Changes comment structure:**
```markdown
## QA Review: Changes Requested 🔄

### Issues Found

**Critical (must fix):**
- [ ] Criterion 3 not met: <specific issue>
  - Evidence missing: <what's needed>
  - Suggested fix: <concrete suggestion>

**Minor (should fix):**
- [ ] Test coverage: Missing edge case for <scenario>
  - Add test: test_<feature>_<edge-case>

### Next Steps
1. Address critical issues
2. Update PR with fixes
3. Re-request review

Marking story as "In Progress" until issues resolved.
```

---

## QA Review Checklist

Use this checklist for every PR review:

### Pre-Review
- [ ] PR linked to exactly one Issue
- [ ] Issue linked to parent Epic
- [ ] PR template fully filled
- [ ] CI checks passing (green)
- [ ] Branch naming correct

### Success Criteria
- [ ] Each criterion has evidence
- [ ] Implementation meets requirements
- [ ] Edge cases covered
- [ ] Error handling present

### Testing
- [ ] Tests exist for all criteria
- [ ] Happy path covered
- [ ] Edge cases tested (≥1 per criterion)
- [ ] Error conditions tested
- [ ] All tests passing (local + CI)
- [ ] Coverage >90%

### Code Quality
- [ ] No unrelated changes
- [ ] Naming conventions followed
- [ ] No TODOs without issue refs
- [ ] Code is readable
- [ ] Error messages clear

### Documentation
- [ ] README updated
- [ ] API docs updated (if applicable)
- [ ] Examples provided
- [ ] Limitations noted

### Integration
- [ ] No regressions (existing tests pass)
- [ ] Dependencies appropriate
- [ ] No security issues

### Decision
- [ ] Approve OR
- [ ] Request changes (with concrete feedback)

---

## QA Anti-Patterns (Don't Do This)

### ❌ Approving Without Validation
**Wrong:**
```
LGTM! Looks good to me.
```

**Right:**
```
Reviewed against all 10 success criteria. All tests passing. 
Evidence provided for each criterion. Approved.
```

### ❌ Vague Change Requests
**Wrong:**
```
This doesn't look right. Please fix.
```

**Right:**
```
Criterion 3 not met: Expected error handling for division by zero.
File: app.py line 45
Suggested fix: Add `if b == 0: return error('Division by zero')`
Test needed: test_calculate_division_by_zero
```

### ❌ Introducing New Requirements
**Wrong:**
```
Can you also add a /status endpoint while you're at it?
```

**Right:**
```
Out of scope for this story. If needed, create separate story #<X> for /status endpoint.
```

### ❌ Nitpicking Style Over Substance
**Wrong:**
```
I prefer single quotes over double quotes. Please change all strings.
```

**Right:**
```
(If lint passes, this is not QA's concern. Focus on correctness.)
```

### ❌ Approving When CI Fails
**Wrong:**
```
Code looks good, approved! (CI: 2 tests failing)
```

**Right:**
```
Cannot approve with failing CI. Fix test failures first.
```

---

## Manual Testing Protocols

For frontend or API changes, QA performs manual testing:

### Backend API Testing
```bash
# Start service
python -m src.service.app

# Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/metrics

# Test error cases
curl -X POST http://localhost:5000/api/calculate -H "Content-Type: application/json" -d '{"operation":"divide","a":5,"b":0}'
```

**Document results:**
- ✅ /health returns 200 with {"status": "ok", ...}
- ✅ /metrics returns 200 with {"requests_total": X, ...}
- ✅ Division by zero returns 400 with error message

### Frontend Testing
```bash
# Start service
python -m src.service.app

# Open browser
# Navigate to http://localhost:5000

# Test interactions
# - Click buttons
# - Enter inputs
# - Verify outputs
```

**Test at responsive breakpoints:**
- 320px (mobile)
- 768px (tablet)
- 1024px+ (desktop)

**Document results with screenshots** (if significant UI changes).

---

## QA Metrics to Track

### Quality Indicators
- **Approval Rate:** % of PRs approved on first review
  - Target: 80%+ (indicates good story specs and implementation)
- **Rework Rate:** % of PRs requiring changes
  - Target: <20%
- **Criteria Coverage:** % of PRs with evidence for all criteria
  - Target: 100%

### Process Indicators
- **Review Turnaround Time:** Hours from PR open to review complete
  - Target: <4 hours (same day)
- **Fix Turnaround Time:** Hours from changes requested to fix submitted
  - Target: <8 hours

### Defect Leakage
- **Post-Release Issues:** # of bugs found after release that passed QA
  - Target: 0 for criteria explicitly tested

**Track these over time to improve the process.**

---

## QA Escalation Paths

### When to Escalate

**To Tech Lead:**
- Story criteria are ambiguous (can't validate)
- Architecture decision needed (out of QA scope)
- Multiple interpretations of requirement

**To Sponsor/PO:**
- Success criteria don't match user need (discovered during review)
- Scope creep detected (implementer added features not in story)

**To Release/DevOps:**
- CI infrastructure issues (not code issues)
- Merge conflicts requiring resolution
- Security vulnerability detected

### How to Escalate
1. **Document the issue clearly**
2. **Block PR** (do not approve)
3. **Comment on PR** with escalation notice
4. **Tag appropriate role** in GitHub
5. **Move story back** to appropriate state

**Example:**
```
@tech-lead: Escalation needed

Issue: Story #45 criterion 3 states "endpoint must be idempotent" but 
no test verifies idempotency. Unclear what level of idempotency is required.

Request: Clarify requirement or update test plan.

Blocking approval until resolved.
```

---

## QA Role Prompts (Quick Reference)

### Starting Review
```
[Role: Reviewer/QA]

Review PR #<pr-id> against Story #<story-id> and Epic #<epic-id>.

Apply the QA Review Checklist:
1. Pre-review validation (PR links, template, CI)
2. Success criteria validation (map each to evidence)
3. Test coverage review (happy path + edge cases)
4. Code quality assessment (no unrelated changes)
5. Documentation review (README, API docs)
6. Integration check (no regressions)

Decision: Approve with evidence OR Request changes with concrete feedback.
```

### Manual Testing
```
[Role: Reviewer/QA]

Perform manual testing for PR #<pr-id>:
1. Checkout branch: gh pr checkout <pr-id>
2. Start service: python -m src.service.app
3. Test each endpoint/feature per success criteria
4. Test error cases
5. Test responsive layouts (if frontend)
6. Document results

Provide test evidence in review comment.
```

### Escalation
```
[Role: Reviewer/QA]

Escalation needed for PR #<pr-id>:

Issue: <clear description of blocker>
Impacted: Story #<story-id>, criterion <X>
Escalate to: <Tech Lead | PO | Release/DevOps>
Reason: <why this blocks approval>

Blocking approval until resolved.
```

---

## Summary: QA as Quality Gate

**QA's Core Value:**
- Validates implementation against requirements (not just "code works")
- Ensures test coverage is sufficient (not just "tests pass")
- Catches scope creep early (before merge)
- Maintains workflow discipline (gate enforcement)
- Provides concrete, actionable feedback (not just "looks wrong")

**QA Empowerment:**
- **Can block any PR** that doesn't meet DoD
- **Can escalate unclear requirements** back to Tech Lead/PO
- **Can reject incomplete PR templates** (no review until complete)
- **Can request story split** if scope too large

**QA Success:**
- High approval rate (good specs + implementation)
- Low defect leakage (quality caught before release)
- Fast turnaround (efficient review process)
- Clear feedback (implementers learn and improve)

**Remember:** QA is not about finding reasons to say "no" — it's about ensuring we ship quality work that meets the agreed-upon requirements. QA protects the team from technical debt and the users from broken features.

---

## Related Documentation

- [RULEBANK.md](../RULEBANK.md) - DoR/DoD definitions
- [ROLE_PROMPTS.md](ROLE_PROMPTS.md) - Detailed role prompts including QA
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Full workflow walkthrough
- [QUICKSTART.md](QUICKSTART.md) - Fast 30-minute test

**QA is Role 4 in the 5-role workflow. Make every review count!** ✅
