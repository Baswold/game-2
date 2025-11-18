"""
Crafting module - Manages item crafting and recipes.
"""

from typing import Dict, List, Optional
from items import get_item, ItemType


class Recipe:
    """
    Represents a crafting recipe.
    """

    def __init__(self, recipe_id: str, name: str, description: str,
                 materials: Dict[str, int], result_item_id: str,
                 level_requirement: int = 1):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
        self.materials = materials  # item_id -> quantity
        self.result_item_id = result_item_id
        self.level_requirement = level_requirement
        self.discovered = False

    def can_craft(self, character, inventory) -> tuple:
        """
        Check if recipe can be crafted.
        Returns (can_craft: bool, reason: str).
        """
        if character.level < self.level_requirement:
            return False, f"Requires level {self.level_requirement}"

        # Check materials
        for item_id, required in self.materials.items():
            if not inventory.has_item(item_id, required):
                item = get_item(item_id)
                item_name = item.name if item else item_id
                have = inventory.get_item_count(item_id)
                return False, f"Need {required}x {item_name} (have {have})"

        return True, ""

    def craft(self, inventory) -> bool:
        """
        Craft the item, consuming materials.
        Returns True if successful.
        """
        # Remove materials
        for item_id, quantity in self.materials.items():
            if not inventory.remove_item(item_id, quantity):
                return False

        # Add result
        if not inventory.add_item(self.result_item_id, 1):
            # Failed to add (inventory full) - restore materials
            for item_id, quantity in self.materials.items():
                inventory.add_item(item_id, quantity)
            return False

        return True

    def get_materials_display(self) -> str:
        """Get formatted list of required materials."""
        materials = []
        for item_id, quantity in self.materials.items():
            item = get_item(item_id)
            if item:
                materials.append(f"{quantity}x {item.name}")
            else:
                materials.append(f"{quantity}x {item_id}")
        return ", ".join(materials)

    def get_result_display(self) -> str:
        """Get formatted result item name."""
        item = get_item(self.result_item_id)
        return item.name if item else self.result_item_id

    def display(self) -> str:
        """Get formatted recipe display."""
        output = []
        output.append(f"\n--- {self.name} ---")
        output.append(f"{self.description}")
        output.append(f"Materials: {self.get_materials_display()}")
        output.append(f"Result: {self.get_result_display()}")
        output.append(f"Required Level: {self.level_requirement}")
        return '\n'.join(output)


