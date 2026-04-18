import json
import random
from pathlib import Path
from urllib import error, parse, request as urlrequest

from flask import Blueprint, jsonify, redirect, render_template, request, send_from_directory, session, url_for

from database.db_manager import DatabaseManager
from services.box_service import BoxServices
from services.user_service import UserService


main_blueprint = Blueprint("main", __name__)
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
SPRITES_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "pokemon"
ITEMS_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "items"
TYPE_ICONS_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "types" / "generation-viii" / "sword-shield"
BADGES_DIR = Path(__file__).resolve().parent / "sprites" / "sprites" / "badges"
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
FORM_LABELS = {
    "-alola": "Forma Alola",
    "-hisui": "Forma Hisui",
    "-mega-x": "Mega X",
    "-mega-y": "Mega Y",
    "-mega": "Mega",
    "-gmax": "Giga-Max",
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
    {"label": "Forme Alola", "image": "img/alola-forms.png", "href": "alola-forms.html"},
    {"label": "Forme Mega", "image": "img/megavenusaur.png", "href": "mega-forms.html"},
    {"label": "Forme Giga-Max", "image": "img/gigamax.png", "href": "gigamax-forms.html"},
]
GAME_CARDS = [
    {"label": "Zona Safari", "image": "img/catturali-tutti.png", "href": "/zona-safari"},
    {"label": "Torre Lotta", "image": "img/vs.png", "href": "/torre-lotta"},
]
SAFARI_BALLS = {
    "pokeball": {"label": "Poke Ball", "chance": 40, "count": 2},
    "megaball": {"label": "Mega Ball", "chance": 50, "count": 2},
    "ultraball": {"label": "Ultra Ball", "chance": 70, "count": 1},
}
TOWER_MAX_HP = 120
TOWER_PLAYER_LEVEL = 62
db_manager = DatabaseManager()
user_service = UserService(db_manager)
box_service = BoxServices(db_manager)


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


def normalize_search_query(value):
    return "-".join(value.strip().lower().split())


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


def get_badge_url(filename):
    return f"/badge-assets/{filename}"


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


def is_special_form_name(name):
    return any(keyword in name for keyword in FORM_LABELS)


def get_form_display_label(variety_name, default_name):
    if variety_name == default_name:
        return "Forma Base"

    for keyword, label in FORM_LABELS.items():
        if keyword in variety_name:
            return label

    return variety_name.replace(default_name, "").replace("-", " ").strip().title() or "Forma Speciale"


def get_generation_display_name(generation_name):
    if generation_name.startswith("Gen ") and "/" in generation_name:
        return generation_name.split("/", 1)[1].strip()
    return generation_name


def get_generation_navigation(page_name):
    hrefs = [card["href"] for card in GENERATION_CARDS]
    if page_name.startswith("/"):
        page_name = page_name[1:]
    if page_name not in hrefs:
        return None, None

    index = hrefs.index(page_name)
    previous_card = GENERATION_CARDS[index - 1]
    next_card = GENERATION_CARDS[(index + 1) % len(GENERATION_CARDS)]
    return previous_card, next_card


def get_minigame_navigation(path_name):
    hrefs = [card["href"] for card in GAME_CARDS]
    if path_name not in hrefs:
        return None, None

    index = hrefs.index(path_name)
    previous_game = GAME_CARDS[index - 1]
    next_game = GAME_CARDS[(index + 1) % len(GAME_CARDS)]
    return previous_game, next_game


def get_form_choices_for_species(species_name):
    species = fetch_json(f"{POKEAPI_BASE_URL}/pokemon-species/{species_name}")
    choices = []

    for variety in species.get("varieties", []):
        pokemon_name = variety["pokemon"]["name"]
        include = variety.get("is_default", False) or is_special_form_name(pokemon_name)
        if not include:
            continue

        summary = get_pokemon_summary(pokemon_name)
        sprite_exists = (SPRITES_DIR / f"{summary['id']}.png").exists()
        if not sprite_exists:
            continue

        choices.append(
            {
                "id": summary["id"],
                "name": summary["name"],
                "sprite": summary["sprite"],
                "label": get_form_display_label(pokemon_name, species_name),
            }
        )

    choices.sort(key=lambda item: item["id"])
    return choices


