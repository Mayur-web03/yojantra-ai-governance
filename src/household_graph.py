import networkx as nx

def build_household_graph(citizens, properties, schemes):

    G = nx.Graph()

    # Add citizen nodes
    for _, row in citizens.iterrows():
        G.add_node(
            row["citizen_id"],
            type="citizen",
            name=row["name"],
            household=row["household_id"]
        )

    # Connect family members
    households = citizens["household_id"].unique()

    for household in households:

        members = citizens[citizens["household_id"] == household]["citizen_id"].tolist()

        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                G.add_edge(members[i], members[j], relation="family")

    # Add property nodes
    for _, row in properties.iterrows():

        prop_id = row["property_id"]

        G.add_node(prop_id, type="property", value=row["value"])

        G.add_edge(row["owner_id"], prop_id, relation="owns")

    # Add scheme nodes
    for _, row in schemes.iterrows():

        scheme = row["scheme_name"]

        G.add_node(scheme, type="scheme")

        G.add_edge(row["citizen_id"], scheme, relation="beneficiary")

    return G