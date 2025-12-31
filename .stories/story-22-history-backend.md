# Story: History Backend (API + storage)

**Parent Epic:** #18  
**Sprint:** Sprint 1  
**Depends on:** #19  
**Estimate:** 10 hours

## Success Criteria
- [ ] CalculationHistory model created
- [ ] GET /api/history?limit=50 returns last 50 user calculations
- [ ] POST /api/history saves calculation
- [ ] DELETE /api/history clears user history
- [ ] User isolation (only see own history)

## Database Model
calculation_history: id, user_id, calculator_type, expression, result, created_at

## API Contracts
GET /api/history?limit=50 → 200 {calculations: [{id, type, expression, result, timestamp}]}  
POST /api/history: {type, expression, result} → 201 {success, id}  
DELETE /api/history → 200 {success, message}

## Tests
CRUD operations, user isolation, pagination limit. Coverage >90%.

## Deliverables
Update models.py with CalculationHistory, src/service/history.py, update app.py, tests/test_history.py

## Branch
feature/22-history-backend
