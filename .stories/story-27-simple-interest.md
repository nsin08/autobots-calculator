# Story: Simple Interest Calculator

**Parent Epic:** #18  
**Sprint:** Sprint 2 (v0.3.0-final)  
**Depends on:** #23  
**Estimate:** 8 hours

## Success Criteria
- [ ] POST /api/calculate/simple-interest endpoint
- [ ] Formula: I = P × R × T
- [ ] Frontend: form with principal, rate, time_years inputs
- [ ] Display: interest, final_amount

## API Contract
POST /api/calculate/simple-interest: {principal, rate, time_years} → 200 {interest, final_amount}

## Tests
Formula accuracy, edge cases (zero rate, boundary values). Coverage >90%.

## Deliverables
Update src/service/calculators/financial.py, update frontend with Simple tab, tests

## Branch
feature/27-simple-interest
