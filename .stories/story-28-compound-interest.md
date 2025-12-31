# Story: Compound Interest Calculator

**Parent Epic:** #18  
**Sprint:** Sprint 2  
**Depends on:** #27  
**Estimate:** 10 hours

## Success Criteria
- [ ] POST /api/calculate/compound-interest endpoint
- [ ] Formula: A = P(1 + r/n)^(nt)
- [ ] Frequencies: Monthly, Quarterly, Annual
- [ ] Frontend: form with principal, rate, time_years, frequency dropdown
- [ ] Test with PO example: $50k @ 6% for 5y, monthly → Final = $67,409.09

## API Contract
POST /api/calculate/compound-interest: {principal, rate, time_years, frequency} → 200 {interest, final_amount}

## Tests
All 3 frequencies, PO's exact test case, edge cases. Coverage >90%.

## Deliverables
Update src/service/calculators/financial.py, update frontend with Compound tab, tests

## Branch
feature/28-compound-interest
