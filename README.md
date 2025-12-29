# Autobots Calculator

[![Tests](https://github.com/nsin08/autobots-calculator/actions/workflows/test.yml/badge.svg)](https://github.com/nsin08/autobots-calculator/actions/workflows/test.yml)

A web-based calculator demonstrating a complete 5-role GitHub lifecycle workflow.

## Project

**Live Demo:** http://localhost:5000 (when running locally)

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

### Using the Calculator

Once the service is running, open your browser and navigate to:
```
http://localhost:5000
```

**Calculator Features:**
- Click number buttons (0-9) to enter numbers
- Click operation buttons (+, -, ×, ÷) to select operation
- Click = to calculate result
- Click C to clear
- Click ← to delete last character
- Keyboard support: numbers, operators, Enter/=, Escape/C, Backspace

**Example:**
1. Click `5`
2. Click `+`
3. Click `3`
4. Click `=`
5. Result: `8`

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

### POST /api/calculate
Performs arithmetic and advanced mathematical operations.

**Request:**
```json
{
  "operation": "add|subtract|multiply|divide|factorial|power|modulo",
  "a": 10,
  "b": 5  // Optional for factorial
}
```

**Response (Success - 200):**
```json
{
  "result": 15
}
```

**Response (Error - 400):**
```json
{
  "error": "Division by zero"
}
```

#### Basic Operations
**Examples:**
```bash
# Addition
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 2, "b": 3}'
# Returns: {"result": 5}

# Subtraction
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "subtract", "a": 10, "b": 4}'
# Returns: {"result": 6}

# Multiplication
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 3, "b": 4}'
# Returns: {"result": 12}

# Division
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 10, "b": 2}'
# Returns: {"result": 5}

# Error case: Division by zero
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 10, "b": 0}'
# Returns: {"error": "Division by zero"}
```

#### Advanced Operations (v0.2.0+)

**Factorial** - Computes n! (0 ≤ n ≤ 20, integer only)
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "factorial", "a": 5}'
# Returns: {"result": 120}

# Error case: Negative number
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "factorial", "a": -5}'
# Returns: {"error": "Factorial not defined for negative numbers"}

# Error case: Non-integer
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "factorial", "a": 5.5}'
# Returns: {"error": "Factorial requires integer input"}
```

**Power** - Computes a^b (exponent bounds: -100 ≤ b ≤ 100)
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": 3}'
# Returns: {"result": 8}

# Negative exponent
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": -2}'
# Returns: {"result": 0.25}

# Error case: Exponent out of bounds
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": 101}'
# Returns: {"error": "Exponent out of bounds (-100 to 100)"}
```

**Modulo** - Computes a % b (remainder after division)
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "modulo", "a": 10, "b": 3}'
# Returns: {"result": 1}

# Error case: Zero divisor
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "modulo", "a": 10, "b": 0}'
# Returns: {"error": "Division by zero"}
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
