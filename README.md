# MyDex

MyDex e una web app realizzata con Flask che unisce:

- Pokedex con ricerca tramite [PokeAPI](https://pokeapi.co/)
- pagine dedicate alle generazioni e alle forme speciali
- autenticazione utenti con MySQL
- box personale dei Pokemon catturati
- pagina medaglie
- minigiochi `Zona Safari` e `Torre Lotta`

## Funzionalita principali

- ricerca Pokemon per nome, ID o forma
- pagina Pokedex con statistiche, abilita, tipi e descrizione
- navigazione tra regioni e forme speciali
- registrazione e login utenti
- box personale collegato al database
- assegnazione medaglie dopo le vittorie in Torre Lotta
- minigioco `Zona Safari` con cattura progressiva dei Pokemon
- minigioco `Torre Lotta` con squadre utente e NPC

## Tecnologie usate

- Python
- Flask
- MySQL
- HTML / CSS
- PokeAPI

## Struttura del progetto

```text
WebApp/
|- app.py
|- routes.py
|- requirements.txt
|- .env.example
|- database/
|  |- db_manager.py
|  |- npc_seed.sql
|- services/
|  |- user_service.py
|  |- box_service.py
|  |- secutity_manager.py
|- TEMPLATES/
|- STATIC/
|- sprites/
```

## Installazione

1. Clona il repository.
2. Crea e attiva un ambiente virtuale.
3. Installa le dipendenze:

```bash
py -m pip install -r requirements.txt
```

4. Crea un file `.env` partendo da `.env.example`.
5. Configura MySQL e crea il database `pokedex`.
6. Avvia l'app:

```bash
py app.py
```

L'app sara disponibile su [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Configurazione database

Le tabelle principali usate dall'app sono:

- `utenti`
- `box`
- `npc`
- `npc_team`
- `medaglia`

Per popolare gli NPC della Torre Lotta puoi eseguire:

```sql
SOURCE database/npc_seed.sql;
```

## Note per GitHub

- Il file `.env` non va pubblicato.
- Anche `database.db` e le cartelle `__pycache__` non vanno versionati.
- Se questi file erano gia tracciati da Git, vanno rimossi dall'indice con `git rm --cached`.

## Possibili sviluppi futuri

- bilanciamento avanzato della Torre Lotta
- nuove medaglie o ricompense
- miglioramento IA degli NPC
- deploy online del progetto
