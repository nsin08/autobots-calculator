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

**Prompt to use:**
```
[Role: Tech Lead/Architect]

Take Issue #1 (Service readiness baseline) and convert to:
1. Epic tracking overall v0.1.0 delivery
2. Story A: Health endpoint implementation
3. Story B: Metrics endpoint implementation  
4. Story C: CI setup and release hygiene

For each story, add:
- API contract (endpoint, request/response format, status codes)
- Test plan (unit tests required, edge cases)
- Acceptance criteria mapped to parent Epic
- Branch naming convention

Architecture notes:
- Use Flask (lightweight, well-known)
- Health: stateless check, always returns 200 unless service is down
- Metrics: in-memory counters (request_total, uptime_seconds)
- Tests: pytest with Flask test client
- CI: GitHub Actions (lint, test, coverage report)

Mark stories as "Spec Ready" only after validating Definition of Ready.
```

**Expected output:**
- Epic #2 created with label `epic`
- Story #3: Health endpoint (label `story`, linked to Epic #2)
- Story #4: Metrics endpoint (label `story`, linked to Epic #2)
- Story #5: CI & Release (label `story`, linked to Epic #2)
- Architecture comment added to Epic #2
- All stories moved to `Spec Ready` column

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

## Phase 4: Reviewer Validates PRs

### Role: Reviewer/QA

**Prompt to use (for PR #10):**
```
[Role: Reviewer/QA]

Review PR #10 (Health endpoint) against Story #3 and Epic #2.

Use the Review Checklist:
1. Verify PR links to Story #3 and Epic #2
2. Check PR template is complete (no placeholders)
3. Validate each success criterion has evidence:
   - Endpoint returns 200? Check implementation + test
   - Returns status:ok? Check code + test assertion
   - Has timestamp? Check code + test
   - Tests have >90% coverage? Check test file
   - README updated? Check README diff
4. Run tests locally: pytest tests/test_health.py
5. Check for unrelated changes
6. Verify naming conventions

Decision: Approve OR Request Changes with specific feedback.
```

**Expected output:**
- Review comment on PR #10 with checklist completed
- Either:
  - ✅ Approved → Story #3 moves to `Done`
  - 🔄 Changes requested → Story #3 back to `In Progress` with actionable feedback

**Repeat for PR #11 (Metrics endpoint)**

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
