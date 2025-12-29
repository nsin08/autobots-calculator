# Service Readiness Baseline

A minimal service demonstrating health & observability endpoints with full project lifecycle.

## Project

**Use case:** "Health & Observability pack for a tiny service" (ship v0.1.0)

This project demonstrates a complete GitHub workflow from idea → Epic → Stories → implementation → review → release.

## Structure

```
autobots/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── epic.md
│   │   ├── story-task.md
│   │   └── review-checklist.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   └── ROLE_PROMPTS.md
├── src/
│   └── service/
│       ├── __init__.py
│       ├── app.py
│       ├── health.py
│       └── metrics.py
├── tests/
│   ├── test_health.py
│   └── test_metrics.py
├── RULEBANK.md
├── README.md
└── requirements.txt
```

## Quick Start

### Prerequisites
- Python 3.8+
- GitHub CLI (`gh`) or GitKraken MCP tools
- Access to GitHub repository

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd autobots

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m src.service.app

# Run tests
pytest tests/
```

## Endpoints

### GET /health
Returns service health status.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-12-29T10:00:00Z"
}
```

### GET /metrics
Returns basic service metrics.

**Response:**
```json
{
  "requests_total": 42,
  "uptime_seconds": 3600
}
```

## Development Workflow

This project follows a 5-role lifecycle. See [RULEBANK.md](RULEBANK.md) for complete rules.

### Roles
1. **Sponsor/PO** - Creates Idea Issues
2. **Tech Lead/Architect** - Converts to Epic + Stories
3. **Implementer** - Builds features
4. **Reviewer/QA** - Validates PRs
5. **Release/DevOps** - Ships releases

### State Machine
```
Intake → Spec Ready → In Progress → In Review → Done → Released
```

### Templates
- **Epic**: [.github/ISSUE_TEMPLATE/epic.md](.github/ISSUE_TEMPLATE/epic.md)
- **Story/Task**: [.github/ISSUE_TEMPLATE/story-task.md](.github/ISSUE_TEMPLATE/story-task.md)
- **PR**: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
- **Review**: [.github/ISSUE_TEMPLATE/review-checklist.md](.github/ISSUE_TEMPLATE/review-checklist.md)

## Testing the Workflow

See [docs/WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) for step-by-step instructions on executing the complete lifecycle.

## Example Epic

**Epic: Service readiness baseline (v0.1.0)**

Stories:
- Story A: GET /health + tests + docs
- Story B: GET /metrics + tests + docs  
- Story C: CI + PR template enforcement + release notes

## License

MIT
