# Quick Start: Testing the Workflow

Fast-track guide to test the 5-role lifecycle workflow in under 30 minutes.

## Setup (5 minutes)

```bash
# 1. Initialize repo (if not already done)
cd d:\wsl_shared\src\autobots
git init
gh repo create autobots-workflow --public --source=. --remote=origin

# 2. Create project board
gh project create --owner @me --title "Autobots Lifecycle Demo"

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify tests run
pytest tests/
```

## Workflow Test (25 minutes)

### Step 1: PO Creates Idea (3 min)

```bash
# Create Epic issue
gh issue create \
  --title "EPIC: Service readiness baseline v0.1.0" \
  --label "epic" \
  --body-file .github/ISSUE_TEMPLATE/epic.md
# Returns: Issue #1
```

**Prompt to Copilot:**
```
[Role: Sponsor/PO]
Fill in Epic #1 with:
- Problem: Need health & metrics endpoints for monitoring
- Success: /health and /metrics working with tests + docs
- Stories: health, metrics, CI/release
- Target: v0.1.0
```

### Step 2: Tech Lead Specs (5 min)

**Prompt to Copilot:**
```
[Role: Tech Lead/Architect]
Create 3 story issues from Epic #1:
- Story: Health endpoint (GET /health returns 200 + status:ok + tests)
- Story: Metrics endpoint (GET /metrics returns counters + tests)  
- Story: CI & release automation

Add architecture notes: Flask, pytest, GitHub Actions
```

```bash
# Create stories
gh issue create --title "Health endpoint" --label "story" --body "Parent: #1 ..."
gh issue create --title "Metrics endpoint" --label "story" --body "Parent: #1 ..."
gh issue create --title "CI & release" --label "story" --body "Parent: #1 ..."
# Returns: Issues #2, #3, #4
```

### Step 3: Implementer Builds (10 min)

**For Health endpoint:**

```bash
# Create branch
git checkout -b feature/2-health-endpoint

# Implement (already done in src/service/app.py)
# Tests (already done in tests/test_health.py)
# Commit
git add src/service/app.py tests/test_health.py README.md
git commit -m "Add health endpoint with tests"
git push -u origin feature/2-health-endpoint

# Create PR
gh pr create \
  --title "Add health endpoint" \
  --body "Closes #2, Epic #1" \
  --base main
# Returns: PR #10
```

**Prompt to Copilot:**
```
[Role: Implementer]
Fill PR #10 template:
- Map success criteria to test_health.py evidence
- Add test output
- Document risk/rollback
```

**Repeat for Metrics (PR #11)**

### Step 4: Reviewer Validates (5 min)

**Prompt to Copilot:**
```
[Role: Reviewer/QA]
Review PR #10:
- Check template complete
- Verify tests in test_health.py cover criteria
- Run: pytest tests/test_health.py
- Validate no unrelated changes

Decision: Approve or request changes
```

```bash
# If approved
gh pr review 10 --approve --body "✅ All criteria met, tests pass"
gh pr merge 10 --squash

# Repeat for PR #11
```

### Step 5: Release Ships (2 min)

```bash
# After both PRs merged
git checkout main
git pull

# Create release
gh release create v0.1.0 \
  --title "v0.1.0 - Service Readiness Baseline" \
  --notes "Features:
- Health endpoint (#10, closes #2)
- Metrics endpoint (#11, closes #3)

Closes Epic #1"

# Tag and push
git tag v0.1.0
git push origin v0.1.0
```

---

## Verification Checklist

```bash
# Verify artifacts
gh issue list --label epic     # Should show Epic #1 closed
gh issue list --label story    # Should show stories #2, #3, #4 closed
gh pr list --state merged      # Should show PRs #10, #11 merged
gh release list                # Should show v0.1.0

# Verify functionality
python -m src.service.app &    # Start service
curl http://localhost:5000/health   # Should return {"status": "ok", ...}
curl http://localhost:5000/metrics  # Should return {"requests_total": ..., ...}

# Verify tests
pytest tests/ -v               # All tests should pass
```

---

## What You've Demonstrated

✅ **5-role lifecycle**: PO → Tech Lead → Implementer → Reviewer → Release  
✅ **Template enforcement**: Epic, Story, PR templates used  
✅ **Gate compliance**: DoR/DoD respected  
✅ **Artifact traceability**: Issue → PR → Release linked  
✅ **Working code**: Endpoints functional with tests  
✅ **Release hygiene**: Tagged, documented, shipped

**Time to complete**: ~30 minutes  
**Artifacts created**: 1 Epic, 3 Stories, 2 PRs, 1 Release, 1 Tag

---

## Automation Opportunities

After manual walkthrough, automate with:

1. **GitHub Actions**: Auto-check template completeness
2. **Project board automation**: Auto-move cards on PR events
3. **Bot reviewers**: Auto-validate DoD checklist
4. **Release notes**: Auto-generate from PR labels
5. **Agent orchestration**: Each role as an agent with MCP tools

**Next**: See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) for detailed phase breakdowns.
