import requests

base_url = "https://pokeapi.co/api/v2/"

def get_poke(name):
  url = f"{base_url}/pokemon/{name}"
  response = requests.get(url)

  if response.status_code == 200:
    poke_data = response.json()
    return poke_data
  else:
    print(f"Failed to retrieve data {response.status_code}")

poke_name = "pikachu"
poke_info = get_poke(poke_name)

if poke_info:
  print(f"{poke_info['name']}")
  print(f"{poke_info['id']}")
  print(f"{poke_info['height']}")