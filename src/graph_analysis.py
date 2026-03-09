import networkx as nx


def analyze_graph(G):

    results = []

    # centrality
    centrality = nx.degree_centrality(G)

    for node, score in centrality.items():

        if score > 0.2:

            results.append({
                "entity": node,
                "centrality_score": round(score, 3),
                "flag": "Highly Connected Entity"
            })

    return results