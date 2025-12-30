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
- **Note:** PO should be available for clarification questions from Tech Lead

---

## Phase 1.5: PO-Tech Lead Initial Collaboration (Before Spec Ready)

### Collaboration Pattern: Tech Lead Questions → PO Clarifies

⚠️ **This phase is critical for preventing downstream rework. Tech Lead MUST NOT proceed to Spec Ready without clarifying ambiguities.**

**Tech Lead Review & Question (on Issue #1):**
```
@PO - Initial review of Idea Issue #1. Need clarification before creating Epic/Stories:

**Understanding Check:**
- [ ] Confirmed: This is for v0.1.0 baseline (not full observability suite)
- [ ] Confirmed: Target is internal monitoring (not customer-facing)

**Clarification Needed:**

1. **Success Criteria 1 (Health endpoint):**
   - Q: What should health check validate? (service alive only, or dependencies too?)
   - Q: Should it include timestamp or version info?
   - Q: What status codes for unhealthy? (503, 500, other?)

2. **Success Criteria 2 (Metrics endpoint):**
   - Q: "Request count" - all requests or just to /metrics itself?
   - Q: "Uptime" - since process start or something else?
   - Q: Any specific format needed (JSON, Prometheus, plain text)?
   - Q: Do we need any rate/gauge metrics or just counters?

3. **Edge Cases & Error Handling:**
   - Q: What happens if service is starting up but not ready?
   - Q: Should /metrics track errors separately?
   - Q: Rate limiting needed on these endpoints?

4. **Scope & Dependencies:**
   - Q: Priority order: health first, then metrics? Or parallel?
   - Q: Any infrastructure dependencies (load balancer, monitoring tool)?
   - Q: Target timeline for v0.1.0?

5. **Testing Strategy:**
   - Q: ">90% coverage" - is this per-file or overall project?
   - Q: Do you want integration tests or unit tests sufficient?

**Blocker:** Cannot mark Spec Ready until these are answered.

CC: @implementer for technical feasibility input once clarified.
```

**PO Response (same thread):**
```
@tech-lead - Good questions! Here are clarifications:

**Success Criteria 1 (Health endpoint):**
- A: Health check should validate service alive only (no dependency checks in v0.1.0)
- A: Include timestamp (ISO8601 UTC) - helpful for debugging
- A: Only 200 expected - if service is up, it's healthy (dependencies out of scope)

**Success Criteria 2 (Metrics endpoint):**
- A: Request count = total requests to ALL endpoints (not just /metrics)
- A: Uptime = seconds since service process started
- A: JSON format (consistent with /health)
- A: Just these 2 metrics for v0.1.0 (counters only, no gauges/rates)

**Edge Cases & Error Handling:**
- A: No startup grace period needed - if endpoint responds, it's ready
- A: No separate error tracking in v0.1.0 (keep simple)
- A: No rate limiting (internal use only)

**Scope & Dependencies:**
- A: Parallel development OK (health and metrics independent)
- A: No infrastructure dependencies - standard HTTP endpoints
- A: Target: Ship v0.1.0 in 1 week (assuming 2 implementers)

**Testing Strategy:**
- A: >90% coverage = per-file for new code (health.py, metrics.py routes)
- A: Unit tests sufficient for v0.1.0 (integration tests in v0.2.0)

**Updated Success Criteria (refined):**
1. GET /health returns 200 with JSON: {"status":"ok", "timestamp":"<ISO8601>"}
2. GET /metrics returns 200 with JSON: {"requests_total":<int>, "uptime_seconds":<int>}
3. Unit tests achieve >90% coverage per file (test_health.py, test_metrics.py)
4. README documents both endpoints with curl examples
5. Service runs via `python -m src.service.app` with clear instructions

**Non-goals remain unchanged.**

@tech-lead - Ready for you to create Epic + Stories now. Let me know if any other questions!
```

**Tech Lead Acknowledgment:**
```
@PO - Perfect, all clarified! Summary of understanding:

**Scope Confirmed:**
- Health: Liveness check only (200 + timestamp)
- Metrics: Total requests + uptime (in-memory counters)
- Format: JSON for both
- Tests: Unit tests, >90% per-file coverage
- Timeline: 1 week (parallel development)

**Assumptions Documented:**
- No dependency health checks
- No error tracking in v0.1.0
- No rate limiting (internal use)
- No startup grace period

**Next Steps:**
1. Create Epic #2 with these clarifications
2. Split into 3 Stories: Health, Metrics, CI/Release
3. Add architecture notes (Flask, in-memory state)
4. Validate technical feasibility with implementer
5. Mark Spec Ready once DoR satisfied

Will proceed now. Thanks!
```

---

## Phase 2: Tech Lead Converts to Epic + Stories

### Role: Tech Lead/Architect

⚠️ **Tech Lead must challenge unclear requirements and collaborate with PO/Implementers - not just accept everything passively.**

**NOTE:** Phase 1.5 (PO-Tech Lead collaboration) should be complete before starting this phase.

### Step 1: Validate Technical Feasibility with Implementers

**After PO clarifications (Phase 1.5), validate with implementers before creating stories:**

```
@implementer - Technical feasibility check (based on PO's clarifications):

**Proposed Implementation:**
1. Story: Health endpoint - GET /health returns 200 + {status, timestamp}
2. Story: Metrics endpoint - GET /metrics returns 200 + {requests_total, uptime_seconds}
3. Story: CI setup - GitHub Actions (lint, test, coverage)

**Technical Approach:**
- Framework: Flask (lightweight, well-documented)
- State: In-memory counters (REQUEST_COUNT, START_TIME globals)
- Tests: pytest with Flask test_client
- Coverage: pytest-cov, >90% per file

**Questions for Implementer:**
- Any blockers with Flask + in-memory state approach?
- Rough effort estimate per story (S/M/L)?
- Concerns about test coverage target (>90%)?
- Any spikes needed (e.g., Flask setup, metrics tracking)?
- Preferred development order (health first, or parallel)?

**Waiting for implementer feedback before creating Epic/Stories.**
```

**Implementer Response:**
```
@tech-lead - Feasibility looks good. Feedback:

**Technical Approach:**
- ✅ Flask is perfect for this (no blockers)
- ✅ In-memory state works for v0.1.0 (no persistence needed)
- ✅ pytest + test_client is standard approach
- ✅ >90% coverage achievable (routes are simple)

**Effort Estimates:**
- Story 1 (Health): Small (2-3 hours) - straightforward endpoint + tests
- Story 2 (Metrics): Small-Medium (3-4 hours) - need request counter hook + tests
- Story 3 (CI): Small (1-2 hours) - standard GitHub Actions template

**Recommendations:**
- Do health first (validates Flask setup)
- Metrics second (builds on health pattern)
- CI last (validates both endpoints)
- No spike needed (Flask + pytest are well-known)

**Potential Issues:**
- REQUEST_COUNT needs thread-safe increment (use lock or atomic)
- START_TIME should be module-level (not per-request)
- CI should run on PRs + main (not just main)

**Ready to start once stories are created!**
```

**Tech Lead Acknowledgment:**
```
@implementer - Thanks! Noted on thread safety and module-level START_TIME.

**Updated Plan:**
- Add threading.Lock for REQUEST_COUNT in architecture notes
- Document START_TIME initialization in story acceptance criteria
- CI to run on pull_request + push events

Proceeding to create Epic + Stories now.
```

### Step 2: Create Epic + Stories (After Both PO & Implementer Validation)

**Only after clarifying with PO and validating feasibility:**

**Prompt to use:**
```
[Role: Tech Lead/Architect]

Take Issue #1 (Service readiness baseline) and convert to:
1. Epic tracking overall v0.1.0 delivery (document Q&A with PO and implementer)
2. Story A: Health endpoint implementation
3. Story B: Metrics endpoint implementation  
4. Story C: CI setup and release hygiene

For each story, add:
- API contract (endpoint, request/response format, status codes)
- Test plan (unit tests required, edge cases)
- Acceptance criteria mapped to parent Epic
- Branch naming convention
- Technical notes from implementer feedback
- Assumptions documented

Architecture notes (add to Epic):
- Use Flask (lightweight, well-known) - validated with implementer
- Health: stateless check, returns 200 with {status:ok, timestamp:ISO8601}
- Metrics: in-memory counters with thread-safe increment (threading.Lock)
  - REQUEST_COUNT: global counter incremented via @app.before_request hook
  - START_TIME: module-level timestamp (initialized on import)
  - Endpoint returns: {requests_total:<int>, uptime_seconds:<int>}
- Tests: pytest with Flask test client
- CI: GitHub Actions (lint, test, coverage report) on pull_request + push events
- Coverage target: >90% per file for new code
- Development order: Health → Metrics → CI (sequential dependency)
- Technical risks: None identified (Flask + pytest well-established)
- Thread safety: REQUEST_COUNT uses lock (per implementer feedback)

**Document in Epic (reference Phase 1.5 conversation):**
- Questions asked to PO (with links to comments)
- PO's clarifications (summarized)
- Implementer feedback on feasibility (with links)
- Assumptions made and validated:
  - No dependency health checks (confirmed with PO)
  - No error tracking in v0.1.0 (confirmed with PO)
  - In-memory state acceptable (confirmed with implementer)
  - Thread-safe counters needed (identified by implementer)

Mark stories as "Spec Ready" only after validating Definition of Ready AND PO confirms understanding.
```

**Expected output:**
- Epic #2 created with label `epic`
  - Includes summary of Phase 1.5 PO-Tech Lead conversation (with comment links)
  - Includes summary of implementer feasibility validation (with comment links)
  - Includes architecture notes with technical decisions documented
- Story #3: Health endpoint (label `story`, linked to Epic #2, DoR satisfied)
- Story #4: Metrics endpoint (label `story`, linked to Epic #2, DoR satisfied)
- Story #5: CI & Release (label `story`, linked to Epic #2, DoR satisfied)
- Architecture comment added to Epic #2 (includes technical risks, assumptions, Q&A references)
- All stories moved to `Spec Ready` column
- **Final PO confirmation comment:** PO reviews Epic + Stories and confirms alignment with original intent

---

## Phase 2.5: PO Reviews Spec (Before Implementation Starts)

### Collaboration Pattern: Tech Lead Shares Spec → PO Validates

⚠️ **PO must validate that stories accurately reflect the original intent before implementation begins.**

**Tech Lead Request for PO Review (on Epic #2):**
```
@PO - Epic #2 and Stories #3-5 created based on our conversation (Phase 1.5).

**Please review and confirm:**

1. **Epic Scope:** Does Epic #2 accurately represent the "Service readiness baseline" vision?
2. **Story Split:** Are Stories #3-5 (Health, Metrics, CI) the right decomposition?
3. **Success Criteria:** Do story acceptance criteria match your expectations from Issue #1?
4. **Architecture Notes:** Any concerns with Flask + in-memory state approach?
5. **Assumptions:** Review documented assumptions - any misalignments?

**Changes from original Issue #1:**
- Refined health endpoint to include timestamp (based on your clarification)
- Specified metrics as requests_total + uptime_seconds (per your guidance)
- Added thread-safe counter requirement (from implementer feedback)
- Defined test coverage as per-file >90% (per your clarification)

**Key References:**
- Original Idea: Issue #1
- PO Clarifications: [link to Phase 1.5 comment thread]
- Implementer Feasibility: [link to feasibility comment]

**Blocker:** Please confirm before I mark "Spec Ready" and assign to implementers.

Expected: "Confirmed, proceed" OR "Change needed: <specific feedback>"
```

**PO Review & Confirmation:**
```
@tech-lead - Reviewed Epic #2 and Stories #3-5. Looks excellent!

**Confirmations:**
✅ Epic scope matches vision (Service readiness baseline v0.1.0)
✅ Story split makes sense (independent, testable units)
✅ Success criteria align with Issue #1 (well-refined)
✅ Architecture approach approved (Flask + in-memory for v0.1.0)
✅ Assumptions documented correctly

**Appreciated additions:**
- Thread-safe counters (good catch by implementer)
- Explicit API contracts (helpful for testing)
- Development order (health first makes sense)

**One minor clarification:**
- Story #4 (Metrics) acceptance criteria mentions "requests_total increments correctly"
  - Suggested: Add test case "test_metrics_increments_after_each_request"
  - This ensures counter hook works properly

**Decision: Confirmed, proceed to Spec Ready.**

@implementers - Stories ready for pickup once Tech Lead marks Spec Ready. Prioritize Story #3 (Health) first per architecture notes.
```

**Tech Lead Final Update:**
```
@PO - Thanks for confirmation!

**Updated:**
- Story #4 acceptance criteria now includes explicit test case: test_metrics_increments_after_each_request

**Status Change:**
- Moving Stories #3, #4, #5 to "Spec Ready"
- Epic #2 ready for implementation
- DoR satisfied for all stories

@implementers - Stories #3, #4, #5 now available. Please start with #3 (Health) as discussed.
```

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

## Phase 3A.5: Implementer-Tech Lead Clarification (If Needed During Implementation)

### Collaboration Pattern: Implementer Questions → Tech Lead Answers

⚠️ **If implementer discovers ambiguity or technical issues during implementation, stop and clarify before proceeding.**

**Example: Implementer Discovers Ambiguity (comment on Story #3):**
```
@tech-lead - Question during implementation of Story #3:

**Issue Found:**
Story acceptance criteria says "returns 200 with timestamp" but doesn't specify:
1. Timestamp format: ISO8601 with timezone? UTC only? Milliseconds?
2. Timestamp source: Server time or request time?
3. Timestamp key name: "timestamp", "time", "checked_at"?

**Current Understanding:**
From Epic #2 architecture notes: "timestamp:ISO8601"
From PO clarification (Phase 1.5): "Include timestamp (ISO8601 UTC)"

**Proposed Implementation:**
```python
{
  "status": "ok",
  "timestamp": "2024-01-15T14:30:00Z"  # ISO8601 UTC with 'Z' suffix
}
```

**Questions:**
- Is this format correct?
- Should I use `datetime.utcnow().isoformat() + 'Z'` or `datetime.now(timezone.utc).isoformat()`?
- Do we want seconds precision or milliseconds?

**Blocker:** Need confirmation before completing implementation.
```

**Tech Lead Response:**
```
@implementer - Good catch! Here's the spec:

**Timestamp Format (Definitive):**
- ISO8601 with UTC timezone indicator ('Z' suffix)
- Seconds precision (no milliseconds needed for health check)
- Use: `datetime.utcnow().isoformat() + 'Z'`
- Example: `"2024-01-15T14:30:00Z"`
- Key name: `"timestamp"` (as shown in Epic #2)

**Rationale:**
- ISO8601 is universally parseable
- UTC avoids timezone confusion
- Seconds precision sufficient (not measuring latency)
- 'Z' suffix is standard UTC indicator

**Test Validation:**
Add test case: `assert response['timestamp'].endswith('Z')` to verify format.

**Updated Story #3 acceptance criteria** to include: 
"Timestamp must be ISO8601 UTC format with 'Z' suffix (seconds precision)"

@PO - FYI, clarified timestamp format with implementer. No scope change, just specification detail.

Proceed with implementation!
```

**Implementer Acknowledgment:**
```
@tech-lead - Perfect, thanks! 

**Confirmed:**
- Using `datetime.utcnow().isoformat() + 'Z'`
- Added test: `test_health_timestamp_format()` that validates 'Z' suffix
- Updated implementation to match

Continuing with PR now.
```

---

## Phase 3A.75: Implementer-QA Early Collaboration (Optional but Recommended)

### Collaboration Pattern: Implementer Previews → QA Provides Early Feedback

⚠️ **For complex stories, implementer can request early QA review (before opening formal PR) to catch issues early.**

**Implementer Request for Early Review (comment on Story #3):**
```
@reviewer - Early review request (before formal PR):

**Status:** Implementation ~80% complete, want to validate approach before finalizing.

**Preview Available:**
- Branch: `feature/3-health-endpoint` (pushed but PR not opened yet)
- Commits: 2 commits (implementation + tests)
- Tests: 4/5 tests passing (edge case test WIP)

**Specific Questions:**
1. Does test coverage look sufficient for acceptance criteria?
2. Is timestamp format test adequate or should I add more cases?
3. README documentation clear enough?

**Not asking for full review** - just high-level feedback to avoid rework.

**Timeline:** Planning to open formal PR tomorrow, want to incorporate feedback first.
```

**QA Early Feedback:**
```
@implementer - Quick preview review (not formal):

**Test Coverage:** ✅ Looks good
- 4 tests cover happy path and structure
- Edge case test (multiple calls) is good addition

**Suggestions (before formal PR):**
1. **Timestamp test:** Consider adding test for "timestamp is recent" (e.g., within last 5 seconds)
   - This validates you're not returning a hardcoded timestamp
   - Example: `assert (datetime.utcnow() - parse(response['timestamp'])).seconds < 5`

2. **README docs:** Include example with curl output (not just command)
   - Shows what users should expect
   - Makes acceptance criteria validation easier

**Not blockers** - PR will likely be approved with current approach, but these would strengthen it.

Looking forward to formal review!
```

**Implementer Follow-up:**
```
@reviewer - Thanks! Incorporated both suggestions:

1. ✅ Added `test_health_timestamp_is_recent()` with 5-second window check
2. ✅ Updated README with curl command + example output

Opening formal PR now with these improvements.
```

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

### Phase 4.5: QA-Implementer Collaboration (Changes Requested)

### Collaboration Pattern: QA Identifies Issues → Implementer Fixes → QA Re-reviews

⚠️ **When QA requests changes, provide specific, actionable feedback. Implementer should ask clarifying questions if feedback is unclear.**

**Scenario A: QA Requests Changes (comment on PR #10):**
```
## QA Review: Changes Requested 🔄

### Issues Found

**Critical (must fix):**
- [ ] **Criterion 3 not fully met:** Timestamp format not validated in tests
  - Evidence: Tests check timestamp exists but not format (ISO8601 with 'Z')
  - Missing test: Validate timestamp ends with 'Z' and is parseable
  - Suggested fix: Add assertion in test_health_has_timestamp()
  - Code location: tests/test_health.py line 25

**Minor (should fix):**
- [ ] **Documentation incomplete:** README shows curl command but no example output
  - Expected: Show both command AND response (helps users validate)
  - Suggested addition: Include example output in README.md
  - Example format:
    ```bash
    $ curl http://localhost:5000/health
    {"status": "ok", "timestamp": "2024-01-15T14:30:00Z"}
    ```

### What's Working Well ✅
- Implementation logic correct
- Status code and JSON structure proper
- Edge case test (multiple calls) good addition

### Next Steps
1. Add timestamp format validation test
2. Enhance README with example output
3. Update PR description with new test evidence
4. Re-request review

Moving Story #3 back to "In Progress".
```

**Implementer Response (same PR thread):**
```
@reviewer - Thanks for specific feedback! Question on timestamp validation:

**Question:**
You mentioned "is parseable" - should I:
1. Just validate the format (ends with 'Z'), OR
2. Actually parse with datetime.fromisoformat() to ensure valid ISO8601?

**Proposed approach:**
```python
def test_health_timestamp_format():
    response = client.get('/health')
    timestamp = response.json['timestamp']
    # Check format
    assert timestamp.endswith('Z'), "Timestamp must have UTC 'Z' suffix"
    # Check parseable (remove 'Z' since fromisoformat doesn't handle it)
    datetime.fromisoformat(timestamp[:-1])  # Will raise if invalid
```

Is this what you're looking for?
```

**QA Clarification:**
```
@implementer - Perfect! That's exactly the validation needed.

**Confirmed approach:**
- ✅ Check 'Z' suffix (ensures UTC marker)
- ✅ Parse with fromisoformat (ensures valid ISO8601)
- ✅ Removing 'Z' before parsing is correct (Python quirk)

**Optional enhancement:** You could also assert timestamp is "recent" (within last 5 seconds) to ensure it's not hardcoded, but not required for this story.

Proceed with your proposed approach!
```

**Implementer Update:**
```
@reviewer - Changes implemented:

**Fixed:**
1. ✅ Added timestamp format validation test (as discussed)
   - Validates 'Z' suffix
   - Validates parseable ISO8601
   - Added optional "recency" check (within 5 seconds)
2. ✅ Enhanced README with curl command + example output

**Updated PR:**
- New commit: "Add timestamp format validation and enhance README"
- Test coverage still >90%
- All tests passing locally
- Updated "Test Evidence" section in PR description

**Re-requesting review now.**
```

**QA Re-Review & Approval:**
```
## QA Review: Approved ✅ (Re-review after fixes)

### Changes Validated
1. ✅ Timestamp format test added (tests/test_health.py line 30-35)
   - Validates 'Z' suffix ✅
   - Validates parseable ISO8601 ✅
   - Bonus: Validates timestamp recency ✅
2. ✅ README enhanced with example output (README.md lines 45-48)

### Success Criteria Validation (Complete)
1. ✅ Endpoint returns 200 → test_health_returns_200 (PASSING)
2. ✅ JSON format correct → test_health_returns_json (PASSING)
3. ✅ Status is "ok" → test_health_has_status_ok (PASSING)
4. ✅ Timestamp format validated → test_health_timestamp_format (PASSING)
5. ✅ Edge cases covered → test_health_multiple_calls (PASSING)

### Test Coverage
- ✅ 5 tests added (all passing)
- ✅ Coverage: 100% of health endpoint code
- ✅ Happy path + edge cases covered

### Code Quality
- ✅ No unrelated changes
- ✅ Naming conventions followed
- ✅ Documentation complete

### CI Status
- ✅ All checks passing (32 tests in 2.8s)

**Approved for merge.** Great collaboration on getting this right!

Moving Story #3 to "Done".
```

**Scenario B: QA Escalates Ambiguity to Tech Lead (comment on PR #10):**
```
## QA Review: Escalation Needed ⚠️

@tech-lead - Cannot complete review due to ambiguity in Story #3 acceptance criteria.

**Issue:**
Story #3 criterion 2 states: "Timestamp must be ISO8601 UTC format"

**Ambiguity:**
Implementation uses `datetime.utcnow().isoformat() + 'Z'` which produces:
- Format: `2024-01-15T14:30:00Z` (seconds precision)

But I cannot find specification for:
1. Should milliseconds be included? (`2024-01-15T14:30:00.123Z`)
2. Is seconds precision acceptable?
3. What's the source of truth for this decision?

**Blocking approval** until this is clarified (can't validate acceptance criteria without clear spec).

**Request:** Please clarify expected timestamp precision in Story #3 or Epic #2 architecture notes.

CC: @implementer - Hold on changes until Tech Lead clarifies.
```

**Tech Lead Response:**
```
@reviewer @implementer - Good catch on ambiguity. Here's the clarification:

**Decision: Seconds precision is correct.**

**Rationale:**
1. From PO clarification (Phase 1.5): "Include timestamp (ISO8601 UTC) - helpful for debugging"
2. Use case: Health check debugging (when was endpoint last responsive)
3. Millisecond precision not needed (not measuring latency)
4. Simpler format = easier to read in logs

**Updated Story #3 acceptance criteria:**
- "Timestamp must be ISO8601 UTC format with seconds precision (no milliseconds)"

**Source of truth:** Epic #2 architecture notes (now updated)

@reviewer - Please proceed with review using seconds precision as standard.
@implementer - No changes needed, your implementation is correct.
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

## Phase 5.5: Release-PO Final Validation (Post-Release Confirmation)

### Collaboration Pattern: Release Ships → PO Validates Release → Close Epic

⚠️ **PO should validate that the release meets the original vision before Epic is closed.**

**Release/DevOps Notification (comment on Epic #2):**
```
@PO - v0.1.0 released! Ready for your final validation.

**Release Details:**
- Tag: v0.1.0
- Release Notes: https://github.com/org/repo/releases/tag/v0.1.0
- Deployed: Production (or staging, if applicable)

**Delivered Features:**
1. ✅ GET /health endpoint - Returns 200 with status + timestamp
2. ✅ GET /metrics endpoint - Returns request count + uptime
3. ✅ Unit tests with >90% coverage per file
4. ✅ README documentation with examples
5. ✅ CI/CD pipeline (lint, test, coverage)

**Validation Checklist for PO:**
- [ ] Test /health endpoint: `curl https://api.example.com/health`
- [ ] Test /metrics endpoint: `curl https://api.example.com/metrics`
- [ ] Review README documentation
- [ ] Verify original Issue #1 requirements met

**Please confirm:**
"Validated, meets requirements" OR "Issue found: <details>"

Once confirmed, I'll close Epic #2 and mark all stories "Released".
```

**PO Validation & Confirmation:**
```
@release - Validated v0.1.0 against original requirements. Excellent work!

**Validation Results:**

✅ **Requirement 1:** Service has GET /health endpoint that returns 200 with status:ok
   - Tested: `curl https://api.example.com/health`
   - Result: `{"status":"ok","timestamp":"2024-01-15T14:30:00Z"}`
   - Status: ✅ PASSED

✅ **Requirement 2:** Service has GET /metrics endpoint with request count + uptime
   - Tested: `curl https://api.example.com/metrics`
   - Result: `{"requests_total":42,"uptime_seconds":3600}`
   - Status: ✅ PASSED

✅ **Requirement 3:** Both endpoints have unit tests with >90% coverage
   - Verified: CI test output shows 95% coverage
   - Status: ✅ PASSED

✅ **Requirement 4:** README documents both endpoints with examples
   - Verified: README has clear curl examples + expected output
   - Status: ✅ PASSED

✅ **Requirement 5:** Service can be run locally with clear instructions
   - Verified: README instructions work (`python -m src.service.app`)
   - Status: ✅ PASSED

**Decision: Confirmed, release meets all requirements from Issue #1.**

**Feedback for future iterations:**
- Response times are fast (<50ms) - great for health checks
- Consider adding /metrics in Prometheus format for v0.2.0 (was in non-goals)
- Documentation is clear and helpful

**Approved to close Epic #2.** Thank you team!

@tech-lead @implementers @reviewer - Great collaboration throughout this Epic! 🎉
```

**Release/DevOps Final Actions:**
```
@PO - Thanks for validation!

**Final Actions Completed:**
1. ✅ Closed Epic #2 (all requirements met)
2. ✅ Moved Stories #3, #4, #5 to "Released" status
3. ✅ Updated CHANGELOG.md with v0.1.0 entry
4. ✅ Updated project board (all items in "Released" column)

**Traceability Map (for audit):**
- Idea: Issue #1 (PO)
- Epic: Issue #2 (Tech Lead, includes PO/Implementer Q&A)
- Stories: #3 (Health), #4 (Metrics), #5 (CI)
- PRs: #10 (Health), #11 (Metrics), #12 (CI)
- Release: v0.1.0 (includes all stories)

**v0.1.0 is now officially shipped!** 🚀

**For v0.2.0 planning:** PO suggested Prometheus format for metrics - creating placeholder Issue for future consideration.
```

**Scenario B: PO Finds Issue Post-Release (comment on Epic #2):**
```
@release - Issue found during validation. Not blocking release but needs follow-up.

**Validation Results:**

✅ Requirements 1-4: PASSED (as detailed above)

⚠️ **Requirement 5:** Service run instructions partially incomplete
   - Issue: README says `python -m src.service.app` but doesn't mention port
   - Impact: Users may not know how to access endpoints (http://localhost:5000)
   - Severity: Minor (workaround: check console output)
   - Fix needed: Add "Service runs on http://localhost:5000" to README

**Decision: Approve release (requirements met), but create follow-up issue for documentation enhancement.**

**Request:**
1. Approve closing Epic #2 (core functionality delivered)
2. Create Issue #6: "Enhance README with port/URL information" (label: documentation, chore)
3. Target Issue #6 for v0.1.1 patch or v0.2.0

Not blocking team, just want docs improved for next users.
```

**Release/DevOps Response:**
```
@PO - Understood, agreed on approach.

**Actions Taken:**
1. ✅ Created Issue #6: "Enhance README with service URL information"
   - Label: documentation, chore
   - Milestone: v0.1.1
   - Linked to Epic #2 (post-release follow-up)
2. ✅ Closed Epic #2 (core requirements met)
3. ✅ Updated release notes to mention Issue #6 as known documentation gap

**Epic #2 Status:** CLOSED (successfully delivered)
**Follow-up:** Issue #6 tracked separately

Thanks for thorough validation!
```

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
