import pandas as pd


def calculate_household_risk(citizens, properties, schemes, ration_cards):

    risk_results = []

    households = citizens["household_id"].unique()

    for household in households:

        household_members = citizens[citizens["household_id"] == household]

        risk_score = 0
        reasons = []

        member_ids = household_members["citizen_id"].tolist()

        # Property ownership check
        household_properties = properties[
            properties["owner_id"].isin(member_ids)
        ]

        total_property_value = household_properties["value"].sum()

        if total_property_value > 3000000:
            risk_score += 30
            reasons.append("High property ownership")

        # Scheme stacking check
        household_schemes = schemes[
            schemes["citizen_id"].isin(member_ids)
        ]

        if household_schemes["scheme_name"].nunique() >= 3:
            risk_score += 25
            reasons.append("Multiple schemes used")

        # Duplicate ration cards
        household_rations = ration_cards[
            ration_cards["household_id"] == household
        ]

        if len(household_rations) > 1:
            risk_score += 25
            reasons.append("Multiple ration cards")

        # Property owned by young person
        for _, prop in household_properties.iterrows():

            owner = citizens[citizens["citizen_id"] == prop["owner_id"]].iloc[0]

            if owner["age"] < 25 and prop["value"] > 2000000:
                risk_score += 20
                reasons.append("Property owned by young member")

        risk_results.append({
            "household_id": household,
            "risk_score": risk_score,
            "reasons": ", ".join(reasons)
        })

    risk_df = pd.DataFrame(risk_results)

    # Assign risk level
    def risk_level(score):

        if score >= 70:
            return "High Risk"
        elif score >= 40:
            return "Medium Risk"
        else:
            return "Low Risk"

    risk_df["risk_level"] = risk_df["risk_score"].apply(risk_level)

    return risk_df