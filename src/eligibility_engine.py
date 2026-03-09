def check_eligibility(family_size, income, property_value):

    reasons = []
    score = 0

    # income rule
    if income > 800000:
        score += 30
        reasons.append("Income exceeds welfare threshold")

    # asset rule
    if property_value > 3000000:
        score += 30
        reasons.append("High property ownership")

    # large household advantage
    if family_size >= 5:
        score -= 10

    if score >= 40:
        decision = "Not Eligible"
    else:
        decision = "Eligible"

    return {
        "decision": decision,
        "risk_score": score,
        "reasons": reasons
    }