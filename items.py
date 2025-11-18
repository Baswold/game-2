"""
Items module - Defines all items, equipment, and consumables in the game.
"""

from typing import Dict, Optional, Callable
from enum import Enum


class ItemType(Enum):
    """Types of items in the game."""
    CONSUMABLE = "consumable"
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    MATERIAL = "material"
    QUEST = "quest"


class ItemRarity(Enum):
    """Item rarity levels."""
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class Item:
    """Base class for all items."""

    def __init__(self, item_id: str, name: str, description: str,
                 item_type: ItemType, value: int = 0,
                 rarity: ItemRarity = ItemRarity.COMMON):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.item_type = item_type
        self.value = value  # Gold value
        self.rarity = rarity

    def to_dict(self) -> Dict:
        """Convert item to dictionary."""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'item_type': self.item_type.value,
            'value': self.value,
            'rarity': self.rarity.value
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.rarity.value})"


class Consumable(Item):
    """Consumable items that can be used."""

    def __init__(self, item_id: str, name: str, description: str,
                 value: int, effect_type: str, effect_amount: int,
                 rarity: ItemRarity = ItemRarity.COMMON):
        super().__init__(item_id, name, description, ItemType.CONSUMABLE, value, rarity)
        self.effect_type = effect_type  # 'heal', 'strength_boost', etc.
        self.effect_amount = effect_amount

    def use(self, character) -> str:
        """Use the consumable on a character. Returns message."""
        if self.effect_type == 'heal':
            healed = character.heal(self.effect_amount)
            return f"Healed {healed} HP!"
        elif self.effect_type == 'max_hp_boost':
            character.base_stats['max_hp'] += self.effect_amount
            character.base_stats['hp'] += self.effect_amount
            return f"Maximum HP increased by {self.effect_amount}!"
        elif self.effect_type == 'revive':
            if character.is_dead():
                character.revive(self.effect_amount / 100)
                return f"Revived with {self.effect_amount}% HP!"
            else:
                return "Character is not dead!"
        else:
            return "Used item."

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'effect_type': self.effect_type,
            'effect_amount': self.effect_amount
        })
        return data


class Equipment(Item):
    """Base class for equipment items."""

    def __init__(self, item_id: str, name: str, description: str,
                 item_type: ItemType, value: int, stats: Dict[str, int],
                 level_requirement: int = 1,
                 rarity: ItemRarity = ItemRarity.COMMON):
        super().__init__(item_id, name, description, item_type, value, rarity)
        self.stats = stats  # Dictionary of stat bonuses
        self.level_requirement = level_requirement

    def can_equip(self, character) -> bool:
        """Check if character can equip this item."""
        return character.level >= self.level_requirement

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'stats': self.stats.copy(),
            'level_requirement': self.level_requirement
        })
        return data

    def get_stats_description(self) -> str:
        """Get formatted description of stat bonuses."""
        if not self.stats:
            return "No bonuses"
        stat_lines = [f"+{value} {stat.replace('_', ' ').title()}" for stat, value in self.stats.items()]
        return ", ".join(stat_lines)


class Weapon(Equipment):
    """Weapon equipment."""

    def __init__(self, item_id: str, name: str, description: str,
                 value: int, damage: int, stats: Dict[str, int] = None,
                 level_requirement: int = 1,
                 rarity: ItemRarity = ItemRarity.COMMON):
        if stats is None:
            stats = {}
        super().__init__(item_id, name, description, ItemType.WEAPON,
                         value, stats, level_requirement, rarity)
        self.damage = damage

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = super().to_dict()
        data['damage'] = self.damage
        return data


class Armor(Equipment):
    """Armor equipment."""

    def __init__(self, item_id: str, name: str, description: str,
                 value: int, defense_bonus: int, stats: Dict[str, int] = None,
                 level_requirement: int = 1,
                 rarity: ItemRarity = ItemRarity.COMMON):
        if stats is None:
            stats = {}
        stats['defense'] = stats.get('defense', 0) + defense_bonus
        super().__init__(item_id, name, description, ItemType.ARMOR,
                         value, stats, level_requirement, rarity)
        self.defense_bonus = defense_bonus

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        data = super().to_dict()
        data['defense_bonus'] = self.defense_bonus
        return data


class Accessory(Equipment):
    """Accessory equipment."""

    def __init__(self, item_id: str, name: str, description: str,
                 value: int, stats: Dict[str, int],
                 level_requirement: int = 1,
                 rarity: ItemRarity = ItemRarity.COMMON):
        super().__init__(item_id, name, description, ItemType.ACCESSORY,
                         value, stats, level_requirement, rarity)


class Material(Item):
    """Crafting material."""

    def __init__(self, item_id: str, name: str, description: str, value: int,
                 rarity: ItemRarity = ItemRarity.COMMON):
        super().__init__(item_id, name, description, ItemType.MATERIAL, value, rarity)


