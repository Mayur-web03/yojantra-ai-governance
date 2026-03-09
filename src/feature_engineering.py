import pandas as pd

def build_features(citizens, properties, schemes, ration_cards):

    features = []

    households = citizens["household_id"].unique()

    for h in households:

        members = citizens[citizens["household_id"] == h]

        member_ids = members["citizen_id"].tolist()

        household_properties = properties[
            properties["owner_id"].isin(member_ids)
        ]

        household_schemes = schemes[
            schemes["citizen_id"].isin(member_ids)
        ]

        ration = ration_cards[
            ration_cards["household_id"] == h
        ]

        features.append({

            "household_id": h,

            "family_size": len(members),

            "total_property_value": household_properties["value"].sum(),

            "scheme_count": household_schemes["scheme_name"].nunique(),

            "ration_card_count": len(ration)

        })

    return pd.DataFrame(features)