import pandas as pd


def calculate_risk(features, graph_results, patterns):

    risk_list = []

    for _, row in features.iterrows():

        score = 0
        reasons = []

        # Asset rule
        if row["total_property_value"] > 3000000:
            score += 30
            reasons.append("High property ownership")

        # Scheme stacking
        if row["scheme_count"] >= 3:
            score += 25
            reasons.append("Multiple schemes")

        # Multiple ration cards
        if row["ration_card_count"] > 1:
            score += 25
            reasons.append("Duplicate ration cards")

        # ML anomaly
        if row["anomaly"] == "Suspicious":
            score += 20
            reasons.append("AI anomaly detected")

        risk_list.append({
            "household_id": row["household_id"],
            "risk_score": score,
            "reasons": ", ".join(reasons)
        })

    risk_df = pd.DataFrame(risk_list)

    return risk_df