def resolve_search(query):
    normalized_query = normalize_search_query(query)

    if not normalized_query:
        return {"status": "empty"}

    if normalized_query.isdigit():
        try:
            pokemon = get_pokemon_summary(normalized_query)
            return {"status": "direct", "pokemon_id": pokemon["id"]}
        except error.HTTPError:
            return {"status": "error", "message": "Pokemon non trovato. Riprova."}
        except Exception:
            return {"status": "error", "message": "Errore durante la richiesta a PokeAPI."}

    if is_special_form_name(normalized_query):
        try:
            pokemon = get_pokemon_summary(normalized_query)
            return {"status": "direct", "pokemon_id": pokemon["id"]}
        except error.HTTPError:
            return {"status": "error", "message": "Pokemon non trovato. Riprova."}
        except Exception:
            return {"status": "error", "message": "Errore durante la richiesta a PokeAPI."}

    try:
        choices = get_form_choices_for_species(normalized_query)
        if len(choices) > 1:
            return {"status": "choice", "species": normalized_query, "choices": choices}
        if len(choices) == 1:
            return {"status": "direct", "pokemon_id": choices[0]["id"]}
    except error.HTTPError:
        pass
    except Exception:
        return {"status": "error", "message": "Errore durante la richiesta a PokeAPI."}

    try:
        pokemon = get_pokemon_summary(normalized_query)
        return {"status": "direct", "pokemon_id": pokemon["id"]}
    except error.HTTPError:
        return {"status": "error", "message": "Pokemon non trovato. Riprova."}
    except Exception:
        return {"status": "error", "message": "Errore durante la richiesta a PokeAPI."}


def get_adjacent_pokemon_ids(pokemon_id):
    previous_id = pokemon_id - 1 if pokemon_id > 1 else None
    next_id = pokemon_id + 1 if pokemon_id < MAX_POKEDEX_ID else None
    return previous_id, next_id


def build_battle_pokemon(pokemon_id, display_name=None, level=TOWER_PLAYER_LEVEL, side="player"):
    data = fetch_json(f"{POKEAPI_BASE_URL}/pokemon/{pokemon_id}")
    total_stats = sum(item["base_stat"] for item in data["stats"])
    speed_value = next((item["base_stat"] for item in data["stats"] if item["stat"]["name"] == "speed"), 50)

    return {
        "id": data["id"],
        "name": display_name or data["name"].replace("-", " ").title(),
        "level": level,
        "total_stats": total_stats,
        "speed": speed_value,
        "hp": TOWER_MAX_HP,
        "max_hp": TOWER_MAX_HP,
        "sprite_front": get_sprite_url(data["id"]),
        "side": side,
    }


def reset_battle_team(team):
    for pokemon in team:
        pokemon["hp"] = pokemon["max_hp"]


def get_first_available_pokemon(team):
    for pokemon in team:
        if pokemon["hp"] > 0:
            return pokemon
    return None


def team_is_defeated(team):
    return get_first_available_pokemon(team) is None


def calculate_tower_damage(attacker, defender):
    base_damage = (attacker["total_stats"] / 8) + (attacker["level"] / 6) - (defender["total_stats"] / 110)
    damage = max(24, round(base_damage * random.uniform(0.94, 1.1)))
    critical = random.random() < 0.08
    if critical:
        damage = round(damage * 1.25)
    return min(damage, defender["hp"]), critical


