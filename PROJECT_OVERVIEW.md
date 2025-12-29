# Project Lifecycle Demonstration

Complete 5-role GitHub workflow for testing idea-to-release capability with agents.

## What This Demonstrates

This project proves capability to **interact with the complete project lifecycle**:
- Intake → Spec → Implementation → Review → Release
- Multiple roles with handoffs (PO, Tech Lead, Implementer, Reviewer, DevOps)
- Template-driven consistency
- Gate enforcement (DoR/DoD)
- Auditable artifact trail
- Small, reviewable increments

## Core Components

### 1. [RULEBANK.md](RULEBANK.md)
Non-negotiable rules for the team:
- State machine (Intake → Released)
- Definition of Ready/Done
- PR hygiene gates
- Artifact linking requirements

### 2. Templates
- **Epic**: [.github/ISSUE_TEMPLATE/epic.md](.github/ISSUE_TEMPLATE/epic.md)
- **Story/Task**: [.github/ISSUE_TEMPLATE/story-task.md](.github/ISSUE_TEMPLATE/story-task.md)
- **PR**: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
- **Review**: [.github/ISSUE_TEMPLATE/review-checklist.md](.github/ISSUE_TEMPLATE/review-checklist.md)

### 3. Role Prompts
Each role has specific instructions: [docs/ROLE_PROMPTS.md](docs/ROLE_PROMPTS.md)
1. Sponsor/PO (Intake)
2. Tech Lead/Architect (Spec Ready)
3. Implementer (In Progress → PR)
4. Reviewer/QA (In Review)
5. Release/DevOps (Release)

### 4. Working Service
Minimal Flask service with:
- `GET /health` → health check endpoint
- `GET /metrics` → basic metrics (request count, uptime)
- Full test coverage
- Documentation

## Quick Start

### Fast Track (30 min)
See [docs/QUICKSTART.md](docs/QUICKSTART.md) for rapid walkthrough.

### Full Guide
See [docs/WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) for detailed step-by-step.

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
pytest tests/
python -m src.service.app
```

## Example Flow

```
1. PO creates Epic #1 "Service readiness baseline v0.1.0"
   ↓
2. Tech Lead creates Stories #2 (health), #3 (metrics), #4 (CI)
   ↓
3. Implementer builds #2 → opens PR #10 with evidence
   ↓
4. Reviewer validates PR #10 against Story #2 criteria → approves
   ↓
5. Release merges → tags v0.1.0 → generates notes → closes Epic
```

**Result**: Full traceability from idea to shipped release.

## Key Success Criteria

✅ Multiple artifacts created (Epic → Stories → PRs → Release)  
✅ Templates enforced at each step  
✅ Gates respected (no jumping states)  
✅ Small, focused PRs  
✅ Test coverage  
✅ Working endpoints  
✅ Release notes linked to issues  

## File Structure

```
autobots/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── epic.md
│   │   ├── story-task.md
│   │   └── review-checklist.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── ROLE_PROMPTS.md       # Prompts for each role
│   ├── WORKFLOW_GUIDE.md     # Detailed step-by-step
│   └── QUICKSTART.md         # 30-minute walkthrough
├── src/
│   └── service/
│       ├── app.py            # Flask service with /health, /metrics
│       └── __init__.py
├── tests/
│   ├── test_health.py        # Health endpoint tests
│   └── test_metrics.py       # Metrics endpoint tests
├── RULEBANK.md               # Team rules & state machine
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## Tools Used

- **GitHub CLI** (`gh`) or **GitKraken MCP** for git operations
- **GitHub Copilot** with agent capabilities for role execution
- **GitHub Projects** for workflow visualization
- **GitHub Issues** for work tracking
- **GitHub PRs** for review process
- **GitHub Releases** for versioning

## Testing Strategy

### Manual Test
Follow [QUICKSTART.md](docs/QUICKSTART.md) to execute full workflow manually.

### Agent Test
Use role prompts from [ROLE_PROMPTS.md](docs/ROLE_PROMPTS.md) with Copilot agents.

### Automation Test
Add GitHub Actions to enforce:
- Template completeness checks
- Auto-move project cards
- Auto-generate release notes
- Gate validation before state transitions

## Next Steps

After completing basic workflow:

1. **Add complexity**: Feature requiring multiple branches → integration branch
2. **Test failure paths**: Intentionally violate DoR/DoD and verify blocks
3. **Parallel work**: Multiple implementers working on different stories
4. **Metrics**: Track cycle time (Intake → Released)
5. **Automation**: GitHub Actions for template validation
6. **Agent orchestration**: Each role as autonomous agent with MCP

## Success Metrics

Track these to measure workflow effectiveness:

- **Cycle time**: Hours from Intake to Released
- **Gate compliance**: % of items satisfying DoR/DoD
- **Template usage**: % of PRs using template correctly
- **PR size**: Average lines changed per PR (goal: <300)
- **Review turnaround**: Hours from PR open to merge
- **Traceability**: % of releases linking back to Epic

## Philosophy

This isn't about "automating coding" — it's about **demonstrating lifecycle interaction capability**:

- Create and route artifacts (Issues, PRs, Releases)
- Enforce gates (required fields, CI green, checklist completion)
- Drive transitions (project columns, labels, status)
- Maintain audit trail (links, evidence, decisions)

**Code is cheap. Clarity is rare. Judgment is priceless.**

The workflow proves an agent can **operate the process**, not just generate code.

## License

MIT
