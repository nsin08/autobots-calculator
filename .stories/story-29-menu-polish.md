# Story: Menu Navigation Polish + User Preferences

**Parent Epic:** #18  
**Sprint:** Sprint 2  
**Depends on:** #25, #27, #28  
**Estimate:** 12 hours

## Success Criteria
- [ ] UserPreference model with last_calculator_type field
- [ ] Remember last used calculator per user (persist to DB)
- [ ] On login, restore last calculator type
- [ ] Sub-tabs within Financial (EMI | Simple | Compound)
- [ ] Professional styling polish (colors, spacing, transitions)

## Database Model
user_preferences: user_id, last_calculator_type

## Tests
Preference save/load, sub-tab switching, persistence across sessions

## Deliverables
Update models.py with UserPreference, update history.py with preference logic, frontend polish, tests

## Branch
feature/29-menu-polish-preferences
