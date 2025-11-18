"""
Save System module - Handles game saving and loading.
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, List


class SaveGame:
    """
    Represents a saved game state.
    """

    def __init__(self, save_name: str):
        self.save_name = save_name
        self.timestamp = datetime.now()
        self.data = {}

    def save_to_file(self, save_dir: str = "saves") -> bool:
        """
        Save game data to file.
        Returns True if successful.
        """
        try:
            # Create save directory if it doesn't exist
            os.makedirs(save_dir, exist_ok=True)

            # Prepare save data
            save_data = {
                'save_name': self.save_name,
                'timestamp': self.timestamp.isoformat(),
                'data': self.data
            }

            # Write to file
            filename = os.path.join(save_dir, f"{self.save_name}.json")
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_from_file(save_name: str, save_dir: str = "saves") -> Optional['SaveGame']:
        """
        Load game data from file.
        Returns SaveGame object if successful, None otherwise.
        """
        try:
            filename = os.path.join(save_dir, f"{save_name}.json")

            if not os.path.exists(filename):
                return None

            with open(filename, 'r') as f:
                save_data = json.load(f)

            save_game = SaveGame(save_data['save_name'])
            save_game.timestamp = datetime.fromisoformat(save_data['timestamp'])
            save_game.data = save_data['data']

            return save_game

        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def get_all_saves(save_dir: str = "saves") -> List[Dict]:
        """
        Get list of all save files with metadata.
        Returns list of dicts with save info.
        """
        saves = []

        try:
            if not os.path.exists(save_dir):
                return saves

            for filename in os.listdir(save_dir):
                if filename.endswith('.json'):
                    save_name = filename[:-5]  # Remove .json extension

                    # Try to load metadata
                    filepath = os.path.join(save_dir, filename)
                    with open(filepath, 'r') as f:
                        save_data = json.load(f)

                    saves.append({
                        'save_name': save_name,
                        'timestamp': save_data.get('timestamp', 'Unknown'),
                        'character_name': save_data.get('data', {}).get('character', {}).get('name', 'Unknown'),
                        'level': save_data.get('data', {}).get('character', {}).get('level', 0)
                    })

        except Exception as e:
            print(f"Error listing saves: {e}")

        return saves

    @staticmethod
    def delete_save(save_name: str, save_dir: str = "saves") -> bool:
        """
        Delete a save file.
        Returns True if successful.
        """
        try:
            filename = os.path.join(save_dir, f"{save_name}.json")

            if os.path.exists(filename):
                os.remove(filename)
                return True

            return False

        except Exception as e:
            print(f"Error deleting save: {e}")
            return False


class GameState:
    """
    Manages the current game state for saving/loading.
    """

    def __init__(self):
        self.character = None
        self.inventory = None
        self.world = None
        self.quest_manager = None
        self.crafting_system = None

    def save_game(self, save_name: str) -> bool:
        """
        Save the current game state.
        Returns True if successful.
        """
        try:
            save_game = SaveGame(save_name)

            # Gather all game data
            save_game.data = {
                'character': self.character.to_dict() if self.character else None,
                'inventory': self.inventory.to_dict() if self.inventory else None,
                'world': self.world.to_dict() if self.world else None,
                'quests': self.quest_manager.to_dict() if self.quest_manager else None,
                'crafting': self.crafting_system.to_dict() if self.crafting_system else None
            }

            return save_game.save_to_file()

        except Exception as e:
            print(f"Error preparing save: {e}")
            return False

    def load_game(self, save_name: str) -> bool:
        """
        Load a saved game state.
        Returns True if successful.
        """
        try:
            save_game = SaveGame.load_from_file(save_name)

            if not save_game:
                return False

            data = save_game.data

            # Load character
            if 'character' in data and data['character']:
                from character import Character
                self.character = Character.from_dict(data['character'])

            # Load inventory
            if 'inventory' in data and data['inventory']:
                from inventory import Inventory
                self.inventory = Inventory.from_dict(data['inventory'])

            # Load world
            if 'world' in data and data['world']:
                from world import create_game_world
                self.world = create_game_world()
                self.world.from_dict(data['world'])

            # Load quest manager
            if 'quests' in data and data['quests']:
                from quest import create_all_quests
                self.quest_manager = create_all_quests()
                self.quest_manager.from_dict(data['quests'])

            # Load crafting system
            if 'crafting' in data and data['crafting']:
                from crafting import create_crafting_system
                self.crafting_system = create_crafting_system()
                self.crafting_system.from_dict(data['crafting'])

            # Restore equipped items
            if self.character and self.inventory:
                char_data = data['character']
                equipped = char_data.get('equipped', {})

                for slot, item_data in equipped.items():
                    if item_data:
                        from items import create_item
                        item = create_item(item_data['item_id'])
                        if item:
                            self.character.equip_item(item, slot)

            return True

        except Exception as e:
            print(f"Error loading save: {e}")
            return False

    def new_game(self, character_name: str):
        """Initialize a new game."""
        from character import Character
        from inventory import Inventory
        from world import create_game_world
        from quest import create_all_quests
        from crafting import create_crafting_system
        from items import create_item

        self.character = Character(character_name)
        self.inventory = Inventory()
        self.world = create_game_world()
        self.quest_manager = create_all_quests()
        self.crafting_system = create_crafting_system()

        # Give starting items
        self.inventory.add_item('health_potion_small', 3)
        self.inventory.add_item('rusty_sword', 1)

        # Equip starting weapon
        weapon = create_item('rusty_sword')
        if weapon:
            self.character.equip_item(weapon, 'weapon')
