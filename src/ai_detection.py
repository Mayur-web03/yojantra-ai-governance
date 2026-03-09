from sklearn.ensemble import IsolationForest


def detect_anomalies(features):

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    X = features[
        [
            "family_size",
            "total_property_value",
            "scheme_count",
            "ration_card_count"
        ]
    ]

    features["anomaly"] = model.fit_predict(X)

    features["anomaly"] = features["anomaly"].map({
        1: "Normal",
        -1: "Suspicious"
    })

    return features