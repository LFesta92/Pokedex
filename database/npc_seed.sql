CREATE TABLE IF NOT EXISTS npc (
    id_npc INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS npc_team (
    id_team INT AUTO_INCREMENT PRIMARY KEY,
    id_npc INT NOT NULL,
    slot INT NOT NULL,
    id_pokemon_api INT NOT NULL,
    nome_pokemon VARCHAR(100) NOT NULL,
    livello INT NOT NULL,
    UNIQUE KEY uk_npc_slot (id_npc, slot),
    CONSTRAINT fk_npc_team_npc
        FOREIGN KEY (id_npc) REFERENCES npc(id_npc)
        ON DELETE CASCADE
);

INSERT INTO npc (username) VALUES
    ('npc_1'),
    ('npc_2'),
    ('npc_3'),
    ('npc_4'),
    ('npc_5'),
    ('npc_6'),
    ('npc_7'),
    ('npc_8'),
    ('npc_9'),
    ('npc_10'),
    ('npc_11'),
    ('npc_12'),
    ('npc_13'),
    ('npc_14'),
    ('npc_15')
ON DUPLICATE KEY UPDATE username = VALUES(username);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 59, 'Arcanine', 58 FROM npc WHERE username = 'npc_1'
UNION ALL SELECT id_npc, 2, 130, 'Gyarados', 59 FROM npc WHERE username = 'npc_1'
UNION ALL SELECT id_npc, 3, 214, 'Heracross', 57 FROM npc WHERE username = 'npc_1'
UNION ALL SELECT id_npc, 4, 553, 'Krookodile', 60 FROM npc WHERE username = 'npc_1'
UNION ALL SELECT id_npc, 5, 849, 'Toxtricity', 58 FROM npc WHERE username = 'npc_1'
UNION ALL SELECT id_npc, 6, 149, 'Dragonite', 62 FROM npc WHERE username = 'npc_1'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 448, 'Lucario', 60 FROM npc WHERE username = 'npc_2'
UNION ALL SELECT id_npc, 2, 445, 'Garchomp', 64 FROM npc WHERE username = 'npc_2'
UNION ALL SELECT id_npc, 3, 461, 'Weavile', 59 FROM npc WHERE username = 'npc_2'
UNION ALL SELECT id_npc, 4, 637, 'Volcarona', 63 FROM npc WHERE username = 'npc_2'
UNION ALL SELECT id_npc, 5, 376, 'Metagross', 62 FROM npc WHERE username = 'npc_2'
UNION ALL SELECT id_npc, 6, 248, 'Tyranitar', 64 FROM npc WHERE username = 'npc_2'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 212, 'Scizor', 58 FROM npc WHERE username = 'npc_3'
UNION ALL SELECT id_npc, 2, 373, 'Salamence', 64 FROM npc WHERE username = 'npc_3'
UNION ALL SELECT id_npc, 3, 350, 'Milotic', 60 FROM npc WHERE username = 'npc_3'
UNION ALL SELECT id_npc, 4, 462, 'Magnezone', 59 FROM npc WHERE username = 'npc_3'
UNION ALL SELECT id_npc, 5, 609, 'Chandelure', 61 FROM npc WHERE username = 'npc_3'
UNION ALL SELECT id_npc, 6, 612, 'Haxorus', 63 FROM npc WHERE username = 'npc_3'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 257, 'Blaziken', 60 FROM npc WHERE username = 'npc_4'
UNION ALL SELECT id_npc, 2, 260, 'Swampert', 60 FROM npc WHERE username = 'npc_4'
UNION ALL SELECT id_npc, 3, 254, 'Sceptile', 60 FROM npc WHERE username = 'npc_4'
UNION ALL SELECT id_npc, 4, 475, 'Gallade', 61 FROM npc WHERE username = 'npc_4'
UNION ALL SELECT id_npc, 5, 306, 'Aggron', 58 FROM npc WHERE username = 'npc_4'
UNION ALL SELECT id_npc, 6, 330, 'Flygon', 59 FROM npc WHERE username = 'npc_4'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 473, 'Mamoswine', 61 FROM npc WHERE username = 'npc_5'
UNION ALL SELECT id_npc, 2, 472, 'Gliscor', 60 FROM npc WHERE username = 'npc_5'
UNION ALL SELECT id_npc, 3, 468, 'Togekiss', 60 FROM npc WHERE username = 'npc_5'
UNION ALL SELECT id_npc, 4, 530, 'Excadrill', 62 FROM npc WHERE username = 'npc_5'
UNION ALL SELECT id_npc, 5, 635, 'Hydreigon', 65 FROM npc WHERE username = 'npc_5'
UNION ALL SELECT id_npc, 6, 681, 'Aegislash', 63 FROM npc WHERE username = 'npc_5'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 706, 'Goodra', 62 FROM npc WHERE username = 'npc_6'
UNION ALL SELECT id_npc, 2, 663, 'Talonflame', 58 FROM npc WHERE username = 'npc_6'
UNION ALL SELECT id_npc, 3, 700, 'Sylveon', 59 FROM npc WHERE username = 'npc_6'
UNION ALL SELECT id_npc, 4, 715, 'Noivern', 60 FROM npc WHERE username = 'npc_6'
UNION ALL SELECT id_npc, 5, 701, 'Hawlucha', 58 FROM npc WHERE username = 'npc_6'
UNION ALL SELECT id_npc, 6, 681, 'Aegislash', 62 FROM npc WHERE username = 'npc_6'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 784, 'Kommo-o', 64 FROM npc WHERE username = 'npc_7'
UNION ALL SELECT id_npc, 2, 778, 'Mimikyu', 61 FROM npc WHERE username = 'npc_7'
UNION ALL SELECT id_npc, 3, 738, 'Vikavolt', 58 FROM npc WHERE username = 'npc_7'
UNION ALL SELECT id_npc, 4, 750, 'Mudsdale', 59 FROM npc WHERE username = 'npc_7'
UNION ALL SELECT id_npc, 5, 768, 'Golisopod', 61 FROM npc WHERE username = 'npc_7'
UNION ALL SELECT id_npc, 6, 763, 'Tsareena', 57 FROM npc WHERE username = 'npc_7'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 823, 'Corviknight', 61 FROM npc WHERE username = 'npc_8'
UNION ALL SELECT id_npc, 2, 858, 'Hatterene', 62 FROM npc WHERE username = 'npc_8'
UNION ALL SELECT id_npc, 3, 861, 'Grimmsnarl', 62 FROM npc WHERE username = 'npc_8'
UNION ALL SELECT id_npc, 4, 887, 'Dragapult', 66 FROM npc WHERE username = 'npc_8'
UNION ALL SELECT id_npc, 5, 847, 'Barraskewda', 59 FROM npc WHERE username = 'npc_8'
UNION ALL SELECT id_npc, 6, 839, 'Coalossal', 60 FROM npc WHERE username = 'npc_8'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 979, 'Annihilape', 66 FROM npc WHERE username = 'npc_9'
UNION ALL SELECT id_npc, 2, 937, 'Ceruledge', 64 FROM npc WHERE username = 'npc_9'
UNION ALL SELECT id_npc, 3, 936, 'Armarouge', 64 FROM npc WHERE username = 'npc_9'
UNION ALL SELECT id_npc, 4, 998, 'Baxcalibur', 67 FROM npc WHERE username = 'npc_9'
UNION ALL SELECT id_npc, 5, 964, 'Palafin', 65 FROM npc WHERE username = 'npc_9'
UNION ALL SELECT id_npc, 6, 983, 'Kingambit', 66 FROM npc WHERE username = 'npc_9'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 980, 'Clodsire', 60 FROM npc WHERE username = 'npc_10'
UNION ALL SELECT id_npc, 2, 959, 'Tinkaton', 62 FROM npc WHERE username = 'npc_10'
UNION ALL SELECT id_npc, 3, 920, 'Lokix', 58 FROM npc WHERE username = 'npc_10'
UNION ALL SELECT id_npc, 4, 970, 'Garganacl', 64 FROM npc WHERE username = 'npc_10'
UNION ALL SELECT id_npc, 5, 911, 'Skeledirge', 65 FROM npc WHERE username = 'npc_10'
UNION ALL SELECT id_npc, 6, 908, 'Meowscarada', 64 FROM npc WHERE username = 'npc_10'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 160, 'Feraligatr', 58 FROM npc WHERE username = 'npc_11'
UNION ALL SELECT id_npc, 2, 392, 'Infernape', 60 FROM npc WHERE username = 'npc_11'
UNION ALL SELECT id_npc, 3, 395, 'Empoleon', 60 FROM npc WHERE username = 'npc_11'
UNION ALL SELECT id_npc, 4, 497, 'Serperior', 61 FROM npc WHERE username = 'npc_11'
UNION ALL SELECT id_npc, 5, 503, 'Samurott', 61 FROM npc WHERE username = 'npc_11'
UNION ALL SELECT id_npc, 6, 652, 'Chesnaught', 60 FROM npc WHERE username = 'npc_11'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 34, 'Nidoking', 56 FROM npc WHERE username = 'npc_12'
UNION ALL SELECT id_npc, 2, 31, 'Nidoqueen', 56 FROM npc WHERE username = 'npc_12'
UNION ALL SELECT id_npc, 3, 65, 'Alakazam', 60 FROM npc WHERE username = 'npc_12'
UNION ALL SELECT id_npc, 4, 68, 'Machamp', 59 FROM npc WHERE username = 'npc_12'
UNION ALL SELECT id_npc, 5, 94, 'Gengar', 60 FROM npc WHERE username = 'npc_12'
UNION ALL SELECT id_npc, 6, 112, 'Rhydon', 57 FROM npc WHERE username = 'npc_12'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 407, 'Roserade', 58 FROM npc WHERE username = 'npc_13'
UNION ALL SELECT id_npc, 2, 466, 'Electivire', 60 FROM npc WHERE username = 'npc_13'
UNION ALL SELECT id_npc, 3, 467, 'Magmortar', 60 FROM npc WHERE username = 'npc_13'
UNION ALL SELECT id_npc, 4, 477, 'Dusknoir', 59 FROM npc WHERE username = 'npc_13'
UNION ALL SELECT id_npc, 5, 464, 'Rhyperior', 62 FROM npc WHERE username = 'npc_13'
UNION ALL SELECT id_npc, 6, 474, 'Porygon-Z', 60 FROM npc WHERE username = 'npc_13'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 131, 'Lapras', 57 FROM npc WHERE username = 'npc_14'
UNION ALL SELECT id_npc, 2, 143, 'Snorlax', 60 FROM npc WHERE username = 'npc_14'
UNION ALL SELECT id_npc, 3, 196, 'Espeon', 58 FROM npc WHERE username = 'npc_14'
UNION ALL SELECT id_npc, 4, 197, 'Umbreon', 58 FROM npc WHERE username = 'npc_14'
UNION ALL SELECT id_npc, 5, 181, 'Ampharos', 57 FROM npc WHERE username = 'npc_14'
UNION ALL SELECT id_npc, 6, 232, 'Donphan', 58 FROM npc WHERE username = 'npc_14'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);

INSERT INTO npc_team (id_npc, slot, id_pokemon_api, nome_pokemon, livello)
SELECT id_npc, 1, 282, 'Gardevoir', 60 FROM npc WHERE username = 'npc_15'
UNION ALL SELECT id_npc, 2, 286, 'Breloom', 58 FROM npc WHERE username = 'npc_15'
UNION ALL SELECT id_npc, 3, 310, 'Manectric', 57 FROM npc WHERE username = 'npc_15'
UNION ALL SELECT id_npc, 4, 334, 'Altaria', 58 FROM npc WHERE username = 'npc_15'
UNION ALL SELECT id_npc, 5, 359, 'Absol', 59 FROM npc WHERE username = 'npc_15'
UNION ALL SELECT id_npc, 6, 365, 'Walrein', 58 FROM npc WHERE username = 'npc_15'
ON DUPLICATE KEY UPDATE
    id_pokemon_api = VALUES(id_pokemon_api),
    nome_pokemon = VALUES(nome_pokemon),
    livello = VALUES(livello);
