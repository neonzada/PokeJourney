import configparser
import networkx as nx
import matplotlib.pyplot as plt
import pokes
import random
import math
from rich.console import Console
from rich.columns import Columns
from rich.table import Table

# Maximum number of pokemons allowed to fight in an instance of a battle
#MAX_POKES = 3
console = Console()

# Player class with name, current pokemons and current potions
class Player:
  def __init__(self, name, currentPoke):
    self.name = name
    self.currentPoke = currentPoke
    #self.potions = potions

# Pokemon class
# class Pokemon:
#   def __init__(self, name, hp, attack, defense, spatk, spdef, speed):
#     self.name = name
#     self.hp = hp
#     self.attack = attack
#     self.defense = defense
#     self.spatk = spatk
#     self.spdef = spdef
#     self.speed = speed

def printPoke(pokes_infos):

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

# Auto-battle implementation using greedy algorithms: always choose the best ratio between atk/def and sp-atk/sp-def
# Returns true if sp-atk/sp-def >= atk/def, false otherwise
def greedyATK(poke, enemyPoke):
  return True if ((poke["stats"][3]["base_stat"] / enemyPoke["stats"][4]["base_stat"]) >= (poke["stats"][1]["base_stat"] / enemyPoke["stats"][2]["base_stat"])) else False

def attackCheck(attacker, receiver, special):
  if special:
    # Special attack is calculated as follows: 0.75 to 1.25 random multiplier of the attackers' SP-ATK minus 40-60% of receivers' SP-DEF
    atk = math.floor(random.randrange(75,125) * 0.01 * (attacker["stats"][3]["base_stat"] - (random.randrange(40, 60) * 0.01 * receiver["stats"][4]["base_stat"])))
  else:
    # Basic attack is calculated as follows: 0.75 to 1.25 random multiplier of the attackers' ATK minus 5-15% of receivers' DEF
    atk = math.floor(random.randrange(75,125) * 0.01 * (attacker["stats"][1]["base_stat"] - (random.randrange(5, 15) * 0.01 * receiver["stats"][2]["base_stat"])))

  receiver["stats"][0]["base_stat"] -= atk

  console.print(f"{attacker['name']} dealt [bold red]{atk}[/bold red] damage to {receiver['name']}!")
  if receiver["stats"][0]["base_stat"] <= 0:
    console.print(f"{attacker['name']} wins!")
    return True
  else:
    return False

# TODO: special attacks reserved only for the boss (25% chance of triggering it, warning before)
# please for the love of god check if the poke is negative health
def initFight(player):
  plt.close('all')
  console.clear()
  poke = player.currentPoke

  id = random.randrange(1, 1025, 1)
  enemyPoke = pokes.get_poke(id)

  enemyName = enemyPoke["name"]
  playerName = poke["name"]

  while True:
    printPoke([poke, enemyPoke])
    console.print("[1] Attack\t[2 Special]\t[3] Block\t[4] Potions\t[5] Catch\t[6] Auto")
    sel = input()
    match sel:
      case '1':
        if attackCheck(poke, enemyPoke, False): break
        if attackCheck(enemyPoke, poke, False): break

      case '3':
        # defend heavily the next attack (can be used for special attacks in boss)
        poke["stats"][2]["base_stat"] *= 2
        if attackCheck(enemyPoke, poke): break
        poke["stats"][2]["base_stat"] /= 2

      case '4':
        # loop through every potion that the player has
        pass
      case '5':
        # 
        #if random.randrange(0, 10, 1) > 5 + 
        pass
      case '6':
        isSpecial = greedyATK(poke, enemyPoke)
        while True:
          if attackCheck(poke, enemyPoke, isSpecial) : break
          if attackCheck(enemyPoke, poke, False) : break
        break
      case _:
        print("Invalid input")


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


def main():
  Config = configparser.ConfigParser()
  Config.read("config.ini")

  starterPoke = pokes.get_poke(Config['Pokes']['Starter'])

  console.print("Please type your name: ")
  name = input()
  player = Player(name, starterPoke)

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
  console.print("TIP: you can quit on this screen by typing 'q'.", style="green")

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
        console.print(f"[{i}] - {place} [bold green](YOU ARE HERE)[/bold green]")
      elif place == dest:
        console.print(f"[{i}] - {place} [bold red](YOUR OBJECTIVE)[/bold red]")
      else:
        console.print(f"[{i}] - [white]{place}[/white]")

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
              initFight(player)
            
            console.print(f"current: {place}", style="green")
            updateNodes(G, place, dest, visited)
            source = place
      
      else:
        print("Invalid index")
    else:
      print("Invalid input")


if __name__ == '__main__':
  main()