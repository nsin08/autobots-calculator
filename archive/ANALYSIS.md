# GitHub Search Analysis: Similar Projects to Autobots

**Date:** December 30, 2025  
**Search Strategy:** Used `gh search repos` queries targeting workflow automation, AI agents, and SDLC.

Important: `gh search repos` searches repo metadata (name/description/topics). It does **not** search file contents. Claims about templates/instructions living inside repos require `gh search code`.

## Search Results Summary (Validated)

Re-ran all repo searches with `--limit 30` and confirmed:

- Query 1 `"AI agent workflow"`: 30 results; stars range 3..24,674
- Query 2 `"epic story task workflow"`: 0 results
- Query 3 `"copilot instructions workflow"`: 0 results
- Query 4 `"github issue template workflow automation"`: 0 results
- Query 5 `"project management github actions"`: 0 results
- Query 6 `"sdlc software development lifecycle"`: 3 results; stars range 0..6

Interpretation note: "0 results" here means "0 repos matched that exact phrase in metadata", not "the concept doesn't exist on GitHub".

---

## Close Candidates (Most Relevant)

### Top 5 Most Similar Projects (Manual Selection)

These are "closest by concept", not "top by stars".

1. **simstudioai/sim** (24,674 stars)  
   - URL: https://github.com/simstudioai/sim  
   - Similarity: AI agent workflow platform (general-purpose)  
   - Difference: not GitHub-native SDLC; more of a workflow product

2. **mantrakp04/manusmcp** (92 stars)  
   - URL: https://github.com/mantrakp04/manusmcp  
   - Similarity: multi-role agent system  
   - Difference: not SDLC/lifecycle focused

3. **k3nnethfrancis/client-researcher** (82 stars)  
   - URL: https://github.com/k3nnethfrancis/client-researcher  
   - Similarity: multi-agent workflow with role separation  
   - Difference: domain-specific (research), not SDLC

4. **jackvandervall/agentic-archive** (79 stars)  
   - URL: https://github.com/jackvandervall/agentic-archive  
   - Similarity: agent workflow examples  
   - Difference: archive/examples rather than a lifecycle framework

5. **aaronsteers/auto-sdlc** (0 stars)  
   - URL: https://github.com/aaronsteers/auto-sdlc  
   - Similarity: explicitly "AI + SDLC automation"  
   - Difference: low activity; unclear gates/traceability model from metadata

### Notable Adjacent Projects (Missed By Initial Keywords)

These contradict the stronger "no projects bridging GitHub issues and AI agents" claim:

- **OpenHands/OpenHands** (66,014 stars): https://github.com/OpenHands/OpenHands  
- **All-Hands-AI/openhands-resolver** (117 stars): https://github.com/All-Hands-AI/openhands-resolver  
- **sweepai/sweep** (7,621 stars): https://github.com/sweepai/sweep

They typically optimize for "issue -> agent -> PR/changes", rather than "multi-role SDLC with explicit gates + template-enforced artifacts".

Also adjacent (not AI, but "GitHub issues/comments -> automation"):

- **github/command** (157 stars): https://github.com/github/command  
- **github/branch-deploy** (513 stars): https://github.com/github/branch-deploy

---

## Key Findings (What's Supported vs. Overstated)

### What Exists (From the `"AI agent workflow"` Query)

- Visual/no-code agent workflow builders and platforms (e.g., `simstudioai/sim`)
- Multi-agent role systems (e.g., `mantrakp04/manusmcp`)
- Low-code automation + AI integrations (e.g., n8n "AI agents" repos)
- Generic planning/workflow engines (e.g., `orra-dev/orra`, `future-agi/agent-opt`)

### What This Metadata Search Did Not Prove

- "Copilot-ready workflow templates don't exist": not provable via repo search; needs `gh search code` for `copilot-instructions.md`, `.github/ISSUE_TEMPLATE/*`, etc.
- "No issue-template-driven automation exists": there are many "IssueOps" repos, but they don't necessarily target SDLC/quality gates.
- "No GitHub issues + AI agents projects exist": false (see OpenHands/Sweep examples above).

### More Defensible "Gap" Statement

What the repo-metadata searches did not directly surface is an open-source project positioning itself as:

- GitHub-native lifecycle framework (Issues/PRs/Projects as the workflow engine)
- Explicit role separation (PO/Tech Lead/Implementer/QA/Release)
- Explicit DoR/DoD-style gates for state transitions
- Templates + role prompts + "copilot instructions" used as the primary operating system
- End-to-end traceability (Epic -> Story -> PR -> Release)

---

## Autobots Value Proposition (Validated Against This Repo)

These claims match what exists in this repository:

- Role prompts: `docs/ROLE_PROMPTS.md`
- Workflow execution guide: `docs/WORKFLOW_GUIDE.md`
- Copilot agent guidance: `.github/copilot-instructions.md`
- GitHub templates present under `.github/ISSUE_TEMPLATE/`
- Demo app: `src/service/app.py` (Flask health/metrics + calculator API/UI)

---

## Recommendations

1. Tighten negative claims: prefer "not surfaced by these queries" over "doesn't exist".
2. Add a "Related Work" section acknowledging adjacent repos (OpenHands, Sweep, IssueOps) and clearly state how Autobots differs.
3. If you want a stronger competitor scan, add `gh search code` passes for:
   - `copilot-instructions.md`
   - `.github/ISSUE_TEMPLATE`
   - `definition of done` / `definition of ready`
   - "quality gate", "lifecycle", "workflow state machine"
