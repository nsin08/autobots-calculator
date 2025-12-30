# Workflow Execution Guide

Complete step-by-step guide to test the 5-role GitHub lifecycle workflow.

## Prerequisites

1. GitHub repository created and initialized
2. GitHub CLI (`gh`) installed and authenticated, OR GitKraken MCP tools available
3. GitHub Copilot with agent capabilities
4. Project board created with columns: `Intake`, `Spec Ready`, `In Progress`, `In Review`, `Done`, `Released`

## Use Case: Service Readiness Baseline v0.1.0

We'll build a minimal service with health & metrics endpoints through the complete lifecycle.

---

## Phase 1: PO Creates Idea (Intake)

### Role: Sponsor/PO

**Prompt to use:**
```
[Role: Sponsor/PO]

Create an Idea Issue for: "Service readiness baseline - health and observability endpoints"

Problem: We need a production-ready service with basic health checks and metrics for monitoring.

Success criteria:
1. Service has a GET /health endpoint that returns 200 with status:ok
2. Service has a GET /metrics endpoint that returns request count and uptime
3. Both endpoints have unit tests with >90% coverage
4. README documents both endpoints with examples
5. Service can be run locally with clear instructions

Non-goals:
- Advanced metrics (Prometheus format) - future iteration
- Authentication - not needed for health/metrics
- Distributed tracing - out of scope
- Load testing - not in MVP

Use the Idea/Story template and keep it focused.
```

**Expected output:**
- Issue #1 created with label `intake`
- Moved to `Intake` column on project board
- Assigned to Tech Lead

---

## Phase 2: Tech Lead Converts to Epic + Stories

### Role: Tech Lead/Architect

⚠️ **Tech Lead must challenge unclear requirements and collaborate with PO/Implementers - not just accept everything passively.**

### Step 1: Challenge and Clarify Requirements

**Before creating any stories, question the PO:**

```bash
# Review the PO's Idea Issue
gh issue view 1
```

