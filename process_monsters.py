import json

def load_json_file(filepath):
    """Loads a JSON file and returns its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return None

def process_evolutions(monster):
    """Processes the evolutions for a monster based on a whitelist."""
    if "evolutions" not in monster or not monster["evolutions"]:
        return None

    new_evolutions = set()
    for evolution in monster["evolutions"]:
        evo_type = evolution.get("type", "")
        if "HAPPINESS" in evo_type:
            new_evolutions.add("Happiness")
        elif "ITEM" in evo_type and "item_name" in evolution:
            new_evolutions.add(evolution["item_name"])
    
    return sorted(list(new_evolutions)) if new_evolutions else None

def process_locations(monster):
    """Processes the locations for a monster, filtering and simplifying types."""
    if "locations" not in monster or not monster["locations"]:
        return None

    location_types = set()
    for location in monster["locations"]:
        loc_type = location.get("type")
        if not loc_type or loc_type == "Grass":
            continue
        
        if "rod" in loc_type.lower():
            location_types.add("Rod")
        else:
            location_types.add(loc_type)
            
    return sorted(list(location_types)) if location_types else None

def check_recoil_moves(monster, moves_with_recoil):
    """Checks if any of the last 4 learnable moves by level 30 are recoil moves."""
    if "moves" not in monster or not monster["moves"]:
        return False

    level_moves_at_30 = [
        move for move in monster["moves"]
        if move.get("type") == "level" and move.get("level", 999) <= 30
    ]
    
    level_moves_at_30.sort(key=lambda m: m.get("level", 999))
    
    last_four_moves = level_moves_at_30[-4:]
    
    monster_types = monster.get("types", [])
    for move in last_four_moves:
        move_name = move.get("name")
        if move_name in moves_with_recoil:
            return True
        if move_name == "Curse" and "GHOST" in monster_types:
            return True
            
    return False

def main():
    """Main function to process monster data."""
    # --- Configuration ---
    KEYS_TO_KEEP = ["id", "name", "catch_rate", "weight", "speed", "has_recoil_at_level_30", "types", "evolutions", "locations"]
    MOVES_WITH_RECOIL = {
        "Double-Edge", "Brave Bird", "Take Down", "Flare Blitz", "Wood Hammer", 
        "Wild Charge", "Head Smash", "Submission", "Explosion", "Self-Destruct", 
        "Final Gambit", "Healing Wish", "Memento", "Perish Song"
    }

    # --- Data Loading ---
    monsters_data = load_json_file('monsters.json')
    catch_rates_data = load_json_file('catchRates.json')

    if monsters_data is None or catch_rates_data is None:
        print("Aborting due to file loading errors.")
        return

    catch_rate_map = {item['id']: item['rate'] for item in catch_rates_data}

    # --- Processing ---
    processed_data = []
    for monster in monsters_data:
        # Create a new dictionary to hold the processed data for this monster
        processed_monster = {"id": monster.get("id"), "name": monster.get("name")}

        # Add data from various sources
        processed_monster["catch_rate"] = catch_rate_map.get(monster.get("id"))
        processed_monster["weight"] = monster.get("weight")
        
        if monster.get("stats"):
            processed_monster["speed"] = monster["stats"].get("speed")

        processed_monster["types"] = monster.get("types")

        # Process complex fields using helper functions
        evolutions = process_evolutions(monster)
        if evolutions:
            processed_monster["evolutions"] = evolutions

        locations = process_locations(monster)
        if locations:
            processed_monster["locations"] = locations
        
        processed_monster["has_recoil_at_level_30"] = check_recoil_moves(monster, MOVES_WITH_RECOIL)

        # Create the final ordered monster object based on KEYS_TO_KEEP
        final_monster = {key: processed_monster[key] for key in KEYS_TO_KEEP if key in processed_monster and processed_monster[key] is not None}
        processed_data.append(final_monster)

    # --- Save Output ---
    with open('monsters_cleaned.json', 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=4)

    print("Processing complete. Cleaned data saved to monsters_cleaned.json")

if __name__ == "__main__":
    main()