class QuestItem(Item):
    """Quest-specific item."""

    def __init__(self, item_id: str, name: str, description: str, value: int = 0):
        super().__init__(item_id, name, description, ItemType.QUEST, value, ItemRarity.COMMON)


# =============================================================================
# ITEM DATABASE - All items in the game
# =============================================================================

ITEMS_DB = {}


def register_item(item: Item):
    """Register an item in the database."""
    ITEMS_DB[item.item_id] = item


# Consumables
register_item(Consumable(
    "health_potion_small", "Small Health Potion",
    "Restores 50 HP", 20, "heal", 50, ItemRarity.COMMON
))

register_item(Consumable(
    "health_potion_medium", "Medium Health Potion",
    "Restores 100 HP", 50, "heal", 100, ItemRarity.UNCOMMON
))

register_item(Consumable(
    "health_potion_large", "Large Health Potion",
    "Restores 200 HP", 100, "heal", 200, ItemRarity.RARE
))

register_item(Consumable(
    "health_potion_supreme", "Supreme Health Potion",
    "Fully restores HP", 250, "heal", 9999, ItemRarity.EPIC
))

register_item(Consumable(
    "elixir_vitality", "Elixir of Vitality",
    "Permanently increases max HP by 20", 200, "max_hp_boost", 20, ItemRarity.RARE
))

register_item(Consumable(
    "phoenix_down", "Phoenix Down",
    "Revives from defeat with 50% HP", 300, "revive", 50, ItemRarity.EPIC
))

# Weapons
register_item(Weapon(
    "rusty_sword", "Rusty Sword",
    "An old, worn sword. Better than nothing.", 10, 5,
    {'strength': 2}, 1, ItemRarity.COMMON
))

register_item(Weapon(
    "iron_sword", "Iron Sword",
    "A reliable iron blade.", 50, 12,
    {'strength': 5}, 3, ItemRarity.COMMON
))

register_item(Weapon(
    "steel_sword", "Steel Sword",
    "A well-crafted steel weapon.", 150, 20,
    {'strength': 10, 'agility': 3}, 5, ItemRarity.UNCOMMON
))

register_item(Weapon(
    "silver_rapier", "Silver Rapier",
    "An elegant and deadly blade.", 300, 28,
    {'strength': 12, 'agility': 8}, 8, ItemRarity.RARE
))

register_item(Weapon(
    "dragon_slayer", "Dragon Slayer",
    "A legendary sword forged from dragon scales.", 1000, 45,
    {'strength': 20, 'agility': 5, 'luck': 10}, 12, ItemRarity.EPIC
))

register_item(Weapon(
    "excalibur", "Excalibur",
    "The sword of legends, pulsing with ancient power.", 5000, 80,
    {'strength': 35, 'agility': 15, 'luck': 20, 'max_hp': 50}, 15, ItemRarity.LEGENDARY
))

register_item(Weapon(
    "staff_apprentice", "Apprentice Staff",
    "A simple wooden staff.", 40, 8,
    {'intelligence': 8}, 2, ItemRarity.COMMON
))

register_item(Weapon(
    "staff_mage", "Mage Staff",
    "A staff imbued with magical energy.", 200, 18,
    {'intelligence': 15, 'max_hp': 20}, 6, ItemRarity.UNCOMMON
))

# Armor
register_item(Armor(
    "cloth_armor", "Cloth Armor",
    "Basic cloth protection.", 20, 3,
    {'max_hp': 10}, 1, ItemRarity.COMMON
))

register_item(Armor(
    "leather_armor", "Leather Armor",
    "Light but effective protection.", 60, 8,
    {'max_hp': 20, 'agility': 2}, 3, ItemRarity.COMMON
))

register_item(Armor(
    "chain_mail", "Chain Mail",
    "Interlocking metal rings provide solid defense.", 180, 15,
    {'max_hp': 40, 'strength': 3}, 5, ItemRarity.UNCOMMON
))

register_item(Armor(
    "plate_armor", "Plate Armor",
    "Heavy plate armor offering excellent protection.", 400, 25,
    {'max_hp': 80, 'strength': 5, 'defense': 10}, 8, ItemRarity.RARE
))

register_item(Armor(
    "dragon_armor", "Dragon Scale Armor",
    "Armor crafted from dragon scales.", 1200, 40,
    {'max_hp': 150, 'strength': 10, 'defense': 20, 'agility': -5}, 12, ItemRarity.EPIC
))

register_item(Armor(
    "celestial_robe", "Celestial Robe",
    "A robe woven from starlight itself.", 2000, 20,
    {'max_hp': 100, 'intelligence': 25, 'agility': 10, 'luck': 10}, 10, ItemRarity.LEGENDARY
))

# Accessories
register_item(Accessory(
    "bronze_ring", "Bronze Ring",
    "A simple bronze ring.", 30,
    {'luck': 3}, 1, ItemRarity.COMMON
))

