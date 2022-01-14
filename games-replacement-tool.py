import os
import re

NEW_GAMES_DIR = 'new-games'

GAME_TYPES = r"(.gen|.bin|.md|.sg|.smd|.zip|.7z)$"

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

old_files = next(os.walk(CURRENT_PATH), (None, None, []))[2]
new_files = next(os.walk(f"{CURRENT_PATH}/{NEW_GAMES_DIR}"), (None, None, []))[2]

old_game_files = [file for file in old_files if re.search(GAME_TYPES, file) != None]
new_game_files = [file for file in new_files if re.search(GAME_TYPES, file) != None]

set_old_games = set(re.sub(GAME_TYPES, '', file) for file in old_game_files)
set_new_games = set(re.sub(GAME_TYPES, '', file) for file in new_game_files)

same_games = set_old_games.intersection(set_new_games)

print(f"[INFO] Total found {len(same_games)} same_games")

for game in same_games:
    print(f"[INFO] Moving {game}")

    # TODO Move files from NEW_GAMES_DIR to roms folder
    




