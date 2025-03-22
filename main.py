import configparser
import UI
import Engine
import Pokes
import networkx as nx
from rich.console import Console

# Maximum number of pokemons allowed to fight in an instance of a battle
#MAX_POKES = 3


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

def main():
  Config = configparser.ConfigParser()
  Config.read("config.ini")

  starterPoke = Pokes.get_poke(Config['Pokes']['Starter'])
 
  console = Console()

  console.print("Please type your name: ")
  name = input()
  player = Player(name, starterPoke)

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
  UI.updateNodes(G, source, dest, visited)

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
        for place in route:

          # Check if the player hasn't cleared the map yet
          if place == dest and visited.__len__() < G.number_of_nodes():
            console.print("[bold red]This place is only for those who stand at the top.[/bold red]")
          
          # If not, proceed to execute normal game logic
          else:
            if place not in visited:
              visited.append(place)
              Engine.initFight(player, console)
            
            console.print(f"current: {place}", style="green")
            UI.updateNodes(G, place, dest, visited)
            source = place
      
      else:
        print("Invalid index")
    else:
      print("Invalid input")


if __name__ == '__main__':
  main()