def simulate_tower_turn(player_team, npc_team):
    log = []
    player_active = get_first_available_pokemon(player_team)
    npc_active = get_first_available_pokemon(npc_team)
    if not player_active or not npc_active:
        return log

    attack_order = [
        ("player", player_active, npc_active),
        ("npc", npc_active, player_active),
    ]
    if npc_active["speed"] > player_active["speed"]:
        attack_order.reverse()

    for _, attacker, defender in attack_order:
        if attacker["hp"] <= 0 or defender["hp"] <= 0:
            continue

        damage, critical = calculate_tower_damage(attacker, defender)
        defender["hp"] = max(0, defender["hp"] - damage)
        message = f"{attacker['name']} infligge {damage} danni a {defender['name']}."
        if critical:
            message += " Colpo critico!"
        log.append(message)

        if defender["hp"] == 0:
            log.append(f"{defender['name']} e esausto.")

    return log


def get_tower_state():
    return session.get("battle_tower")


def set_tower_state(state):
    session["battle_tower"] = state
    session.modified = True


def clear_tower_state():
    session.pop("battle_tower", None)
    session.modified = True


def get_npc_pool():
    connection = db_manager.get_connection()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT n.id_npc, n.username, t.slot, t.id_pokemon_api, t.nome_pokemon, t.livello
            FROM npc n
            JOIN npc_team t ON t.id_npc = n.id_npc
            ORDER BY n.id_npc, t.slot
            """
        )
        rows = cursor.fetchall()
    except Exception as error:
        print(f"Recupero NPC non riuscito {error}")
        return []
    finally:
        cursor.close()

    npc_map = {}
    for row in rows:
        npc_entry = npc_map.setdefault(
            row["id_npc"],
            {"id_npc": row["id_npc"], "username": row["username"], "team": []},
        )
        npc_entry["team"].append(
            {
                "slot": row["slot"],
                "id_pokemon_api": row["id_pokemon_api"],
                "nome_pokemon": row["nome_pokemon"],
                "livello": row["livello"],
            }
        )

    return list(npc_map.values())


def build_random_npc_battles(total=3):
    npc_pool = get_npc_pool()
    if len(npc_pool) < total:
        return []

    selected_npcs = random.sample(npc_pool, total)
    battles = []
    for npc in selected_npcs:
        team = [
            build_battle_pokemon(member["id_pokemon_api"], member["nome_pokemon"], member["livello"], side="npc")
            for member in sorted(npc["team"], key=lambda item: item["slot"])
        ]
        battles.append(
            {
                "id_npc": npc["id_npc"],
                "username": npc["username"],
                "team": team,
            }
        )
    return battles


def get_badge_filenames():
    return sorted(file.name for file in BADGES_DIR.glob("*.png") if file.is_file())


def award_random_badge(id_utente):
    badge_filenames = get_badge_filenames()
    if not badge_filenames:
        return None

    connection = db_manager.get_connection()
    if not connection:
        return None

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT nome_png FROM medaglia WHERE id_utente=%s", (id_utente,))
        owned_badges = {row[0] for row in cursor.fetchall() if row[0]}
        available_badges = [filename for filename in badge_filenames if filename not in owned_badges]
        if not available_badges:
            return {"filename": None, "already_complete": True}

        selected_badge = random.choice(available_badges)
        cursor.execute(
            "INSERT INTO medaglia (nome_png, id_utente) VALUES (%s, %s)",
            (selected_badge, id_utente),
        )
        connection.commit()
        return {"filename": selected_badge, "already_complete": False}
    except Exception as error:
        print(f"Assegnazione medaglia non riuscita {error}")
        connection.rollback()
        return None
    finally:
        cursor.close()


def get_user_badges(id_utente):
    connection = db_manager.get_connection()
    if not connection:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id_medaglia, nome_png FROM medaglia WHERE id_utente=%s ORDER BY id_medaglia DESC",
            (id_utente,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row["id_medaglia"],
                "filename": row["nome_png"],
                "url": get_badge_url(row["nome_png"]),
                "name": Path(row["nome_png"]).stem.replace("-", " ").replace("_", " ").title(),
            }
            for row in rows
            if row.get("nome_png")
        ]
    except Exception as error:
        print(f"Recupero medaglie non riuscito {error}")
        return []
    finally:
        cursor.close()


def get_logged_user():
    username = session.get("username")
    if not username:
        return None
    return user_service.get_user_by_username(username)


def get_box_feedback_message(status):
    messages = {
        "added": "Pokemon aggiunto al box con successo.",
        "exists": "Questo Pokemon e gia presente nel tuo box.",
        "login-required": "Devi effettuare il login per salvare un Pokemon nel box.",
        "db-error": "Salvataggio non riuscito. Controlla la connessione al database.",
    }
    return messages.get(status)


def get_available_pokemon_ids():
    pokemon_ids = []
    for sprite_path in SPRITES_DIR.glob("*.png"):
        if sprite_path.stem.isdigit():
            pokemon_ids.append(int(sprite_path.stem))
    return sorted(set(pokemon_ids))


def build_safari_encounters(total=5):
    available_ids = get_available_pokemon_ids()
    if len(available_ids) < total:
        return []

    selected_ids = random.sample(available_ids, total)
    encounters = []
    for pokemon_id in selected_ids:
        summary = get_pokemon_summary(pokemon_id)
        encounters.append(
            {
                "id": summary["id"],
                "name": summary["name"],
                "sprite": summary["sprite"],
            }
        )
    return encounters


def create_safari_game():
    return {
        "encounters": build_safari_encounters(),
        "current_index": 0,
        "balls": {slug: meta["count"] for slug, meta in SAFARI_BALLS.items()},
        "phase": "encounter",
        "result": None,
        "saved_ids": [],
        "history": [],
    }


def get_safari_state():
    return session.get("safari_game")


def set_safari_state(state):
    session["safari_game"] = state
    session.modified = True


def clear_safari_state():
    session.pop("safari_game", None)
    session.modified = True


def get_safari_ball_view(state):
    view = []
    for slug, meta in SAFARI_BALLS.items():
        view.append(
            {
                "slug": slug,
                "label": meta["label"],
                "chance": meta["chance"],
                "remaining": state["balls"].get(slug, 0),
            }
        )
    return view


def get_safari_current_encounter(state):
    index = state.get("current_index", 0)
    encounters = state.get("encounters", [])
    if 0 <= index < len(encounters):
        return encounters[index]
    return None


def finish_safari_game(state, extra_message=None):
    state["phase"] = "finished"
    if extra_message:
        state["final_message"] = extra_message
    set_safari_state(state)


@main_blueprint.route("/pokemon-sprites/<path:filename>")
def pokemon_sprite(filename):
    return send_from_directory(SPRITES_DIR, filename)


@main_blueprint.route("/badge-assets/<path:filename>")
def badge_asset(filename):
    return send_from_directory(BADGES_DIR, filename)


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


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next", "") if request.method == "GET" else request.form.get("next", "")
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            error_message = "Inserisci username e password."
        else:
            user = user_service.login(username, password)
            if user:
                session["username"] = user["username"]
                if next_page:
                    return redirect(next_page)
                return redirect(url_for("main.home"))
            error_message = "Credenziali non valide o database non disponibile."

    return render_template(
        "auth.html",
        mode="login",
        next_page=next_page,
        error=error_message,
    )


@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    next_page = request.args.get("next", "") if request.method == "GET" else request.form.get("next", "")
    error_message = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        email = request.form.get("email", "").strip()

        if not username or not password or not email:
            error_message = "Compila tutti i campi."
        else:
            created = user_service.register_user(username, password, email)
            if created:
                session["username"] = username
                if next_page:
                    return redirect(next_page)
                return redirect(url_for("main.box"))
            error_message = "Registrazione non riuscita. Username, email o database da controllare."

    return render_template(
        "auth.html",
        mode="register",
        next_page=next_page,
        error=error_message,
    )


@main_blueprint.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("main.home"))


@main_blueprint.route("/box")
def box():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=request.path))

    raw_box_entries = box_service.get_pokemon(user["id_utente"])
    box_entries = [
        {
            "id": item["id_pokemon_api"],
            "name": item["nome_pokemon"],
            "sprite": get_sprite_url(item["id_pokemon_api"]),
        }
        for item in raw_box_entries
    ]
    return render_template(
        "box.html",
        user=user,
        box_entries=box_entries,
    )


@main_blueprint.route("/medaglie")
def medaglie():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=request.path))

    badge_entries = get_user_badges(user["id_utente"])
    return render_template(
        "medaglie.html",
        user=user,
        badge_entries=badge_entries,
    )


@main_blueprint.route("/torre-lotta")
def torre_lotta():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=request.path))
    previous_game, next_game = get_minigame_navigation("/torre-lotta")

    box_entries = box_service.get_pokemon(user["id_utente"])
    selection_entries = [
        {
            "id": item["id_pokemon_api"],
            "name": item["nome_pokemon"],
            "sprite": get_sprite_url(item["id_pokemon_api"]),
        }
        for item in box_entries
    ]

    state = get_tower_state()
    if not state:
        return render_template(
            "torre_lotta.html",
            user=user,
            phase="team_select",
            box_entries=selection_entries,
            error=None,
            battle=None,
            badge=None,
            previous_game=previous_game,
            next_game=next_game,
        )

    current_battle = None
    player_active = None
    npc_active = None
    if state["phase"] in {"battle", "between_battles", "victory", "defeat"}:
        current_battle = state["npc_battles"][state["current_battle_index"]] if state["current_battle_index"] < len(state["npc_battles"]) else None
        player_active = get_first_available_pokemon(state.get("player_team", []))
        npc_active = get_first_available_pokemon(current_battle["team"]) if current_battle else None

    return render_template(
        "torre_lotta.html",
        user=user,
        phase=state["phase"],
        box_entries=selection_entries,
        error=state.get("error"),
        battle=current_battle,
        current_battle_number=state.get("current_battle_index", 0) + 1,
        player_team=state.get("player_team", []),
        player_active=player_active,
        npc_active=npc_active,
        battle_log=state.get("battle_log", []),
        wins=state.get("wins", 0),
        total_battles=len(state.get("npc_battles", [])),
        badge=state.get("earned_badge"),
        completion_message=state.get("completion_message"),
        previous_game=previous_game,
        next_game=next_game,
    )


@main_blueprint.route("/torre-lotta/start", methods=["POST"])
def start_torre_lotta():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.torre_lotta")))
    previous_game, next_game = get_minigame_navigation("/torre-lotta")

    box_entries = box_service.get_pokemon(user["id_utente"])
    if len(box_entries) < 6:
        clear_tower_state()
        return render_template(
            "torre_lotta.html",
            user=user,
            phase="team_select",
            box_entries=[
                {"id": item["id_pokemon_api"], "name": item["nome_pokemon"], "sprite": get_sprite_url(item["id_pokemon_api"])}
                for item in box_entries
            ],
            error="Ti servono almeno 6 Pokemon nel box per entrare nella Torre Lotta.",
            battle=None,
            badge=None,
            previous_game=previous_game,
            next_game=next_game,
        )

    selected_ids = request.form.getlist("pokemon_ids")
    selected_ids = [int(item) for item in selected_ids if item.isdigit()]
    selected_ids = list(dict.fromkeys(selected_ids))
    allowed_ids = {item["id_pokemon_api"] for item in box_entries}

    if len(selected_ids) != 6 or not set(selected_ids).issubset(allowed_ids):
        clear_tower_state()
        return render_template(
            "torre_lotta.html",
            user=user,
            phase="team_select",
            box_entries=[
                {"id": item["id_pokemon_api"], "name": item["nome_pokemon"], "sprite": get_sprite_url(item["id_pokemon_api"])}
                for item in box_entries
            ],
            error="Devi selezionare esattamente 6 Pokemon dal tuo box.",
            battle=None,
            badge=None,
            previous_game=previous_game,
            next_game=next_game,
        )

    selected_map = {item["id_pokemon_api"]: item["nome_pokemon"] for item in box_entries}
    player_team = [build_battle_pokemon(pokemon_id, selected_map[pokemon_id], TOWER_PLAYER_LEVEL, side="player") for pokemon_id in selected_ids]
    npc_battles = build_random_npc_battles(3)
    if len(npc_battles) < 3:
        clear_tower_state()
        return render_template(
            "torre_lotta.html",
            user=user,
            phase="team_select",
            box_entries=[
                {"id": item["id_pokemon_api"], "name": item["nome_pokemon"], "sprite": get_sprite_url(item["id_pokemon_api"])}
                for item in box_entries
            ],
            error="Non ci sono abbastanza NPC nel database per avviare la Torre Lotta.",
            battle=None,
            badge=None,
            previous_game=previous_game,
            next_game=next_game,
        )

    state = {
        "phase": "battle",
        "player_team": player_team,
        "npc_battles": npc_battles,
        "current_battle_index": 0,
        "wins": 0,
        "battle_log": ["La sfida alla Torre Lotta ha inizio."],
        "earned_badge": None,
        "completion_message": None,
        "error": None,
    }
    set_tower_state(state)
    return redirect(url_for("main.torre_lotta"))


@main_blueprint.route("/torre-lotta/turn", methods=["POST"])
def torre_lotta_turn():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.torre_lotta")))

    state = get_tower_state()
    if not state or state.get("phase") != "battle":
        return redirect(url_for("main.torre_lotta"))

    current_battle = state["npc_battles"][state["current_battle_index"]]
    turn_log = simulate_tower_turn(state["player_team"], current_battle["team"])
    state["battle_log"] = turn_log

    if team_is_defeated(current_battle["team"]):
        state["wins"] += 1
        if state["wins"] >= len(state["npc_battles"]):
            badge_info = award_random_badge(user["id_utente"])
            state["phase"] = "victory"
            if badge_info and badge_info.get("filename"):
                state["earned_badge"] = {
                    "filename": badge_info["filename"],
                    "url": get_badge_url(badge_info["filename"]),
                }
                state["completion_message"] = "Hai vinto."
            elif badge_info and badge_info.get("already_complete"):
                state["completion_message"] = "Hai vinto."
            else:
                state["completion_message"] = "Hai vinto."
        else:
            state["phase"] = "between_battles"
            state["completion_message"] = "Hai vinto."
    elif team_is_defeated(state["player_team"]):
        state["phase"] = "defeat"
        state["completion_message"] = "Hai perso."

    set_tower_state(state)
    return redirect(url_for("main.torre_lotta"))


@main_blueprint.route("/torre-lotta/continue", methods=["POST"])
def torre_lotta_continue():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.torre_lotta")))

    state = get_tower_state()
    if not state:
        return redirect(url_for("main.torre_lotta"))

    if state.get("phase") == "between_battles":
        state["current_battle_index"] += 1
        state["phase"] = "battle"
        state["completion_message"] = None
        reset_battle_team(state["player_team"])
        state["battle_log"] = ["La nuova sfida ha inizio."]
        set_tower_state(state)
    elif state.get("phase") in {"victory", "defeat"}:
        clear_tower_state()

    return redirect(url_for("main.torre_lotta"))


@main_blueprint.route("/zona-safari")
def zona_safari():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=request.path))
    previous_game, next_game = get_minigame_navigation("/zona-safari")

    state = get_safari_state()
    if not state or request.args.get("new") == "1":
        state = create_safari_game()
        if not state["encounters"]:
            return render_template(
                "zona_safari.html",
                user=user,
                game_active=False,
                game_finished=True,
                error="Non ci sono abbastanza sprite disponibili per avviare la Zona Safari.",
                balls=[],
                encounter=None,
                result=None,
                history=[],
                progress_label="0 / 0",
                saved_total=0,
                previous_game=previous_game,
                next_game=next_game,
            )
        set_safari_state(state)

    encounter = get_safari_current_encounter(state)
    total_encounters = len(state["encounters"])
    progress_label = f"{min(state['current_index'] + 1, total_encounters)} / {total_encounters}" if total_encounters else "0 / 0"

    return render_template(
        "zona_safari.html",
        user=user,
        game_active=state["phase"] != "finished",
        game_finished=state["phase"] == "finished",
        is_last_encounter=state["current_index"] >= max(total_encounters - 1, 0),
        balls=get_safari_ball_view(state),
        encounter=encounter,
        result=state.get("result"),
        history=state.get("history", []),
        progress_label=progress_label,
        saved_total=len(state.get("saved_ids", [])),
        final_message=state.get("final_message"),
        error=None,
        previous_game=previous_game,
        next_game=next_game,
    )


@main_blueprint.route("/zona-safari/start", methods=["POST"])
def start_zona_safari():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.zona_safari")))

    state = create_safari_game()
    set_safari_state(state)
    return redirect(url_for("main.zona_safari"))


@main_blueprint.route("/zona-safari/throw", methods=["POST"])
def zona_safari_throw():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.zona_safari")))

    state = get_safari_state()
    if not state:
        return redirect(url_for("main.zona_safari", new=1))

    if state.get("phase") != "encounter":
        return redirect(url_for("main.zona_safari"))

    ball_slug = request.form.get("ball", "").strip()
    if ball_slug not in SAFARI_BALLS or state["balls"].get(ball_slug, 0) <= 0:
        return redirect(url_for("main.zona_safari"))

    encounter = get_safari_current_encounter(state)
    if not encounter:
        finish_safari_game(state, "La partita e terminata.")
        return redirect(url_for("main.zona_safari"))

    state["balls"][ball_slug] -= 1
    success = random.randint(1, 100) <= SAFARI_BALLS[ball_slug]["chance"]

    result = {
        "ball_label": SAFARI_BALLS[ball_slug]["label"],
        "success": success,
        "pokemon_id": encounter["id"],
        "pokemon_name": encounter["name"],
        "can_save": False,
        "already_owned": False,
        "saved": False,
        "message": "",
    }

    if success:
        existing = box_service.has_pokemon(user["id_utente"], encounter["id"])
        if existing is None:
            result["message"] = "Pokemon catturato, ma il box non e disponibile al momento."
        elif existing:
            result["already_owned"] = True
            result["message"] = "Pokemon catturato, ma e gia presente nel tuo box."
        else:
            result["can_save"] = True
            result["message"] = "Pokemon catturato. Vuoi aggiungerlo al box?"
    else:
        result["message"] = f"{encounter['name']} e scappato via."

    state["phase"] = "result"
    state["result"] = result
    state["history"].append(
        {
            "pokemon_name": encounter["name"],
            "pokemon_id": encounter["id"],
            "ball_label": SAFARI_BALLS[ball_slug]["label"],
            "success": success,
        }
    )
    set_safari_state(state)
    return redirect(url_for("main.zona_safari"))


@main_blueprint.route("/zona-safari/save", methods=["POST"])
def zona_safari_save():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.zona_safari")))

    state = get_safari_state()
    if not state or state.get("phase") != "result" or not state.get("result"):
        return redirect(url_for("main.zona_safari"))

    result = state["result"]
    if not result.get("success") or not result.get("can_save") or result.get("saved"):
        return redirect(url_for("main.zona_safari"))

    added = box_service.add_pokemon(user["id_utente"], result["pokemon_id"], result["pokemon_name"])
    if added:
        result["saved"] = True
        result["can_save"] = False
        result["message"] = "Pokemon aggiunto al box con successo."
        state["saved_ids"].append(result["pokemon_id"])
    else:
        result["message"] = "Salvataggio nel box non riuscito."

    state["result"] = result
    set_safari_state(state)
    return redirect(url_for("main.zona_safari"))


@main_blueprint.route("/zona-safari/next", methods=["POST"])
def zona_safari_next():
    user = get_logged_user()
    if not user:
        return redirect(url_for("main.login", next=url_for("main.zona_safari")))

    state = get_safari_state()
    if not state:
        return redirect(url_for("main.zona_safari", new=1))

    if state.get("phase") == "finished":
        return redirect(url_for("main.zona_safari"))

    state["current_index"] += 1
    state["result"] = None

    if state["current_index"] >= len(state.get("encounters", [])):
        finish_safari_game(state, "Partita conclusa. Hai visto tutti i Pokemon della Zona Safari.")
    else:
        state["phase"] = "encounter"
        set_safari_state(state)

    return redirect(url_for("main.zona_safari"))


@main_blueprint.route("/")
def home():
    query = request.args.get("pokemon", "").strip()
    error_message = None

    if query:
        search_result = resolve_search(query)
        if search_result["status"] == "direct":
            return redirect(url_for("main.pokedex", pokemon=search_result["pokemon_id"]) + "#pokedex-view")
        if search_result["status"] == "choice":
            return redirect(url_for("main.choose_form", pokemon=query))
        if search_result["status"] == "error":
            error_message = search_result["message"]

    return render_template(
        "home.html",
        query=query,
        error=error_message,
        generations=GENERATION_CARDS,
        games=GAME_CARDS,
    )


@main_blueprint.route("/pokedex")
def pokedex():
    raw_query = request.args.get("pokemon", "").strip()
    error_message = None
    pokemon = None
    previous_id = None
    next_id = None
    query = raw_query or "1"

    if raw_query:
        search_result = resolve_search(raw_query)
        if search_result["status"] == "choice":
            return redirect(url_for("main.choose_form", pokemon=raw_query))
        if search_result["status"] == "error":
            return render_template(
                "pokedex.html",
                query=raw_query,
                error=search_result["message"],
                pokemon=None,
                previous_id=None,
                next_id=None,
            )

        resolved_id = str(search_result["pokemon_id"])
        if normalize_search_query(raw_query) != resolved_id:
            return redirect(url_for("main.pokedex", pokemon=resolved_id) + "#pokedex-view")
        query = resolved_id

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


@main_blueprint.route("/choose-form")
def choose_form():
    query = request.args.get("pokemon", "").strip()
    if not query:
        return redirect(url_for("main.home"))

    search_result = resolve_search(query)
    if search_result["status"] == "direct":
        return redirect(url_for("main.pokedex", pokemon=search_result["pokemon_id"]) + "#pokedex-view")
    if search_result["status"] == "error":
        return render_template(
            "form-choice.html",
            query=query,
            error=search_result["message"],
            choices=[],
            species_name=query.title(),
        )

    return render_template(
        "form-choice.html",
        query=query,
        error=None,
        choices=search_result.get("choices", []),
        species_name=search_result.get("species", query).replace("-", " ").title(),
    )


def render_generation_page(generation_name, start_id, end_id, page_name, pokemon_ids=None, range_label=None, description=None):
    query = request.args.get("pokemon", "").strip()
    error_message = None
    generation_title = get_generation_display_name(generation_name)
    previous_card, next_card = get_generation_navigation(page_name)

    if query:
        search_result = resolve_search(query)
        if search_result["status"] == "direct":
            return redirect(url_for("main.pokedex", pokemon=search_result["pokemon_id"]) + "#pokedex-view")
        if search_result["status"] == "choice":
            return redirect(url_for("main.choose_form", pokemon=query))
        if search_result["status"] == "error":
            error_message = search_result["message"]

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
        generation_name=generation_title,
        generation_range=range_label or f"Tutti i Pokemon da {start_id} a {end_id}.",
        generation_description=description or f"Cerca un Pokemon di {generation_name} e scorri la griglia completa degli sprite della generazione.",
        previous_card=previous_card,
        next_card=next_card,
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
