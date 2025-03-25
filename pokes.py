#it would be nice to make other functions here but nahh...

import requests

base_url = "https://pokeapi.co/api/v2/"

def get_poke(atr):
  url = f"{base_url}/pokemon/{atr}"
  response = requests.get(url)

  if response.status_code == 200:
    poke_data = response.json()
    return poke_data
  else:
    print(f"Failed to retrieve data {response.status_code}")