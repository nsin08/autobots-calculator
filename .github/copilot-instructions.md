# Copilot Instructions: Autobots Lifecycle Demo

## Project Overview
This is a **demonstration project** for a complete 5-role GitHub lifecycle workflow (Intake → Spec → Implementation → Review → Release). The actual service code (Flask API with `/health` and `/metrics` endpoints) is minimal—the **real value is in the workflow mechanics and artifact discipline**.

## Core Architecture

### Workflow State Machine
All work flows through: `Intake → Spec Ready → In Progress → In Review → Done → Released`  
**Critical:** Never skip states. Each transition has entry/exit criteria defined in [RULEBANK.md](../RULEBANK.md).

### 5 Roles & Handoffs
1. **Sponsor/PO** (Intake) — Creates Idea Issues with problem statement and success criteria
2. **Tech Lead/Architect** (Spec Ready) — Converts to Epic + Stories with API contracts and test plans
3. **Implementer** (In Progress → PR) — Builds features, tests, docs; opens PRs
4. **Reviewer/QA** (In Review) — Validates PRs against success criteria
5. **Release/DevOps** (Release) — Tags versions, generates release notes

### Artifact Linking (Non-negotiable)
- Every Story/Task **must** link to parent Epic via `Parent: #<id>` in body
- Every PR **must** link via `Closes #<id>` to exactly one Issue
- Maintain full traceability: Idea → Epic → Story → Branch → PR → Release
- See [RULEBANK.md](../RULEBANK.md) lines 17-20 for enforcement rules

## Implementation Patterns

### Service Code (src/service/)
- **Minimal Flask app**: Single [app.py](../src/service/app.py) with global counters `REQUEST_COUNT`, `START_TIME`
- **No external databases**: All state is in-memory (intentionally simple)
- **Endpoint pattern**: Each endpoint returns `jsonify({...}), status_code` tuple
- **Request tracking**: Global `@app.before_request` hook increments counter

### Testing (tests/)
- **Fixture-based**: All tests use `client` fixture from `app.test_client()`
- **Test naming**: `test_<endpoint>_<behavior>` (e.g., `test_health_endpoint_returns_200`)
- **Coverage target**: >90% per story acceptance criteria
- Run: `pytest tests/` (no additional config needed)

### Branch Naming
- Features: `feature/<issue-id>-<slug>` (e.g., `feature/2-health-endpoint`)
- Chores: `chore/<issue-id>-<slug>`
- **Never** push to `main` directly—always PR from feature branch

## Critical Workflows

### When Acting as Implementer
1. Read Story success criteria line-by-line (in issue body under "Success Criteria")
2. Create branch following naming convention above
3. Implement **only** what's in success criteria (no extra features)
4. Add tests that directly prove each criterion
5. Update README with endpoint examples
6. Open PR using [PULL_REQUEST_TEMPLATE.md](../PULL_REQUEST_TEMPLATE.md)—fill **every section** (no placeholders)
7. Map each success criterion to evidence (file paths, test names, CI output)

### When Opening PRs
- **Template compliance is mandatory**: See [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
- Fill "Mapping to Success Criteria" section with concrete evidence (e.g., "✅ Criterion 1: Endpoint returns 200 → Evidence: `test_health_endpoint_returns_200` in [tests/test_health.py](../tests/test_health.py#L13-L16)")
- Include test output in "Test Evidence" section
- Keep PRs small: 1 story per PR, 1-3 commits, no drive-by refactors

### When Acting as Tech Lead
⚠️ **Tech Lead must challenge unclear requirements and collaborate - not just accept everything passively.**

**Before creating Epic/Stories:**
- Question the PO if requirements are unclear (comment on Idea Issue)
- Challenge assumptions: Is this needed? Is scope too large? Technical risks?
- Validate feasibility with implementers: effort estimate, blockers, dependencies
- Push back if success criteria are not measurable or edge cases missing
- Document Q&A with PO in Epic (what was clarified, what assumptions made)

**When creating Epic/Stories:**
- Split Epics into Stories that are independently testable
- Add "Architecture Note" comments to Epic with:
  - API contracts (endpoint, request/response shape, status codes)
  - Test strategy (unit/integration scope)
  - Dependencies between stories
  - Technical risks/unknowns
  - Assumptions validated with PO
- Example from Story #2: "GET /health → 200 {status:ok, timestamp:ISO8601} → Unit tests: status code, JSON shape, timestamp format"

**Do NOT mark "Spec Ready" unless:**
- [ ] Success criteria are measurable
- [ ] Edge cases identified
- [ ] Non-goals stated
- [ ] Technical feasibility validated
- [ ] PO confirms understanding
- [ ] DoR satisfied

### When Acting as Reviewer/QA
⚠️ **QA is the quality gate between implementation and release.**

- Follow comprehensive QA protocols in [docs/QA_GUIDE.md](../docs/QA_GUIDE.md)
- Apply QA Review Checklist (pre-review, criteria validation, testing, code quality, docs, integration)
- Perform manual testing for frontend/API changes (browser testing, responsive layouts, error states)
- Provide concrete, actionable feedback with specific file/line references
- Block PRs that don't meet Definition of Done
- Escalate ambiguous requirements or scope creep

See [docs/QA_GUIDE.md](../docs/QA_GUIDE.md) for:
- Step-by-step review process
- Manual testing protocols
- Anti-patterns to avoid
- Escalation procedures
- Quality metrics tracking

## Role Prompts
When invoking Copilot for lifecycle tasks, **always prefix** with role-specific prompt from [docs/ROLE_PROMPTS.md](../docs/ROLE_PROMPTS.md). Example:
```
[Role: Implementer]
Pick Story #3 (metrics endpoint) and implement following the PR template.
```

See [docs/ROLE_PROMPTS.md](../docs/ROLE_PROMPTS.md) for complete prompt templates for each role.

## Definition of Done
Before marking any PR "ready for review":
- [ ] All acceptance criteria from Story met
- [ ] Tests added/updated and passing locally (`pytest tests/`)
- [ ] README updated with endpoint examples
- [ ] PR template **fully filled** (no "TODO" or placeholder text)
- [ ] Branch follows naming convention
- [ ] Linked to exactly one Issue via `Closes #<id>`

See [RULEBANK.md](../RULEBANK.md) lines 28-35 for complete DoD checklist.

## Common Commands
```bash
# Run service locally
python -m src.service.app  # Starts on http://localhost:5000

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Create issue via GH CLI
gh issue create --title "..." --label "story" --body-file .github/ISSUE_TEMPLATE/story-task.md

# Create PR from feature branch
gh pr create --title "..." --body "Closes #<id>, Epic #<epic-id>" --base main
```

## Anti-Patterns
- ❌ Creating PRs without filling template sections
- ❌ Adding features not in Story success criteria
- ❌ Breaking Issues/PRs into multiple unlinked artifacts
- ❌ Skipping tests ("will add later")
- ❌ Moving forward when DoR/DoD not satisfied
- ❌ Using generic commit messages ("fix", "update")—reference issue IDs

## Key Files to Reference
- [RULEBANK.md](../RULEBANK.md) — Non-negotiable workflow rules (read first!)
- [PROJECT_OVERVIEW.md](../PROJECT_OVERVIEW.md) — High-level goal and components
- [docs/ROLE_PROMPTS.md](../docs/ROLE_PROMPTS.md) — Exact prompts for each role
- [docs/QUICKSTART.md](../docs/QUICKSTART.md) — 30-min end-to-end test scenario
- [.github/ISSUE_TEMPLATE/](./ISSUE_TEMPLATE/) — Templates for Epic, Story, Review
