from rich.console import Console
from rich.table import Table
import networkx as nx
import matplotlib.pyplot as plt

def printPoke(pokes_infos, console):

  table = Table()

  for poke_info in pokes_infos:
    name = poke_info["name"]
    table.add_column(name, justify="center")

  rows = []
  for poke_info in pokes_infos:
    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in poke_info["stats"]}
    rows.append(stats)

  for stat_name in rows[0].keys():
    row = []
    for stats in rows:
      row.append(f"{stat_name}: {stats[stat_name]}")
    table.add_row(*row)

  console.print(table)

def updateNodes(G, source, dest, visited):
  plt.close('all')

  # Graph settings
  pos = nx.spring_layout(G, weight=None, seed=7)

  # Nodes and edges
  color_map = ['green' if node == source 
                else 'red' if node == dest
                else 'blue' if node in visited
                else 'lightblue'
               for node in G] 

  nx.draw_networkx_nodes(G, pos, node_size=500, node_color=color_map, node_shape='8')
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
  plt.gcf().set_size_inches(12, 7)  #12x7 inches
  plt.gcf().canvas.manager.set_window_title("PokeJourney")
  plt.show(block=False) #doesn't hang code