register_item(Accessory(
    "silver_amulet", "Silver Amulet",
    "An amulet that brings good fortune.", 100,
    {'luck': 8, 'max_hp': 15}, 4, ItemRarity.UNCOMMON
))

register_item(Accessory(
    "ring_strength", "Ring of Strength",
    "Grants the wearer enhanced physical power.", 200,
    {'strength': 10, 'max_hp': 20}, 6, ItemRarity.RARE
))

register_item(Accessory(
    "amulet_protection", "Amulet of Protection",
    "Magical protection against harm.", 250,
    {'defense': 15, 'max_hp': 30}, 6, ItemRarity.RARE
))

register_item(Accessory(
    "ring_haste", "Ring of Haste",
    "Increases the wearer's speed.", 220,
    {'agility': 15, 'luck': 5}, 7, ItemRarity.RARE
))

register_item(Accessory(
    "crown_wisdom", "Crown of Wisdom",
    "A crown that enhances mental acuity.", 800,
    {'intelligence': 20, 'max_hp': 40, 'luck': 10}, 10, ItemRarity.EPIC
))

register_item(Accessory(
    "pendant_phoenix", "Phoenix Pendant",
    "Contains the essence of a phoenix.", 1500,
    {'max_hp': 100, 'strength': 10, 'defense': 10, 'luck': 15}, 12, ItemRarity.LEGENDARY
))

# Materials
register_item(Material(
    "iron_ore", "Iron Ore",
    "Raw iron ready for smelting.", 15, ItemRarity.COMMON
))

register_item(Material(
    "leather_scrap", "Leather Scrap",
    "A piece of tanned leather.", 10, ItemRarity.COMMON
))

register_item(Material(
    "wood_plank", "Wood Plank",
    "A sturdy wooden plank.", 8, ItemRarity.COMMON
))

register_item(Material(
    "steel_ingot", "Steel Ingot",
    "Refined steel ready for crafting.", 40, ItemRarity.UNCOMMON
))

register_item(Material(
    "dragon_scale", "Dragon Scale",
    "A scale from a dragon's hide.", 200, ItemRarity.EPIC
))

register_item(Material(
    "star_fragment", "Star Fragment",
    "A piece of a fallen star.", 500, ItemRarity.LEGENDARY
))

register_item(Material(
    "enchanted_crystal", "Enchanted Crystal",
    "A crystal pulsing with magical energy.", 100, ItemRarity.RARE
))

register_item(Material(
    "silver_ore", "Silver Ore",
    "Precious silver ore.", 50, ItemRarity.UNCOMMON
))

# Quest Items
register_item(QuestItem(
    "mysterious_letter", "Mysterious Letter",
    "A sealed letter with no sender.", 0
))

register_item(QuestItem(
    "ancient_key", "Ancient Key",
    "An old key with strange markings.", 0
))

register_item(QuestItem(
    "goblin_chief_head", "Goblin Chief's Head",
    "Proof of defeating the goblin chief.", 0
))

register_item(QuestItem(
    "rare_herb", "Rare Healing Herb",
    "A herb with potent healing properties.", 0
))

register_item(QuestItem(
    "merchants_package", "Merchant's Package",
    "A sealed package for delivery.", 0
))


def get_item(item_id: str) -> Optional[Item]:
    """Get an item by its ID."""
    return ITEMS_DB.get(item_id)


def create_item(item_id: str) -> Optional[Item]:
    """Create a new instance of an item by ID."""
    template = get_item(item_id)
    if not template:
        return None

    # Create a copy of the item
    item_type = template.item_type

    if item_type == ItemType.CONSUMABLE:
        return Consumable(
            template.item_id, template.name, template.description,
            template.value, template.effect_type, template.effect_amount,
            template.rarity
        )
    elif item_type == ItemType.WEAPON:
        return Weapon(
            template.item_id, template.name, template.description,
            template.value, template.damage, template.stats.copy(),
            template.level_requirement, template.rarity
        )
    elif item_type == ItemType.ARMOR:
        return Armor(
            template.item_id, template.name, template.description,
            template.value, template.defense_bonus, template.stats.copy(),
            template.level_requirement, template.rarity
        )
    elif item_type == ItemType.ACCESSORY:
        return Accessory(
            template.item_id, template.name, template.description,
            template.value, template.stats.copy(),
            template.level_requirement, template.rarity
        )
    elif item_type == ItemType.MATERIAL:
        return Material(
            template.item_id, template.name, template.description,
            template.value, template.rarity
        )
    elif item_type == ItemType.QUEST:
        return QuestItem(
            template.item_id, template.name, template.description,
            template.value
        )

    return None


def get_items_by_type(item_type: ItemType) -> list:
    """Get all items of a specific type."""
    return [item for item in ITEMS_DB.values() if item.item_type == item_type]


def get_items_by_rarity(rarity: ItemRarity) -> list:
    """Get all items of a specific rarity."""
    return [item for item in ITEMS_DB.values() if item.rarity == rarity]
