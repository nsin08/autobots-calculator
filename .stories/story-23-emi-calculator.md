# Story: EMI Calculator (backend + frontend)

**Parent Epic:** #18  
**Sprint:** Sprint 1  
**Depends on:** #19  
**Estimate:** 22 hours

## Success Criteria
- [ ] POST /api/calculate/emi endpoint with validation
- [ ] Formula: EMI = [P × r × (1+r)^n] / [(1+r)^n-1], r=rate/1200, n=years*12
- [ ] Use Decimal for precision, round to 2 decimals
- [ ] Frontend: form with loan_amount, annual_rate, tenure_years inputs
- [ ] Display: monthly EMI, total interest, total payment
- [ ] Input validation: loan $1k-$10M, rate 0.1%-30%, tenure 1-30y
- [ ] Test with PO example: $100k @ 8.5% for 20y → EMI = $867.82

## API Contract
POST /api/calculate/emi: {loan_amount, annual_rate, tenure_years} → 200 {emi, total_interest, total_payment}

## Tests
Happy path, zero rate, boundary values, PO's exact test case, edge cases. Coverage >95%.

## Deliverables
src/service/calculators/financial.py, update static/index.html with financial tab, update app.js, tests/test_financial.py

## Branch
feature/23-emi-calculator
