# Asaf
import scripts.MakeNetworkxGraph
import networkx as nx

# TO DO: fix this file

G = MakeNetworkxGraph.__makegraph__(sep_type='comma', nodes_df_link='../databases/SmallGephiType.csv', weighted=True)

""" Shortest Path Stuff """
nodes = []
nodes_lower = []
for node in G.nodes:
    nodes.append(node)
    nodes_lower.append(node.lower())

while 1:
    source = input('Print shortest path of:\nSource: ')
    if source.lower() in nodes:
        target = input('Target: ')
        if target.lower() in nodes:
            s_path_length = nx.shortest_path_length(G, source=source, target=target)
            shortest_path = nx.shortest_path(G, source=source, target=target)
            print("Path length: %d" % s_path_length)
            print("\nPath from %s to %s:\n" % (source, target), shortest_path)
        else:
            print("Target node doesn't exist.")
    else:
        print("Source node doesn't exist.")
