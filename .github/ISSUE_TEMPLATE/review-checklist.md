---
name: Review Checklist
about: Template for PR reviews
title: 'Review: PR #'
labels: review
assignees: ''
---

# Review: PR #<pr-number>

## PR & Issue Links
- PR: #<pr-number>
- Issue: #<issue-id>
- Epic: #<epic-id>

## Review Checklist
- [ ] PR links exactly one Issue and references Epic
- [ ] PR template complete (no placeholders)
- [ ] Each success criterion has evidence
- [ ] Tests exist and cover happy path + 1 edge case (if relevant)
- [ ] Tests are passing (CI green)
- [ ] Docs updated (or explicitly "not needed" with reason)
- [ ] No unrelated refactors
- [ ] Naming / structure consistent with project conventions
- [ ] Code follows project style guide
- [ ] No TODOs without issue references

## Success Criteria Validation
_For each criterion from the original issue, verify evidence:_

| Criterion | Met? | Evidence Location | Notes |
|-----------|------|-------------------|-------|
| ...       | ✅/❌ | ...               | ...   |

## Test Results
- [ ] Unit tests pass locally
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed (if applicable)

## Findings
### Blocking Issues (must fix)
- ...

### Non-blocking Suggestions
- ...

## Decision
- [ ] ✅ **APPROVE** - Ready to merge
- [ ] 🔄 **REQUEST CHANGES** - See blocking issues above
- [ ] 💬 **COMMENT** - Non-blocking feedback only

## Next Steps
<what should happen next>
