# PokeMMO Dex Data Manipulation

This project processes pokedex data for the game PokeMMO to create a cleaned and simplified version of monster data (exported from the client itself).
This data is used by https://github.com/F-l-a/PokeMMO-BallSuggestionSprites

## Logic Explanation

The script `process_monsters.py` performs the following steps:

1.  **Loads Data**: It loads `monsters.json` which contains detailed monster information, and `catchRates.json` which contains the catch rates for each monster.

2.  **Processes Each Monster**: The script iterates through each monster in `monsters.json` and creates a new, simplified record with only the following keys: `id`, `name`, `catch_rate`, `weight`, `speed`, `has_recoil_at_level_30`, `types`, `evolutions`, and `locations`.

3.  **Simplifies Evolutions**: The `evolutions` field is processed to simplify the data. It only keeps track of evolutions that occur via "Happiness" or by using an item, storing the specific item's name.

4.  **Simplifies Locations**: The `locations` where a monster can be found are simplified. "Grass" encounters are ignored, and all encounters via fishing rods are grouped under a single "Rod" type.

5.  **Checks for Recoil Moves**: A special check (`has_recoil_at_level_30`) is performed. This flag is set to `true` if the monster learns a move that causes recoil damage (like Take Down or Double-Edge) within its last four level-up moves up to level 30. It also includes a special case for the move "Curse" if the monster is a Ghost-type.

6.  **Outputs Cleaned Data**: The final processed list of monsters is saved to `monsters_cleaned.json`.

## Data Sources

-   The `catchRates.json` file is sourced from the PokeMMO-Tools/pokemmo-hub repository. Credit and thanks to them for providing this data. You can find the original file here: [https://github.com/PokeMMO-Tools/pokemmo-hub/blob/main/src/data/catchRates.json](https://github.com/PokeMMO-Tools/pokemmo-hub/blob/main/src/data/catchRates.json)
