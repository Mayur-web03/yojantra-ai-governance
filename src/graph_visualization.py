from pyvis.network import Network

def visualize_graph(G):

    net = Network(height="600px", width="100%")

    for node, data in G.nodes(data=True):

        node_type = data.get("type")

        if node_type == "citizen":
            color = "blue"
        elif node_type == "property":
            color = "green"
        elif node_type == "scheme":
            color = "red"
        else:
            color = "gray"

        net.add_node(node, label=node, color=color)

    for source, target, data in G.edges(data=True):

        relation = data.get("relation")

        net.add_edge(source, target, title=relation)

    net.write_html("household_network.html")

    print("Graph created: household_network.html")