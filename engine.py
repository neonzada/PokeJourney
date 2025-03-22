import random
import math
import UI
import Pokes
from rich.console import Console

# Auto-battle implementation using greedy algorithms: always choose the best ratio between atk/def and sp-atk/sp-def
# Returns true if sp-atk/sp-def >= atk/def, false otherwise
def greedyATK(poke, enemyPoke):
  return True if ((poke["stats"][3]["base_stat"] / enemyPoke["stats"][4]["base_stat"]) >= (poke["stats"][1]["base_stat"] / enemyPoke["stats"][2]["base_stat"])) else False

def attackCheck(attacker, receiver, special, console):
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
def initFight(player, console):
  UI.plt.close('all')
  console.clear()
  poke = player.currentPoke

  id = random.randrange(1, 1025, 1)
  enemyPoke = Pokes.get_poke(id)

  enemyName = enemyPoke["name"]
  playerName = poke["name"]

  while True:
    UI.printPoke([poke, enemyPoke], console)
    console.print("[1] Attack\t[2 Special]\t[3] Block\t[4] Potions\t[5] Catch\t[6] Auto")
    sel = input()
    match sel:
      case '1':
        if attackCheck(poke, enemyPoke, False, console): break
        if attackCheck(enemyPoke, poke, False, console): break

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
          if attackCheck(poke, enemyPoke, isSpecial, console) : break
          if attackCheck(enemyPoke, poke, False, console) : break
        break
      case _:
        print("Invalid input")