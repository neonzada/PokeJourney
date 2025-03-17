import configparser
import networkx as nx
import matplotlib.pyplot as plt

# TODO: pode ser otimizado só atualizando o nó viajado e o src
def updateNodes(G, source, dest):
  plt.close('all')
  color_map = ['green' if node == source else 'red' if node == dest else 'lightblue' for node in G] 
  nx.draw_networkx_nodes(G, pos, node_size=500, node_color=color_map, node_shape='8')
  ax = plt.gca()
  ax.margins(0.08)
  plt.axis("off")
  plt.tight_layout()
  plt.show()

Config = configparser.ConfigParser()
Config.read("config.ini")

# Creating the graph
G = nx.Graph()

# Adding edges by reading .ini file
locs = Config.sections()[2:]

for location in locs:
  for key in Config[location]:
    G.add_edge(location, key, weight=int(Config[location][key]))


# Calculates the shortest distance between spawnpoint and the objective
source = Config['Locations']['Spawnpoint']
dest = Config['Locations']['FinalBattle']

print(f"\n\nShortest path: {nx.dijkstra_path(G, source, dest)}")
print(f"Length: {nx.dijkstra_path_length(G, source, dest)}")


# Print graph information
print("Nodes:", G.nodes)
print("Edges:", G.edges)

# Graph settings
# TODO: represent the graph with inverted weights to better visualize distance
pos = nx.spring_layout(G, weight="weight", seed=7)

# Nodes and edges
color_map = ['green' if node == source else 'red' if node == dest else 'lightblue' for node in G] 

nx.draw_networkx_nodes(G, pos, node_size=1000, node_color=color_map, node_shape='8')
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif", font_weight="bold")

# Weights
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6)


# Matplotlib visualization
ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.gcf().set_size_inches(15, 8)  # Set the size to 8x5 inches
plt.show()

# TODO: gameloop
#while True:
