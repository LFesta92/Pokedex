import json
from pathlib import Path
from urllib import error, parse, request as urlrequest

from flask import Blueprint, jsonify, redirect, render_template, request, send_from_directory, url_for


main_blueprint = Blueprint("main", __name__)
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
SPRITES_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "pokemon"
ITEMS_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "items"
TYPE_ICONS_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "types" / "generation-viii" / "sword-shield"
MAX_POKEDEX_ID = 10249
TYPE_ICON_IDS = {
    "normal": 1,
    "fighting": 2,
    "flying": 3,
    "poison": 4,
    "ground": 5,
    "rock": 6,
    "bug": 7,
    "ghost": 8,
    "steel": 9,
    "fire": 10,
    "water": 11,
    "grass": 12,
    "electric": 13,
    "psychic": 14,
    "ice": 15,
    "dragon": 16,
    "dark": 17,
    "fairy": 18,
}
TYPE_COLORS = {
    "normal": "#a8a77a",
    "fire": "#ee8130",
    "water": "#6390f0",
    "electric": "#f7d02c",
    "grass": "#7ac74c",
    "ice": "#96d9d6",
    "fighting": "#c22e28",
    "poison": "#a33ea1",
    "ground": "#e2bf65",
    "flying": "#a98ff3",
    "psychic": "#f95587",
    "bug": "#a6b91a",
    "rock": "#b6a136",
    "ghost": "#735797",
    "dragon": "#6f35fc",
    "dark": "#705746",
    "steel": "#b7b7ce",
    "fairy": "#d685ad",
}
STAT_STYLES = {
    "hp": {"label": "PS", "color": "#7de33b"},
    "attack": {"label": "Attacco", "color": "#f3cb2f"},
    "defense": {"label": "Difesa", "color": "#f28b30"},
    "special-attack": {"label": "Att. Sp.", "color": "#38c1ed"},
    "special-defense": {"label": "Dif. Sp.", "color": "#5a7fe5"},
    "speed": {"label": "Velocita", "color": "#d953df"},
}
GENERATION_CARDS = [
    {"label": "Gen I / Kanto", "image": "img/kanto.png", "href": "gen1.html", "start": 1, "end": 151},
    {"label": "Gen II / Johto", "image": "img/johto.png", "href": "gen2.html", "start": 152, "end": 251},
    {"label": "Gen III / Hoenn", "image": "img/hoenn.png", "href": "gen3.html", "start": 252, "end": 386},
    {"label": "Gen IV / Sinnoh", "image": "img/sinnoh.png", "href": "gen4.html", "start": 387, "end": 493},
    {"label": "Gen V / Unova", "image": "img/unova.png", "href": "gen5.html", "start": 494, "end": 649},
    {"label": "Gen VI / Kalos", "image": "img/kalos.png", "href": "gen6.html", "start": 650, "end": 721},
    {"label": "Gen VII / Alola", "image": "img/alola.png", "href": "gen7.html", "start": 722, "end": 809},
    {"label": "Gen VIII / Galar", "image": "img/galar.png", "href": "gen8.html", "start": 810, "end": 905},
    {"label": "Gen IX / Paldea", "image": "img/paldea.png", "href": "gen9.html", "start": 906, "end": 1035},
    {"label": "Leggende / Hisui", "image": "img/hisui-new.png", "href": "hisui.html"},
    {"label": "Forme Alola", "image": "img/alola.png", "href": "alola-forms.html"},
    {"label": "Forme Mega", "image": "img/megavenusaur.png", "href": "mega-forms.html"},
    {"label": "Forme Giga-Max", "image": "img/gigamax.png", "href": "gigamax-forms.html"},
]


def fetch_json(url, params=None):
    if params:
        url = f"{url}?{parse.urlencode(params)}"

    req = urlrequest.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )
    opener = urlrequest.build_opener(urlrequest.ProxyHandler({}))

    with opener.open(req, timeout=10) as response:
        return json.load(response)


def clean_text(value):
    return value.replace("\n", " ").replace("\f", " ")


def get_localized_value(entries, language, value_key):
    for entry in entries:
        if entry["language"]["name"] == language:
            return clean_text(entry[value_key])
    return None


def get_pokemon(identifier):
    data = fetch_json(f"{POKEAPI_BASE_URL}/pokemon/{identifier}")
    species = fetch_json(data["species"]["url"])

    description = (
        get_localized_value(species["flavor_text_entries"], "it", "flavor_text")
        or get_localized_value(species["flavor_text_entries"], "en", "flavor_text")
        or "Descrizione non disponibile."
    )

    type_entries = []
    for item in data["types"]:
        slug = item["type"]["name"]
        icon_id = TYPE_ICON_IDS.get(slug)
        type_entries.append(
            {
                "name": slug.title(),
                "slug": slug,
                "icon": f"/type-icons/{icon_id}.png" if icon_id else "",
                "color": TYPE_COLORS.get(slug, "#9ca3af"),
            }
        )

    abilities = []
    for item in data["abilities"]:
        slug = item["ability"]["name"]
        ability_data = fetch_json(item["ability"]["url"])
        localized_name = (
            get_localized_value(ability_data.get("names", []), "it", "name")
            or get_localized_value(ability_data.get("names", []), "en", "name")
            or slug.replace("-", " ").title()
        )
        abilities.append(
            {
                "name": localized_name,
                "slug": slug,
            }
        )

    stats = []
    total_stats = 0
    for item in data["stats"]:
        slug = item["stat"]["name"]
        meta = STAT_STYLES.get(slug, {"label": slug.replace("-", " ").title(), "color": "#9ca3af"})
        value = item["base_stat"]
        total_stats += value
        stats.append(
            {
                "name": meta["label"],
                "value": value,
                "bar_width": min(round((value / 255) * 100), 100),
                "color": meta["color"],
            }
        )

    return {
        "id": data["id"],
        "name": data["name"].title(),
        "image": (
            data["sprites"]["other"]["official-artwork"]["front_default"]
            or data["sprites"]["front_default"]
        ),
        "types": type_entries,
        "height": data["height"] / 10,
        "weight": data["weight"] / 10,
        "abilities": abilities,
        "description": description,
        "stats": stats,
        "total_stats": total_stats,
    }


def get_ability_details(identifier):
    data = fetch_json(f"{POKEAPI_BASE_URL}/ability/{identifier}")

    effect_entries = data.get("effect_entries", [])
    flavor_entries = data.get("flavor_text_entries", [])
    italian_flavor = get_localized_value(flavor_entries, "it", "flavor_text")
    effect_text = (
        get_localized_value(effect_entries, "it", "effect")
        or italian_flavor
        or get_localized_value(effect_entries, "en", "effect")
        or "Effetto non disponibile."
    )
    short_effect = (
        get_localized_value(effect_entries, "it", "short_effect")
        or italian_flavor
        or get_localized_value(effect_entries, "en", "short_effect")
        or "Descrizione breve non disponibile."
    )
    localized_name = (
        get_localized_value(data.get("names", []), "it", "name")
        or get_localized_value(data.get("names", []), "en", "name")
        or data["name"].replace("-", " ").title()
    )

    return {
        "name": localized_name,
        "effect": effect_text,
        "short_effect": short_effect,
    }


def get_sprite_url(pokemon_id):
    sprite_path = SPRITES_DIR / f"{pokemon_id}.png"
    if sprite_path.exists():
        return f"/pokemon-sprites/{pokemon_id}.png"

    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"


def get_generation_pokemon(start_id, end_id):
    offset = start_id - 1
    limit = end_id - start_id + 1
    data = fetch_json(f"{POKEAPI_BASE_URL}/pokemon", params={"limit": limit, "offset": offset})
    pokemon_list = []

    for item in data["results"]:
        pokemon_id = int(item["url"].rstrip("/").split("/")[-1])
        if start_id <= pokemon_id <= end_id:
            pokemon_list.append(
                {
                    "id": pokemon_id,
                    "name": item["name"].title(),
                    "sprite": get_sprite_url(pokemon_id),
                }
            )

    return pokemon_list


def get_pokemon_summary(identifier):
    data = fetch_json(f"{POKEAPI_BASE_URL}/pokemon/{identifier}")
    return {
        "id": data["id"],
        "name": data["name"].replace("-", " ").title(),
        "sprite": get_sprite_url(data["id"]),
    }


def get_pokemon_by_ids(pokemon_ids):
    pokemon_list = []
    for pokemon_id in pokemon_ids:
        try:
            pokemon_list.append(get_pokemon_summary(pokemon_id))
        except error.HTTPError:
            continue
    return pokemon_list


def get_adjacent_pokemon_ids(pokemon_id):
    previous_id = pokemon_id - 1 if pokemon_id > 1 else None
    next_id = pokemon_id + 1 if pokemon_id < MAX_POKEDEX_ID else None
    return previous_id, next_id


@main_blueprint.route("/pokemon-sprites/<path:filename>")
def pokemon_sprite(filename):
    return send_from_directory(SPRITES_DIR, filename)


@main_blueprint.route("/type-icons/<path:filename>")
def type_icon(filename):
    return send_from_directory(TYPE_ICONS_DIR, filename)


@main_blueprint.route("/api/ability/<slug>")
def ability_details(slug):
    try:
        return jsonify(get_ability_details(slug))
    except error.HTTPError:
        return jsonify({"error": "Abilita non trovata."}), 404
    except Exception:
        return jsonify({"error": "Errore durante la richiesta a PokeAPI."}), 500


@main_blueprint.route("/")
def home():
    query = request.args.get("pokemon", "").strip()

    if query:
        return redirect(url_for("main.pokedex", pokemon=query) + "#pokedex-view")

    return render_template(
        "home.html",
        query=query,
        error=None,
        generations=GENERATION_CARDS,
    )