**Ask these questions (comment on Issue #1):**
```
@PO - Questions before creating Epic/Stories:

1. **Success Criteria Clarity:**
   - You mentioned "service readiness baseline" - can you clarify priority: health vs metrics vs CI?
   - What does "working" mean for each endpoint? (concrete examples)
   - How will we know it's done? (acceptance test scenarios)

2. **Scope Boundaries:**
   - What's explicitly OUT of scope for v0.1.0?
   - Are there features you're tempted to add but we should defer to v0.2.0?
   - Target release timeline?

3. **Edge Cases:**
   - What happens when service is unhealthy?
   - How should errors be reported?
   - What metrics are critical vs nice-to-have?

4. **Dependencies:**
   - Does this depend on any infrastructure?
   - Any integration points?
   - Technical risks?

**I'll create the Epic + Stories once these are clarified.**
```

**If PO's response is vague, push back:**
```
@PO - Still unclear on health endpoint success criteria. 
Can you provide a concrete example?
E.g., "When service is healthy, GET /health returns 200 with {status:ok, timestamp:ISO8601}"

Cannot mark Spec Ready without measurable criteria.
```

### Step 2: Validate Technical Feasibility

**Before finalizing stories, validate with potential implementers:**

```
@implementer - Tech feasibility check:

Proposed Stories:
1. Story: Health endpoint (GET /health)
2. Story: Metrics endpoint (GET /metrics with counters)
3. Story: CI setup (GitHub Actions + linting)

Questions:
- Any technical blockers?
- Rough effort estimate (S/M/L per story)?
- Should we use Flask or FastAPI?
- Do we need a spike for metrics tracking approach?

**Response needed before I mark Spec Ready.**
```

### Step 3: Create Epic + Stories (After Clarification)

**Only after clarifying with PO and validating feasibility:**

**Prompt to use:**
```
[Role: Tech Lead/Architect]

Take Issue #1 (Service readiness baseline) and convert to:
1. Epic tracking overall v0.1.0 delivery (document Q&A with PO)
2. Story A: Health endpoint implementation
3. Story B: Metrics endpoint implementation  
4. Story C: CI setup and release hygiene

For each story, add:
- API contract (endpoint, request/response format, status codes)
- Test plan (unit tests required, edge cases)
- Acceptance criteria mapped to parent Epic
- Branch naming convention
- Assumptions documented

Architecture notes (add to Epic):
- Use Flask (lightweight, well-known) - validated with implementer
- Health: stateless check, always returns 200 unless service is down
- Metrics: in-memory counters (request_total, uptime_seconds)
- Tests: pytest with Flask test client
- CI: GitHub Actions (lint, test, coverage report)
- Technical risks: None identified
- Assumptions: No external dependencies required

**Document in Epic:**
- Questions asked to PO
- PO's clarifications
- Implementer feedback on feasibility
- Assumptions made

Mark stories as "Spec Ready" only after validating Definition of Ready AND PO confirms understanding.
```

**Expected output:**
- Epic #2 created with label `epic` (includes Q&A summary with PO)
- Story #3: Health endpoint (label `story`, linked to Epic #2)
- Story #4: Metrics endpoint (label `story`, linked to Epic #2)
- Story #5: CI & Release (label `story`, linked to Epic #2)
- Architecture comment added to Epic #2 (includes technical risks, assumptions)
- All stories moved to `Spec Ready` column
- PO confirms understanding (comment on Epic)

---

## Phase 3A: Implementer Builds Health Endpoint

### Role: Implementer

**Prompt to use:**
```
[Role: Implementer]

Pick Story #3 (Health endpoint implementation).

Create branch: feature/3-health-endpoint

Implement:
1. GET /health endpoint in src/service/app.py
   - Returns 200 status
   - JSON body: {"status": "ok", "timestamp": "<ISO 8601 UTC>"}
2. Unit tests in tests/test_health.py
   - test_health_returns_200
   - test_health_returns_json
   - test_health_has_status_ok  
   - test_health_has_timestamp
   - test_health_multiple_calls (edge case)
3. Update README.md with endpoint documentation

Then open PR using the PR template:
- Link to Story #3 and Epic #2
- Map each success criterion to code/test evidence
- Include test run output
- Fill risk/rollback section

Keep PR focused - no extra features.
```

**Expected output:**
- Branch `feature/3-health-endpoint` created
- Implementation in [src/service/app.py](src/service/app.py)
- Tests in [tests/test_health.py](tests/test_health.py)
- README updated with /health documentation
- PR #10 opened with complete template
- Story #3 moved to `In Review`

---

## Phase 3B: Implementer Builds Metrics Endpoint

### Role: Implementer

**Prompt to use:**
```
[Role: Implementer]

Pick Story #4 (Metrics endpoint implementation).

Create branch: feature/4-metrics-endpoint

Implement:
1. GET /metrics endpoint in src/service/app.py
   - Returns 200 status
   - JSON body: {"requests_total": <int>, "uptime_seconds": <int>}
   - Track request counter (global or app context)
   - Calculate uptime from service start time
2. Unit tests in tests/test_metrics.py
   - test_metrics_returns_200
   - test_metrics_returns_json
   - test_metrics_has_required_fields
   - test_metrics_request_count_increments
   - test_metrics_uptime_is_positive
3. Update README.md with /metrics documentation

Then open PR using the PR template:
- Link to Story #4 and Epic #2  
- Map each success criterion to evidence
- Include test output
- Note: depends on PR #10 being merged first (or handle in integration branch)

Keep PR small and focused.
```

**Expected output:**
- Branch `feature/4-metrics-endpoint` created
- Implementation in [src/service/app.py](src/service/app.py)
- Tests in [tests/test_metrics.py](tests/test_metrics.py)
- README updated with /metrics documentation
- PR #11 opened with complete template
- Story #4 moved to `In Review`

---

## Phase 4: Reviewer Validates PRs (QA Gate)

### Role: Reviewer/QA

⚠️ **QA is the quality gate between implementation and release.**  
📖 **See [QA_GUIDE.md](QA_GUIDE.md) for comprehensive QA protocols, manual testing procedures, and escalation paths.**

### Pre-Review Validation

Before detailed code review:

```bash
# Check PR status
gh pr view 10

# Verify CI status
gh pr checks 10
```

**Pre-Review Checklist:**
- [ ] PR linked to exactly one Issue
- [ ] Issue linked to parent Epic
- [ ] PR template fully filled (no placeholders)
- [ ] CI checks passing (green builds)
- [ ] Branch naming follows convention

**Stop Criteria:** If any fail, request changes immediately without code review.

### Review Process

**Prompt to use (for PR #10):**
```
[Role: Reviewer/QA]

Review PR #10 (Health endpoint) against Story #3 and Epic #2.

Apply the QA Review Checklist from QA_GUIDE.md:
1. Pre-review validation (PR links, template, CI)
2. Success criteria validation (map each to evidence):
   - Endpoint returns 200? → Code + test
   - Returns status:ok? → Code + test assertion
   - Has timestamp? → Code + test
   - Tests >90% coverage? → pytest --cov output
   - README updated? → README diff
3. Test coverage review (happy path + edge cases)
4. Code quality (no unrelated changes, naming conventions)
5. Documentation review (README, API docs)
6. Integration check (run tests locally)

Run locally:
  gh pr checkout 10
  pytest tests/test_health.py -v
  python -m src.service.app
  curl http://localhost:5000/health

Decision: Approve with evidence OR Request changes with concrete feedback.
```

### Manual Testing (If Needed)

For frontend or API changes:

**Backend API:**
```bash
# Test happy path
curl http://localhost:5000/api/calculate -X POST \
  -H "Content-Type: application/json" \
  -d '{"operation":"add","a":5,"b":3}'

# Test error case
curl http://localhost:5000/api/calculate -X POST \
  -H "Content-Type: application/json" \
  -d '{"operation":"divide","a":5,"b":0}'
```

**Frontend:** (Open browser to http://localhost:5000)
- Test interactions (buttons, inputs)
- Test responsive layouts (320px, 768px, 1024px+)
- Test error states
- Document results

See [QA_GUIDE.md](QA_GUIDE.md) section "Manual Testing Protocols" for detailed procedures.

### Decision: Approve OR Request Changes

#### If Approved ✅:
```bash
gh pr review 10 --approve --body "## QA Review: Approved ✅

### Success Criteria Validation
1. ✅ Endpoint returns 200 → test_health_endpoint_returns_200 (PASSING)
2. ✅ JSON format correct → test_health_json_structure (PASSING)
3. ✅ Timestamp ISO8601 → test_health_timestamp_format (PASSING)

### Test Coverage
- ✅ 3 tests added
- ✅ Happy path covered
- ✅ Coverage: 100% of app.py health endpoint

### Code Quality
- ✅ No unrelated changes
- ✅ Naming conventions followed

### CI Status
- ✅ All checks passing (30 tests in 2.5s)

**Approved for merge.**"

gh pr merge 10 --squash
```

#### If Changes Needed 🔄:
```bash
gh pr comment 10 --body "## QA Review: Changes Requested 🔄

### Issues Found

**Critical (must fix):**
- [ ] Criterion 3 not met: No test validates timestamp format
  - Evidence missing: test_health_timestamp_is_iso8601
  - Suggested fix: Add test in tests/test_health.py
  - Pattern: assert response['timestamp'].endswith('Z')

### Next Steps
1. Add missing test
2. Update PR with evidence
3. Re-request review

Moving story back to 'In Progress'."
```

**Expected output:**
- Review comment on PR #10 with checklist completed
- Either:
  - ✅ Approved → Merge PR → Story #3 moves to `Done`
  - 🔄 Changes requested → Story #3 back to `In Progress` with actionable feedback

**Repeat for PR #11 (Metrics endpoint)**

For comprehensive QA guidance including anti-patterns, escalation procedures, and quality metrics, see [QA_GUIDE.md](QA_GUIDE.md).

---

## Phase 5: Release/DevOps Ships v0.1.0

### Role: Release/DevOps

**Prompt to use:**
```
[Role: Release/DevOps]

PRs #10 and #11 are merged to main. Story #5 (CI/Release) is complete.

Verify:
1. CI is green on main branch
2. All tests passing
3. All Epic #2 stories are in "Done"

Then:
1. Create tag v0.1.0
2. Generate release notes from PRs:
   - List features added (#10 Health endpoint, #11 Metrics endpoint)
   - Include "Closes Epic #2"
3. Create GitHub Release with notes
4. Move Epic #2 to "Released"
5. Update CHANGELOG.md (if exists)

Use: gh release create v0.1.0 --title "v0.1.0 - Service Readiness Baseline" --notes "..."
```

**Expected output:**
- Git tag `v0.1.0` created
- GitHub Release created with notes
- Epic #2 moved to `Released` column
- All linked stories marked as shipped

---

## Verification: End-to-End Check

After completing the workflow, verify:

### Artifact Trail
- [ ] Epic #2 exists with 3 linked stories
- [ ] Story #3, #4, #5 all have PRs linked
- [ ] All PRs use the PR template
- [ ] All PRs have review comments
- [ ] All items moved through: Intake → Spec Ready → In Progress → In Review → Done → Released

### Code Quality
- [ ] `/health` endpoint returns 200 with correct JSON
- [ ] `/metrics` endpoint returns 200 with counters
- [ ] Tests pass: `pytest tests/`
- [ ] README documents both endpoints
- [ ] Service can run: `python -m src.service.app`

### Process Quality
- [ ] No status jumps (all gates respected)
- [ ] All templates used correctly
- [ ] PRs are small and focused
- [ ] Review feedback is concrete
- [ ] Release notes link back to issues

---

## Common Issues & Solutions

### Issue: PR template not filled
**Solution:** Reviewer requests changes with checklist of missing sections.

### Issue: Tests failing
**Solution:** Move story back to "In Progress", implementer fixes and updates PR.

### Issue: Scope creep in PR
**Solution:** Reviewer requests splitting - create new story for extra work.

### Issue: Missing architecture notes
**Solution:** Tech Lead cannot mark "Spec Ready" until architecture section complete.

### Issue: Unclear success criteria
**Solution:** Story goes back to PO for clarification before "Spec Ready".

---

## Next Steps

After completing this workflow once:

1. **Add complexity:** Try a feature requiring multiple branches that merge to integration branch
2. **Test gates:** Intentionally violate DoR/DoD and verify workflow blocks progress
3. **Automate checks:** Add GitHub Actions to enforce template completeness
4. **Scale up:** Run multiple stories in parallel with different implementers
5. **Add metrics:** Track cycle time (Intake → Released) per story

---

## Success Metrics

This workflow demonstrates:
- ✅ Full lifecycle from idea to release
- ✅ Multiple roles with clear handoffs
- ✅ Template-driven consistency
- ✅ Gate enforcement (DoR/DoD)
- ✅ Auditable artifact trail
- ✅ Small, reviewable PRs
- ✅ Automated testing
- ✅ Release hygiene

**The goal is proving the capability to operate the project lifecycle, not just "write code".**