class CraftingSystem:
    """
    Manages crafting recipes and operations.
    """

    def __init__(self):
        self.recipes: Dict[str, Recipe] = {}
        self.discovered_recipes: set = set()

    def register_recipe(self, recipe: Recipe):
        """Register a recipe."""
        self.recipes[recipe.recipe_id] = recipe

    def discover_recipe(self, recipe_id: str) -> bool:
        """
        Discover a recipe.
        Returns True if newly discovered.
        """
        if recipe_id not in self.recipes:
            return False

        if recipe_id in self.discovered_recipes:
            return False

        self.discovered_recipes.add(recipe_id)
        self.recipes[recipe_id].discovered = True
        return True

    def get_recipe(self, recipe_id: str) -> Optional[Recipe]:
        """Get a recipe by ID."""
        return self.recipes.get(recipe_id)

    def get_discovered_recipes(self) -> List[Recipe]:
        """Get all discovered recipes."""
        return [r for r in self.recipes.values() if r.recipe_id in self.discovered_recipes]

    def get_craftable_recipes(self, character, inventory) -> List[Recipe]:
        """Get all recipes that can currently be crafted."""
        craftable = []
        for recipe in self.get_discovered_recipes():
            can_craft, _ = recipe.can_craft(character, inventory)
            if can_craft:
                craftable.append(recipe)
        return craftable

    def display_recipes(self, character, inventory) -> str:
        """Display all discovered recipes."""
        discovered = self.get_discovered_recipes()

        if not discovered:
            return "\nNo recipes discovered yet.\n"

        output = []
        output.append("\n=== CRAFTING RECIPES ===\n")

        for recipe in discovered:
            can_craft, reason = recipe.can_craft(character, inventory)
            status = "✓" if can_craft else "✗"

            output.append(f"{status} {recipe.name}")
            output.append(f"   Materials: {recipe.get_materials_display()}")
            output.append(f"   Result: {recipe.get_result_display()}")

            if not can_craft:
                output.append(f"   Cannot craft: {reason}")

        return '\n'.join(output)

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        return {
            'discovered_recipes': list(self.discovered_recipes)
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.discovered_recipes = set(data.get('discovered_recipes', []))
        for recipe_id in self.discovered_recipes:
            if recipe_id in self.recipes:
                self.recipes[recipe_id].discovered = True


# =============================================================================
# RECIPE DEFINITIONS
# =============================================================================

def create_crafting_system() -> CraftingSystem:
    """Create and populate the crafting system."""
    system = CraftingSystem()

    # === WEAPON RECIPES ===

    system.register_recipe(Recipe(
        "craft_iron_sword", "Iron Sword",
        "Forge a basic iron sword.",
        materials={'iron_ore': 3, 'wood_plank': 1},
        result_item_id='iron_sword',
        level_requirement=2
    ))

    system.register_recipe(Recipe(
        "craft_steel_sword", "Steel Sword",
        "Forge an improved steel sword.",
        materials={'steel_ingot': 2, 'leather_scrap': 1},
        result_item_id='steel_sword',
        level_requirement=5
    ))

    system.register_recipe(Recipe(
        "craft_silver_rapier", "Silver Rapier",
        "Craft an elegant silver rapier.",
        materials={'silver_ore': 3, 'steel_ingot': 2, 'leather_scrap': 2},
        result_item_id='silver_rapier',
        level_requirement=8
    ))

    system.register_recipe(Recipe(
        "craft_dragon_slayer", "Dragon Slayer",
        "Forge a legendary dragon-slaying sword.",
        materials={'dragon_scale': 5, 'steel_ingot': 5, 'enchanted_crystal': 3},
        result_item_id='dragon_slayer',
        level_requirement=12
    ))

    # === ARMOR RECIPES ===

    system.register_recipe(Recipe(
        "craft_leather_armor", "Leather Armor",
        "Craft light leather armor.",
        materials={'leather_scrap': 5},
        result_item_id='leather_armor',
        level_requirement=2
    ))

    system.register_recipe(Recipe(
        "craft_chain_mail", "Chain Mail",
        "Forge chain mail armor.",
        materials={'iron_ore': 5, 'steel_ingot': 2},
        result_item_id='chain_mail',
        level_requirement=5
    ))

    system.register_recipe(Recipe(
        "craft_plate_armor", "Plate Armor",
        "Forge heavy plate armor.",
        materials={'steel_ingot': 8, 'iron_ore': 5},
        result_item_id='plate_armor',
        level_requirement=8
    ))

    system.register_recipe(Recipe(
        "craft_dragon_armor", "Dragon Scale Armor",
        "Craft legendary dragon scale armor.",
        materials={'dragon_scale': 10, 'steel_ingot': 5, 'leather_scrap': 5},
        result_item_id='dragon_armor',
        level_requirement=12
    ))

    # === ACCESSORY RECIPES ===

    system.register_recipe(Recipe(
        "craft_bronze_ring", "Bronze Ring",
        "Craft a simple bronze ring.",
        materials={'iron_ore': 2},
        result_item_id='bronze_ring',
        level_requirement=1
    ))

    system.register_recipe(Recipe(
        "craft_silver_amulet", "Silver Amulet",
        "Craft a silver amulet.",
        materials={'silver_ore': 3, 'enchanted_crystal': 1},
        result_item_id='silver_amulet',
        level_requirement=4
    ))

    system.register_recipe(Recipe(
        "craft_ring_strength", "Ring of Strength",
        "Craft a ring that enhances strength.",
        materials={'silver_ore': 2, 'enchanted_crystal': 2, 'iron_ore': 3},
        result_item_id='ring_strength',
        level_requirement=6
    ))

    system.register_recipe(Recipe(
        "craft_ring_haste", "Ring of Haste",
        "Craft a ring that increases agility.",
        materials={'silver_ore': 2, 'enchanted_crystal': 2},
        result_item_id='ring_haste',
        level_requirement=7
    ))

    system.register_recipe(Recipe(
        "craft_amulet_protection", "Amulet of Protection",
        "Craft a protective amulet.",
        materials={'silver_ore': 3, 'enchanted_crystal': 3, 'dragon_scale': 1},
        result_item_id='amulet_protection',
        level_requirement=6
    ))

    system.register_recipe(Recipe(
        "craft_crown_wisdom", "Crown of Wisdom",
        "Craft a crown that enhances intelligence.",
        materials={'silver_ore': 5, 'enchanted_crystal': 5, 'star_fragment': 1},
        result_item_id='crown_wisdom',
        level_requirement=10
    ))

    # === CONSUMABLE RECIPES ===

    system.register_recipe(Recipe(
        "craft_health_potion_medium", "Medium Health Potion",
        "Brew a medium healing potion.",
        materials={'health_potion_small': 3},
        result_item_id='health_potion_medium',
        level_requirement=3
    ))

    system.register_recipe(Recipe(
        "craft_health_potion_large", "Large Health Potion",
        "Brew a large healing potion.",
        materials={'health_potion_medium': 2, 'rare_herb': 1},
        result_item_id='health_potion_large',
        level_requirement=5
    ))

    system.register_recipe(Recipe(
        "craft_health_potion_supreme", "Supreme Health Potion",
        "Brew a supreme healing potion.",
        materials={'health_potion_large': 2, 'enchanted_crystal': 1},
        result_item_id='health_potion_supreme',
        level_requirement=8
    ))

    system.register_recipe(Recipe(
        "craft_elixir_vitality", "Elixir of Vitality",
        "Brew an elixir that permanently increases max HP.",
        materials={'rare_herb': 3, 'enchanted_crystal': 2, 'dragon_scale': 1},
        result_item_id='elixir_vitality',
        level_requirement=10
    ))

    # === MATERIAL PROCESSING ===

    system.register_recipe(Recipe(
        "smelt_steel", "Steel Ingot",
        "Smelt iron ore into steel.",
        materials={'iron_ore': 3},
        result_item_id='steel_ingot',
        level_requirement=3
    ))

    # Discover basic recipes by default
    system.discover_recipe('craft_iron_sword')
    system.discover_recipe('craft_leather_armor')
    system.discover_recipe('craft_bronze_ring')
    system.discover_recipe('craft_health_potion_medium')
    system.discover_recipe('smelt_steel')

    return system
