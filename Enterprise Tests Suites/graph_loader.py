import networkx as nx

# Define the graph (top-down structure)
api_graph = {
    "ProductSuites": ["UserProfile", "TransactionSummary"],
    "UserProfile": ["UserAccountLookup"],
    "TransactionSummary": [],
    "UserAccountLookup": []
}

def get_execution_order(api_graph: dict, root_api: str) -> list:
    G = nx.DiGraph()

    # Correct edge direction: parent → child
    for parent, children in api_graph.items():
        for child in children:
            G.add_edge(parent, child)  # top-down graph

    if root_api not in G.nodes:
        raise ValueError(f"{root_api} not found in the graph.")

    # Now do a **post-order** DFS from root → down
    return list(nx.dfs_postorder_nodes(G, source=root_api))
