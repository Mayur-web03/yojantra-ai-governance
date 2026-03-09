def detect_patterns(citizens, properties, schemes, ration_cards):

    patterns = []

    # Duplicate ration cards
    ration_counts = ration_cards.groupby("household_id").size()

    for household, count in ration_counts.items():

        if count > 1:

            patterns.append({
                "household_id": household,
                "pattern": "Duplicate Ration Cards"
            })

    return patterns