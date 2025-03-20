import configparser
import networkx as nx
import matplotlib.pyplot as plt
import pokes
import random
from rich.console import Console

# Maximum number of pokemons allowed to fight in an instance of a battle
#MAX_POKES = 3

# Player class with name, current pokemons and current potions
class Player:
  def __init__(self, name, pokes, potions):
    self.name = name
    self.pokes = pokes
    self.potions = potions


def initFight():
  id = random.randrange(1, 1025, 1)
  poke_info = pokes.get_poke(id)
  stats = {stat["stat"]["name"]: stat["base_stat"] for stat in poke_info["stats"]}
  name = poke_info["name"]
  print(f"\nname: {name}")
  print("\nstats:")
  for stat_name, stat_value in stats.items():
    print(f"{stat_name}: {stat_value}")

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
  plt.show(block=False) #doesn't hang code


def main():
  Config = configparser.ConfigParser()
  Config.read("config.ini")

  console = Console()

  # Creating the graph
  G = nx.Graph()

  # Adding edges by reading .ini file
  locs = Config.sections()[2:]

  for location in locs:
    for key in Config[location]:
      G.add_edge(location, key, weight=int(Config[location][key]))


  # Calculates the shortest distance between spawnpoint and the objective using dijkstra's shortest path algorithm and prints just for the heck of it
  source = Config['Locations']['Spawnpoint']
  dest = Config['Locations']['FinalBattle']

  console.print(f"\n\nShortest path: {nx.dijkstra_path(G, source, dest)}", style="bold red")
  console.print(f"Length: {nx.dijkstra_path_length(G, source, dest)}", style="bold red")
  console.print("TIP: you can quit at any time by typing 'q'.", style="green")

  # Initialize list of visited nodes
  visited = [source]
  win_condition = False
  updateNodes(G, source, dest, visited)

  #gameloop while player hasn't won the game yet
  while not win_condition:
    console.print(f"visited nodes: {visited}")
    console.print("Where do you want to go?")
    for i, place in enumerate(G.nodes):
      if place == source:
        console.print(f"[{i}] - {place} (YOU ARE HERE)")
      else:
        console.print(f"[{i}] - {place}")

    x = input()
    if x == 'q':
      break

    if x.isdigit():
      x = int(x)
      if 0 <= x < len(G.nodes):
        # Calculates the shortest path to the specified location using dijkstra's algorithm
        route = nx.dijkstra_path(G, source, list(G.nodes)[x])
        #print(route)
        for place in route:

          # Check if the player hasn't cleared the map yet
          if place == dest and visited.__len__() < G.number_of_nodes():
            console.print("[bold red]This place is only for those who stand at the top.[/bold red]")
          
          # If not, proceed to execute normal game logic
          else:
            if place not in visited:
              visited.append(place)
              #print(visited.__len__())
              initFight()
            
            console.print(f"current: {place}", style="green")
            updateNodes(G, place, dest, visited)
      
      else:
        print("Invalid index")
    else:
      print("Invalid input")


if __name__ == '__main__':
  main()