import requests

BASE_URL = "https://pokeapi.co/api/v2/"


def get_json(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_pokemon_data(nome_o_id):
    pokemon_data = get_json(f"pokemon/{nome_o_id}")
    species_data = get_json(f"pokemon-species/{nome_o_id}")

    abilita_normali = []
    abilita_nascoste = []

    for abilita in pokemon_data["abilities"]:
        nome_abilita = abilita["ability"]["name"]
        if abilita["is_hidden"]:
            abilita_nascoste.append(nome_abilita)
        else:
            abilita_normali.append(nome_abilita)

    stats = {
        stat["stat"]["name"]: stat["base_stat"]
        for stat in pokemon_data["stats"]
    }

    pokedex_numbers = {
        entry["pokedex"]["name"]: entry["entry_number"]
        for entry in species_data["pokedex_numbers"]
    }

    return {
        "id": pokemon_data["id"],
        "nome": pokemon_data["name"],
        "altezza": pokemon_data["height"],
        "peso": pokemon_data["weight"],
        "tipi": [t["type"]["name"] for t in pokemon_data["types"]],
        "abilita": abilita_normali,
        "abilita_nascoste": abilita_nascoste,
        "stats": stats,
        "generazione_introduzione": species_data["generation"]["name"],
        "pokedex_numbers": pokedex_numbers,
    }
    
