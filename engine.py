import random
import math
import UI
import Pokes
import time

# Auto-battle implementation using greedy algorithms: always choose the best ratio between atk/def and sp-atk/sp-def
# Returns true if sp-atk/sp-def >= atk/def, false otherwise
def greedyATK(poke, enemyPoke):
  return True if ((poke["stats"][3]["base_stat"] / enemyPoke["stats"][4]["base_stat"]) >= (poke["stats"][1]["base_stat"] / enemyPoke["stats"][2]["base_stat"])) else False

def attackCheck(attacker, receiver, special, console):
  if special:
    # just abs() the thing cuz not really in the mood to deal with degative numbers rn
    # Special attack is calculated as follows: 0.75 to 1.25 random multiplier of the attackers' SP-ATK minus 40-60% of receivers' SP-DEF
    atk = abs(math.floor(random.randrange(75,125) * 0.01 * (attacker["stats"][3]["base_stat"] - (random.randrange(40, 60) * 0.01 * receiver["stats"][4]["base_stat"]))))
  else:
    # Basic attack is calculated as follows: 0.75 to 1.25 random multiplier of the attackers' ATK minus 5-15% of receivers' DEF
    atk = abs(math.floor(random.randrange(75,125) * 0.01 * (attacker["stats"][1]["base_stat"] - (random.randrange(5, 15) * 0.01 * receiver["stats"][2]["base_stat"]))))

  receiver["stats"][0]["base_stat"] -= atk

  console.print(f"{attacker['name']} dealt [bold red]{atk}[/bold red] damage to {receiver['name']}!")
  if receiver["stats"][0]["base_stat"] <= 0:
    console.print(f"{attacker['name']} wins!")
    time.sleep(1)
    return True
  else:
    return False

# TODO: special attacks reserved only for the boss (25% chance of triggering it, warning before)
def initFight(player, boss, console):
  UI.plt.close('all')
  console.clear()
  if boss:
    enemyPoke = boss
  else: 
    id = random.randrange(1, 1025, 1)
    enemyPoke = Pokes.get_poke(id)

  ongoing = True

  while ongoing:
    poke = player.currentPoke
    if poke["stats"][0]["base_stat"] < 0:
      console.print(f"{poke['name']} is dead!\n[0] Give up\t[_] Switch")
      x = input()
      if x == '0':
        return False
      else:
        sel = '4'
    
    else:
      UI.printPoke([poke, enemyPoke], console)
      console.print("[1] Attack\t[2] Special\t[3] Block\n[4] Switch\t[5] Catch\t[6] Auto")
      sel = input()
    
    match sel:
      # Attack
      case '1':
        if attackCheck(poke, enemyPoke, False, console): return True
        time.sleep(1)
        if attackCheck(enemyPoke, poke, False, console): continue
        time.sleep(1)
      
      # Special
      case '2':
        if attackCheck(poke, enemyPoke, True, console): return True
        time.sleep(1)
        if attackCheck(enemyPoke, poke, False, console): continue
        time.sleep(1)

      # Block
      case '3':
        # defend heavily the next attack (can be used for special attacks in boss)
        poke["stats"][2]["base_stat"] *= 2
        if attackCheck(enemyPoke, poke, False, console): continue
        time.sleep(1)
        poke["stats"][2]["base_stat"] /= 2

      # Switch
      case '4':
        console.clear()
        for i, pokemon in enumerate(player.pokeList):
          console.print(f"[{i}] - {pokemon['name']}")
        x = input()
        if x.isdigit():
          x = int(x)
          if 0 <= x < len(player.pokeList):
            player.currentPoke = player.pokeList[x]
            console.print(f"Current pokemon switched from [bold red]{poke['name']}[/bold red] to [bold green]{player.currentPoke['name']}[/bold green]")
          else:
            console.print("Invalid index")
        else:
          console.print("Invalid input")

      # Catch
      case '5':
        console.print(f"You tried catching {enemyPoke['name']}", end='')
        for i in range(3):
          console.print(".", end='')
          time.sleep(0.5)
        if random.randrange(0, 10, 1) > 5:
          player.pokeList.append(enemyPoke)
          console.print(f"\n{enemyPoke['name']} has been added to your PokeList!")
          time.sleep(1)
          ongoing = False
          break
        else:
          console.print(f"\nCapture failed!")
          time.sleep(1)
          if attackCheck(enemyPoke, poke, False, console): continue

      # Auto
      case '6':
        isSpecial = greedyATK(poke, enemyPoke)
        while True:
          if attackCheck(poke, enemyPoke, isSpecial, console): return True
          time.sleep(0.5)
          if attackCheck(enemyPoke, poke, False, console): continue
          time.sleep(0.5)

      case _:
        print("Invalid input")