@main_blueprint.route("/pokedex")
def pokedex():
    query = request.args.get("pokemon", "").strip() or "1"
    error_message = None
    pokemon = None
    previous_id = None
    next_id = None

    try:
        pokemon = get_pokemon(query.lower())
        previous_id, next_id = get_adjacent_pokemon_ids(pokemon["id"])
    except error.HTTPError:
        error_message = "Pokemon non trovato."
    except Exception:
        error_message = "Errore durante la richiesta a PokeAPI."

    return render_template(
        "pokedex.html",
        query=query,
        error=error_message,
        pokemon=pokemon,
        previous_id=previous_id,
        next_id=next_id,
    )


def render_generation_page(generation_name, start_id, end_id, page_name, pokemon_ids=None, range_label=None, description=None):
    query = request.args.get("pokemon", "").strip()

    if query:
        return redirect(url_for("main.pokedex", pokemon=query) + "#pokedex-view")

    error_message = None

    try:
        if pokemon_ids is not None:
            pokemon_list = get_pokemon_by_ids(pokemon_ids)
        else:
            pokemon_list = get_generation_pokemon(start_id, end_id)
    except error.HTTPError:
        error_message = "Pokemon non trovato."
        if pokemon_ids is not None:
            pokemon_list = get_pokemon_by_ids(pokemon_ids)
        else:
            pokemon_list = get_generation_pokemon(start_id, end_id)
    except Exception:
        error_message = "Errore durante la richiesta a PokeAPI."
        pokemon_list = []

    return render_template(
        "generation.html",
        generation_name=generation_name,
        generation_range=range_label or f"Tutti i Pokemon da {start_id} a {end_id}.",
        generation_description=description or f"Cerca un Pokemon di {generation_name} e scorri la griglia completa degli sprite della generazione.",
        action_path=page_name,
        query=query,
        error=error_message,
        pokemon_list=pokemon_list,
    )


@main_blueprint.route("/gen1.html")
def gen1():
    return render_generation_page("Gen I / Kanto", 1, 151, "/gen1.html")


@main_blueprint.route("/gen2.html")
def gen2():
    return render_generation_page("Gen II / Johto", 152, 251, "/gen2.html")


@main_blueprint.route("/gen3.html")
def gen3():
    return render_generation_page("Gen III / Hoenn", 252, 386, "/gen3.html")


@main_blueprint.route("/gen4.html")
def gen4():
    return render_generation_page("Gen IV / Sinnoh", 387, 493, "/gen4.html")


@main_blueprint.route("/gen5.html")
def gen5():
    return render_generation_page("Gen V / Unova", 494, 649, "/gen5.html")


@main_blueprint.route("/gen6.html")
def gen6():
    return render_generation_page("Gen VI / Kalos", 650, 721, "/gen6.html")


@main_blueprint.route("/gen7.html")
def gen7():
    return render_generation_page("Gen VII / Alola", 722, 809, "/gen7.html")


@main_blueprint.route("/gen8.html")
def gen8():
    return render_generation_page("Gen VIII / Galar", 810, 905, "/gen8.html")


@main_blueprint.route("/gen9.html")
def gen9():
    return render_generation_page("Gen IX / Paldea", 906, 1035, "/gen9.html")


@main_blueprint.route("/hisui.html")
def hisui():
    return render_generation_page(
        "Leggende / Hisui",
        10229,
        10249,
        "/hisui.html",
        pokemon_ids=list(range(10229, 10250)),
        range_label="Forme da 10229 a 10249.",
        description="Scorri tutte le forme Hisui presenti nei tuoi sprite locali.",
    )


@main_blueprint.route("/alola-forms.html")
def alola_forms():
    return render_generation_page(
        "Forme Alola",
        10100,
        10115,
        "/alola-forms.html",
        pokemon_ids=list(range(10100, 10116)),
        range_label="Forme da 10100 a 10115.",
        description="Scorri tutte le forme Alola presenti nei tuoi sprite locali.",
    )


@main_blueprint.route("/mega-forms.html")
def mega_forms():
    mega_ids = list(range(10033, 10080)) + list(range(10087, 10091))
    return render_generation_page(
        "Forme Mega",
        10033,
        10090,
        "/mega-forms.html",
        pokemon_ids=mega_ids,
        range_label="Forme da 10033 a 10079 e da 10087 a 10090.",
        description="Scorri tutte le Mega Evoluzioni presenti nei tuoi sprite locali.",
    )


@main_blueprint.route("/gigamax-forms.html")
def gigamax_forms():
    gigamax_ids = [10190] + list(range(10195, 10229))
    return render_generation_page(
        "Forme Giga-Max",
        10190,
        10228,
        "/gigamax-forms.html",
        pokemon_ids=gigamax_ids,
        range_label="Forme 10190 e da 10195 a 10228.",
        description="Scorri tutte le forme Giga-Max presenti nei tuoi sprite locali.",
    )
