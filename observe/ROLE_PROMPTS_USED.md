# Role Prompts Used in Session

This document captures the exact role-based prompts and context that guided each phase of the workflow.

## Base Context

All roles operated with the following context:
- Project: Autobots Calculator
- Repository: https://github.com/nsin08/autobots-calculator
- RULEBANK rules enforced
- Template-driven workflow
- 5-role lifecycle: Sponsor → Tech Lead → Implementer → Reviewer → Release

---

## Role 1: Sponsor/PO

### Initial Prompt (Implicit)
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
> "i am a Sponsor, i want to start a project, i have idea to create a online calculator"

### Execution
- Initialized git repository
- Created GitHub repository: autobots-calculator
- Created Epic issue with:
  - Problem statement
  - 5 measurable success criteria
  - Clear scope (In/Out)
  - Target version v0.1.0

---

## Role 2: Tech Lead/Architect

### Initial Prompt (Implicit)
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

### User Input
> "yes" (to acting as Tech Lead)

### Execution
- Created 3 Story issues (#2, #3, #4) from Epic #1
- Each story included:
  - Context (parent Epic reference)
  - Requirements
  - Success Criteria (must be verifiable)
  - Test Plan
  - Deliverables
  - Branch name
- Added Architecture Notes comment to Epic:
  - API Contracts
  - Tech Stack
  - Test Strategy
  - Dependencies
  - Branch Strategy

---

## Role 3: Implementer

### Initial Prompt (Implicit)
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

### User Input (Story #2)
> "yes" (to implementing Story #2)

### Execution - Story #2
- Created branch: feature/2-backend-calculate-api
- Implemented POST /api/calculate endpoint
- Added 9 comprehensive tests
- Updated README with API documentation
- Committed with descriptive message
- Opened PR #5 with complete template:
  - All success criteria mapped to evidence
  - File paths and line numbers referenced
  - Test output included
  - Risk/rollback plan

### User Input (Story #3)
> "yes" (to implementing Story #3)

### Execution - Story #3
- Created branch: feature/3-frontend-calculator-ui
- Created static/index.html, style.css, app.js
- Updated Flask app to serve static files
- Updated README with UI usage instructions
- Committed with descriptive message
- Opened PR #6 with complete template

### User Input (Story #4)
> "Continue as Implementer and build Story #4 (CI/CD) first"

### Execution - Story #4
- Created branch: feature/4-ci-cd-setup
- Created .github/workflows/test.yml
- Created .gitignore
- Added pytest-cov to requirements.txt
- Updated README with CI badge
- Committed with descriptive message
- Opened PR #7 with complete template

---

## Role 4: Reviewer/QA

### Initial Prompt (Implicit)
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

### User Input (PR #5)
> "yes" (to reviewing PR #5)

### Execution - PR #5
- Checked out feature branch
- Ran all tests locally (20/20 passing)
- Verified all 7 success criteria
- Code quality assessment (strengths noted)
- Posted review approval
- Merged PR #5

### User Input (PR #6)
> "yes" (to reviewing PR #6)

### Execution - PR #6
- Checked out feature branch
- Ran all tests locally (20/20 passing)
- Verified all 8 success criteria
- UI/UX quality assessment
- Posted review approval
- Merged PR #6

### User Input (PR #7)
> "yes" (to reviewing PR #7)

### Execution - PR #7
- Checked CI status (✓ passing in 16 seconds!)
- Verified all 6 success criteria
- **Verified CI ran successfully** (milestone!)
- Workflow configuration review
- Posted review approval
- Merged PR #7

---

## Role 5: Release/DevOps

### Initial Prompt (Implicit)
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
## v0.1.0 - YYYY-MM-DD

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

### User Input
> "Would you like me to switch to the Release/DevOps role and ship v0.1.0 -> yes"

### Execution
- Pulled latest master (all PRs merged)
- Reviewed merged PRs (#5, #6, #7)
- Created annotated git tag v0.1.0
- Pushed tag to origin
- Created GitHub Release with comprehensive notes:
  - Features summary
  - Quality metrics
  - Getting started guide
  - API documentation
  - Workflow demonstration summary
- Added release summary comment to Epic #1
- Closed Epic #1 with reason: completed
- Verified all artifacts created

---

## Key Phrases Used

### Workflow Transitions
- "Switch to [Role]" - Role change request
- "yes" - Proceed with next step
- "Continue as [Role]" - Keep current role

### Quality Gates
- "Verify all success criteria"
- "Check tests passing"
- "Review code quality"
- "Validate DoR/DoD"

### Evidence-Based Reviews
- "Map each criterion to evidence"
- "Provide file paths and line numbers"
- "Include test output"
- "Show coverage report"

### Release Checklist
- "Verify CI green"
- "All PRs merged"
- "Create annotated tag"
- "Generate release notes"
- "Close Epic"

---

## Template Compliance

All artifacts used project templates:
- `.github/ISSUE_TEMPLATE/epic.md` - Epic #1
- `.github/ISSUE_TEMPLATE/story-task.md` - Stories #2, #3, #4
- `.github/PULL_REQUEST_TEMPLATE.md` - PRs #5, #6, #7

Every template section was filled with specific, actionable content.

**End of Role Prompts Documentation**
