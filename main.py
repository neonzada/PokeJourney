import configparser
import UI
import Engine
import Pokes
import time
import networkx as nx
from rich.console import Console

# Maximum number of pokemons allowed to fight in an instance of a battle
#MAX_POKES = 3


# Player class with name, current pokemons and current potions
class Player:
  def __init__(self, currentPoke, pokeList):
    self.currentPoke = currentPoke
    self.pokeList = pokeList
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
  godmode = False #for debugging purposes

  Config = configparser.ConfigParser()
  console = Console()
  G = nx.Graph()
  
  Config.read("config.ini")
  starterPoke = Pokes.get_poke(Config['Pokes']['Starter'])
  bossPoke = Pokes.get_poke(Config['Pokes']['Rival'])

  if godmode:
    for stat_entry in starterPoke["stats"]:
      stat_entry["base_stat"] = 9999

  player = Player(starterPoke, [starterPoke])

  #adding edges by reading .ini file
  locs = Config.sections()[2:]
  for location in locs:
    for key in Config[location]:
      G.add_edge(location, key, weight=int(Config[location][key]))

  #shortest distance between spawnpoint and the objective using dijkstra's shortest path algorithm and prints just for the heck of it
  source = Config['Locations']['Spawnpoint']
  dest = Config['Locations']['FinalBattle']

  console.print(f"\n\nShortest path: {nx.dijkstra_path(G, source, dest)}", style="bold red")
  console.print(f"Length: {nx.dijkstra_path_length(G, source, dest)}", style="bold red")
  console.print("TIP: you can quit on this screen by typing 'q'.", style="green")

  #init list of visited nodes
  visited = [source]
  win_condition = False
  running = True
  UI.updateNodes(G, source, dest, visited)

  #gameloop
  while running:
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
        #calculates the shortest path to the specified location using dijkstra's algorithm
        route = nx.dijkstra_path(G, source, list(G.nodes)[x])
        for place in route:
          #check if already dead lol
          if not running:
            break

          #check if the player hasn't cleared the map yet
          if place == dest:
            if visited.__len__() < G.number_of_nodes() - 1:
              console.print("[bold red]This place is only for those who stand at the top.[/bold red]")
              time.sleep(1.5)
            else:
              console.print("[bold red]Entering boss fight...[/bold red]")
              time.sleep(1.5)
              win_condition = True if Engine.initFight(player, bossPoke, console) else False
              running = False
          
          #if not, proceed to execute normal game logic
          else:
            if place not in visited:
              visited.append(place)
              if Engine.initFight(player, False, console) == False:
                running = False #if player doesn't survive, break loop and end game
            

            console.print(f"current: {place}", style="green")
            UI.updateNodes(G, place, dest, visited)
            source = place
      
      else:
        print("Invalid index")
    else:
      print("Invalid input")

  if(win_condition):
    console.print("Congratulations, you beat the [bold red]final boss[/bold red] and won the PokeJourney!")
  else:
    console.print("[bold red]Game over![/bold red]")

if __name__ == '__main__':
  main()