"""
Character Classes module - Defines different character classes/archetypes.
"""

from typing import Dict, List
from enum import Enum


class CharacterClass(Enum):
    """Available character classes."""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    PALADIN = "paladin"
    RANGER = "ranger"


class ClassDefinition:
    """
    Defines a character class with its bonuses and abilities.
    """

    def __init__(self, class_id: str, name: str, description: str,
                 stat_bonuses: Dict[str, int], starting_items: List[str],
                 passive_abilities: List[str]):
        self.class_id = class_id
        self.name = name
        self.description = description
        self.stat_bonuses = stat_bonuses  # Bonus stats for this class
        self.starting_items = starting_items  # Starting equipment
        self.passive_abilities = passive_abilities  # Passive ability descriptions

    def apply_bonuses(self, character):
        """Apply class bonuses to character."""
        for stat, bonus in self.stat_bonuses.items():
            if stat in character.base_stats:
                character.base_stats[stat] += bonus

    def get_display(self) -> str:
        """Get formatted class display."""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"{self.name.upper()}")
        output.append(f"{'='*60}")
        output.append(f"\n{self.description}\n")

        output.append("Starting Bonuses:")
        for stat, bonus in self.stat_bonuses.items():
            if bonus > 0:
                output.append(f"  +{bonus} {stat.replace('_', ' ').title()}")

        output.append("\nStarting Equipment:")
        from items import get_item
        for item_id in self.starting_items:
            item = get_item(item_id)
            if item:
                output.append(f"  • {item.name}")

        output.append("\nPassive Abilities:")
        for ability in self.passive_abilities:
            output.append(f"  • {ability}")

        output.append(f"\n{'='*60}")
        return '\n'.join(output)


# =============================================================================
# CLASS DEFINITIONS
# =============================================================================

CLASSES = {}


def register_class(class_def: ClassDefinition):
    """Register a character class."""
    CLASSES[class_def.class_id] = class_def


# === WARRIOR ===
register_class(ClassDefinition(
    "warrior", "Warrior",
    "A mighty warrior skilled in close combat. Excels at dealing and taking damage. "
    "Warriors have high strength and HP, making them excellent frontline fighters.",
    stat_bonuses={
        'max_hp': 30,
        'strength': 5,
        'defense': 3,
        'agility': -2
    },
    starting_items=['iron_sword', 'leather_armor', 'health_potion_small'],
    passive_abilities=[
        "Battle Hardened: +30% HP",
        "Weapon Master: +5 Strength",
        "Thick Skin: +3 Defense",
        "Heavy Armor: -2 Agility"
    ]
))

# === MAGE ===
register_class(ClassDefinition(
    "mage", "Mage",
    "A scholar of arcane arts who relies on intelligence and magical prowess. "
    "Mages gain bonus experience and have enhanced critical hit chances.",
    stat_bonuses={
        'max_hp': -20,
        'strength': -3,
        'intelligence': 8,
        'luck': 3
    },
    starting_items=['staff_apprentice', 'cloth_armor', 'health_potion_small',
                    'health_potion_small'],
    passive_abilities=[
        "Arcane Knowledge: +8 Intelligence (faster leveling)",
        "Lucky Scholar: +3 Luck (better crits and loot)",
        "Frail Body: -20 HP, -3 Strength",
        "Quick Study: Discover crafting recipes faster"
    ]
))

# === ROGUE ===
register_class(ClassDefinition(
    "rogue", "Rogue",
    "A nimble and cunning fighter who strikes from the shadows. "
    "Rogues excel at dodging attacks and landing critical hits.",
    stat_bonuses={
        'max_hp': 10,
        'strength': 2,
        'agility': 6,
        'luck': 4
    },
    starting_items=['rusty_sword', 'leather_armor', 'bronze_ring',
                    'health_potion_small'],
    passive_abilities=[
        "Shadow Step: +6 Agility (high dodge chance)",
        "Fortune's Favor: +4 Luck (critical hits and loot)",
        "Light Fighter: +2 Strength",
        "Treasure Hunter: Find more gold and items"
    ]
))

# === PALADIN ===
register_class(ClassDefinition(
    "paladin", "Paladin",
    "A holy warrior who balances offense and defense. "
    "Paladins are versatile fighters with balanced stats and regeneration.",
    stat_bonuses={
        'max_hp': 20,
        'strength': 3,
        'defense': 4,
        'intelligence': 2
    },
    starting_items=['iron_sword', 'chain_mail', 'silver_amulet',
                    'health_potion_medium'],
    passive_abilities=[
        "Divine Health: +20 HP",
        "Holy Strength: +3 Strength, +4 Defense",
        "Blessed Mind: +2 Intelligence",
        "Righteous: Potions heal 20% more"
    ]
))

# === RANGER ===
register_class(ClassDefinition(
    "ranger", "Ranger",
    "A skilled hunter and survivalist. Rangers excel in exploration and "
    "have bonuses against beasts and wilderness enemies.",
    stat_bonuses={
        'max_hp': 15,
        'strength': 3,
        'agility': 4,
        'intelligence': 1,
        'luck': 2
    },
    starting_items=['iron_sword', 'leather_armor', 'health_potion_small',
                    'health_potion_small', 'health_potion_small'],
    passive_abilities=[
        "Hunter's Physique: +15 HP, +3 Strength",
        "Swift Tracker: +4 Agility",
        "Wilderness Lore: +1 Intelligence, +2 Luck",
        "Beast Slayer: +20% damage vs beasts",
        "Survivalist: Extra starting potions"
    ]
))


def get_class(class_id: str) -> ClassDefinition:
    """Get a class definition by ID."""
    return CLASSES.get(class_id)


def get_all_classes() -> List[ClassDefinition]:
    """Get all available classes."""
    return list(CLASSES.values())


def display_class_selection() -> str:
    """Display all classes for selection."""
    output = []
    output.append("\n" + "="*70)
    output.append("SELECT YOUR CLASS")
    output.append("="*70)
    output.append("\nChoose your character class to gain special bonuses and abilities:\n")

    for i, class_def in enumerate(get_all_classes(), 1):
        output.append(f"{i}. {class_def.name} - {class_def.description[:60]}...")

    return '\n'.join(output)
