import configparser
import networkx as nx
import matplotlib.pyplot as plt

Config = configparser.ConfigParser()
Config.read("config.ini")

# Creating the graph
G = nx.Graph()

# Adding edges by reading .ini file
locs = Config.sections()[2:]

for location in locs:
  for key in Config[location]:
    G.add_edge(location, key, weight=Config[location][key])


# Print graph information
print("Nodes:", G.nodes)
print("Edges:", G.edges)

# Graph settings
# TODO: represent the graph with inverted weights to better visualize distance
pos = nx.spring_layout(G, weight="weight", seed=7)

# Nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue', node_shape='8')
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=7, font_family="sans-serif", font_weight="bold")

# Weights
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)

# Matplotlib visualization
ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()