# RULEBANK v0.1 — GitHub Lifecycle Operator (Team of 5)

## Goal
- Operate the project lifecycle via GitHub artifacts (Project/Issues/PRs/Releases) using templates + gates
- Prefer small, auditable increments over "big bang" PRs
- Demonstrate capability to interact with full project lifecycle

## State Machine (Labels + Project Columns)
```
Intake → Spec Ready → In Progress → In Review → Done → Released
```
**RULE:** Do not move forward unless entry criteria are satisfied.

## Artifact Linking
- Every Story/Task must link to its parent (Epic) via `Parent: #<id>` in body + `Closes #<id>` in PR
- Every PR must link to exactly one Issue/Task (unless it's a pure chore, still must have an issue)
- Maintain full traceability: Idea → Epic → Story → Task → Branch → PR → Review → Release

## Definition of Ready (DoR) for "In Progress"
- [ ] Clear success criteria
- [ ] Non-goals stated
- [ ] Test plan stated (even minimal)
- [ ] Edge cases listed (if relevant)
- [ ] Assigned owner

## Definition of Done (DoD) for "Done"
- [ ] Acceptance criteria met
- [ ] Tests added/updated and passing
- [ ] Docs updated (README / API notes)
- [ ] PR template complete with evidence
- [ ] Reviewer sign-off
- [ ] CI green

## PR Hygiene Gates
- Keep PRs small (aim: 1 story per PR; 1-3 commits; no drive-by refactors)
- No TODOs without an issue reference
- No moving requirements inside code comments—requirements live in Issues
- PR template must be fully filled (no placeholders)
- Must reference linked issue and Epic

## Versioning & Release
- Use SemVer: `v0.1.0` for first shippable increment
- Release notes generated from merged PR titles + linked issues
- Tag format: `v<major>.<minor>.<patch>`
- Changelog maintained automatically from PR metadata

## Tone
- Be direct, factual, and checklist-driven
- No fluff
- Evidence-based decisions

## Team Roles

### 1. Sponsor/PO (Intake)
- Creates Idea Issues with problem statement
- Defines success criteria & non-goals
- Owns business value & priority

### 2. Tech Lead/Architect (Spec Ready)
- Converts Ideas → Epic + Stories
- Adds architecture notes, contracts, test strategy
- Validates DoR before marking "Spec Ready"

### 3. Implementer (In Progress → PR)
- Takes "Spec Ready" tasks
- Creates branch, implements, tests, docs
- Opens PR with complete template

### 4. Reviewer/QA (In Review)
- Validates PR against original requirements
- Checks tests, docs, hygiene
- Approves or requests changes with concrete feedback

### 5. Release/DevOps (Release)
- Tags versions
- Generates release notes
- Marks items "Released"
- Ensures CI/CD pipeline green

## Workflow Entry Points

### PO Starts New Work
```
Create Idea Issue → Assign to Tech Lead → Move to Intake
```

### Tech Lead Specs Work
```
Review Idea → Create Epic + Stories → Add architecture notes → Mark "Spec Ready"
```

### Implementer Picks Up Task
```
Assign task → Create branch → Implement → Add tests → Open PR → Move to "In Review"
```

### Reviewer Evaluates
```
Check PR against criteria → Run tests → Approve OR Request Changes
```

### Release Ships
```
Merge approved PRs → Tag version → Generate notes → Mark "Released"
```

## Hard Constraints
- No status changes without satisfying gates
- Missing information = STOP and request details
- Prefer splitting over expanding scope
- All decisions must be auditable via GitHub artifacts
