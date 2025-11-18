# Epic Quest - API Reference & Developer Guide

## Overview

This document provides a comprehensive reference for developers who want to extend, modify, or integrate with Epic Quest.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Core Modules](#core-modules)
3. [Data Structures](#data-structures)
4. [Game State Management](#game-state-management)
5. [Event System](#event-system)
6. [Extension Points](#extension-points)
7. [Code Examples](#code-examples)

---

## Architecture Overview

### Module Structure

```
game-2/
├── main.py              # Entry point, main game loop, UI
├── character.py         # Character stats, leveling, equipment
├── items.py            # Item definitions and database
├── inventory.py        # Inventory management, shops
├── combat.py           # Combat system, enemies
├── world.py            # Locations, exploration
├── quest.py            # Quest system, objectives
├── crafting.py         # Crafting recipes, system
├── save_system.py      # Save/load functionality
├── achievements.py     # Achievement tracking
├── statistics.py       # Statistics and records
├── character_classes.py # Character class system
└── ui.py               # UI utilities
```

### Design Principles

1. **Data-Driven**: Content defined in dictionaries/databases
2. **Modular**: Each system is self-contained
3. **Extensible**: Easy to add new content
4. **Serializable**: All game state can be saved/loaded

---

## Core Modules

### character.py

#### Class: Character

Main character class managing stats, equipment, and progression.

```python
class Character:
    def __init__(self, name: str = "Hero")

    # Stat Management
    def get_stat(self, stat_name: str) -> int
    def allocate_stat(self, stat_name: str, points: int = 1) -> bool

    # Health Management
    def heal(self, amount: int) -> int
    def take_damage(self, damage: int) -> int
    def is_dead(self) -> bool

    # Experience and Leveling
    def add_xp(self, amount: int) -> bool  # Returns True if leveled up
    def level_up(self) -> bool

    # Equipment
    def equip_item(self, item, slot: str) -> Optional[object]
    def unequip_item(self, slot: str) -> Optional[object]

    # Combat Stats
    def get_attack_damage(self) -> int
    def get_dodge_chance(self) -> float
    def get_crit_chance(self) -> float

    # Gold
    def add_gold(self, amount: int)
    def remove_gold(self, amount: int) -> bool

    # Serialization
    def to_dict(self) -> Dict
    @staticmethod
    def from_dict(data: Dict) -> 'Character'
```

**Key Properties**:
- `name`: Character name
- `level`: Current level
- `xp`: Current experience points
- `base_stats`: Dictionary of base stats
- `equipment_bonuses`: Bonuses from equipment
- `equipped`: Dictionary of equipped items
- `gold`: Current gold
- `stat_points`: Unallocated stat points

---

### items.py

#### Item System

All items inherit from base `Item` class:

```python
class Item:
    def __init__(self, item_id: str, name: str, description: str,
                 item_type: ItemType, value: int = 0,
                 rarity: ItemRarity = ItemRarity.COMMON)
```

**Item Types**:
- `Consumable`: Usable items (potions, etc.)
- `Weapon`: Equipped weapons
- `Armor`: Equipped armor
- `Accessory`: Equipped accessories
- `Material`: Crafting materials
- `QuestItem`: Quest-specific items

**Creating New Items**:

```python
from items import register_item, Weapon, ItemRarity

# Define weapon
register_item(Weapon(
    item_id="awesome_sword",
    name="Awesome Sword",
    description="An incredibly awesome sword",
    value=500,
    damage=35,
    stats={'strength': 12, 'luck': 5},
    level_requirement=10,
    rarity=ItemRarity.EPIC
))

# Item is now accessible via ITEMS_DB
from items import create_item
sword = create_item("awesome_sword")
```

---

### combat.py

#### Combat System

Turn-based combat with action selection:

```python
class Combat:
    def __init__(self, character, enemy: Enemy)

    # Main combat loop
    def execute_turn(self, player_action: CombatAction,
                     item=None) -> List[str]

    # Actions
    def player_attack(self) -> str
    def enemy_attack(self) -> str
    def player_defend(self) -> str
    def player_use_item(self, item) -> Tuple[bool, str]
    def attempt_flee(self) -> Tuple[bool, str]

    # Status
    def get_status(self) -> str
    def get_rewards(self) -> Dict
```

**Creating Enemies**:

```python
from combat import register_enemy, Enemy, EnemyType

register_enemy(Enemy(
    enemy_id="cool_monster",
    name="Cool Monster",
    level=10,
    hp=200,
    strength=25,
    defense=15,
    agility=10,
    xp_reward=150,
    gold_reward=100,
    enemy_type=EnemyType.BEAST,
    loot_table={
        'health_potion_large': 0.5,  # 50% drop chance
        'cool_item': 0.2
    }
))
```

---

### world.py

#### Location System

```python
class Location:
    def __init__(self, location_id: str, name: str, description: str,
                 location_type: LocationType, level_range: tuple = (1, 99),
                 connections: List[str] = None,
                 has_shop: bool = False,
                 has_inn: bool = False,
                 enemy_encounters: List[str] = None,
                 treasure_items: List[str] = None)
```

**Creating Locations**:

```python
from world import Location, LocationType

world.add_location(Location(
    location_id="cool_dungeon",
    name="Cool Dungeon",
    description="A very cool and dangerous dungeon",
    location_type=LocationType.DUNGEON,
    level_range=(8, 12),
    connections=["other_location", "town"],
    enemy_encounters=["cool_monster", "regular_enemy"],
    treasure_items=["awesome_sword", "health_potion_large"]
))
```

---

### quest.py

#### Quest System

```python
class Quest:
    def __init__(self, quest_id: str, name: str, description: str,
                 objectives: List[Objective],
                 level_requirement: int = 1,
                 xp_reward: int = 0,
                 gold_reward: int = 0,
                 item_rewards: List[str] = None,
                 prerequisite_quests: List[str] = None)
```

**Objective Types**:
- `KILL_ENEMY`: Kill specific enemy type
- `COLLECT_ITEM`: Collect specific item
- `VISIT_LOCATION`: Visit a location
- `DELIVER_ITEM`: Deliver item (future)
- `TALK_TO_NPC`: Talk to NPC (future)
- `REACH_LEVEL`: Reach specific level

**Creating Quests**:

```python
from quest import Quest, Objective, ObjectiveType

manager.register_quest(Quest(
    quest_id="slay_monsters",
    name="Monster Slayer",
    description="Defeat 10 cool monsters",
    objectives=[
        Objective(
            objective_id="kill_cool",
            description="Defeat Cool Monsters",
            objective_type=ObjectiveType.KILL_ENEMY,
            target="cool_monster",
            required_amount=10
        )
    ],
    level_requirement=8,
    xp_reward=500,
    gold_reward=300,
    item_rewards=["awesome_sword"]
))
```

---

### crafting.py

#### Crafting System

```python
class Recipe:
    def __init__(self, recipe_id: str, name: str, description: str,
                 materials: Dict[str, int],
                 result_item_id: str,
                 level_requirement: int = 1)

    def can_craft(self, character, inventory) -> tuple
    def craft(self, inventory) -> bool
```

**Creating Recipes**:

```python
from crafting import Recipe

system.register_recipe(Recipe(
    recipe_id="craft_awesome_sword",
    name="Awesome Sword",
    description="Craft the awesome sword",
    materials={
        'steel_ingot': 5,
        'dragon_scale': 2,
        'enchanted_crystal': 1
    },
    result_item_id='awesome_sword',
    level_requirement=10
))
```

---

## Data Structures

### Character Stats Dictionary

```python
{
    'max_hp': int,        # Maximum HP
    'hp': int,            # Current HP
    'strength': int,      # Physical damage
    'defense': int,       # Damage reduction
    'agility': int,       # Dodge and speed
    'intelligence': int,  # XP gain bonus
    'luck': int          # Crit and loot
}
```

### Combat Formulas

```python
# Attack Damage
damage = (character.strength * 2) + weapon.damage

# Critical Hit
crit_chance = character.luck * 0.005  # 0.5% per luck point
if random.random() < crit_chance:
    damage = int(damage * 1.5)

# Defense Reduction
damage_reduction = defender.defense * 0.5
actual_damage = max(1, damage - damage_reduction)

# Dodge
dodge_chance = character.agility * 0.01  # 1% per agility
if random.random() < dodge_chance:
    actual_damage = 0

# XP Gain
intel_bonus = 1.0 + (character.intelligence * 0.01)
actual_xp = int(base_xp * intel_bonus)
```

---

## Game State Management

### Save System

```python
class GameState:
    def save_game(self, save_name: str) -> bool
    def load_game(self, save_name: str) -> bool
    def new_game(self, character_name: str)
```

**Save Data Structure**:

```python
{
    'character': {
        'name': str,
        'level': int,
        'xp': int,
        'base_stats': dict,
        'equipped': dict,
        'gold': int,
        # ... more fields
    },
    'inventory': {
        'max_capacity': int,
        'items': dict  # item_id -> quantity
    },
    'world': {
        'current_location_id': str,
        'locations': dict  # location state
    },
    'quests': {
        'active_quests': dict,
        'completed_quests': list
    },
    'crafting': {
        'discovered_recipes': list
    }
}
```

---

## Event System

### Quest Progress Tracking

Update quest progress from anywhere:

```python
# After killing enemy
quest_manager.update_quest_progress(
    ObjectiveType.KILL_ENEMY,
    enemy_id,
    amount=1
)

# After collecting item
quest_manager.update_quest_progress(
    ObjectiveType.COLLECT_ITEM,
    item_id,
    amount=1
)

# After visiting location
quest_manager.update_quest_progress(
    ObjectiveType.VISIT_LOCATION,
    location_id,
    amount=1
)
```

---

## Extension Points

### Adding New Item Type

1. Define enum in items.py:
```python
class ItemType(Enum):
    # ... existing types
    NEW_TYPE = "new_type"
```

2. Create new class:
```python
class NewItem(Item):
    def __init__(self, item_id, name, description, ...):
        super().__init__(item_id, name, description,
                         ItemType.NEW_TYPE, ...)
```

3. Update create_item() function to handle new type

### Adding New Objective Type

1. Define in quest.py:
```python
class ObjectiveType(Enum):
    # ... existing
    NEW_OBJECTIVE = "new_objective"
```

2. Update Quest.update_objective() to handle new type

3. Call update_quest_progress() when objective completed

### Adding New Location Type

1. Define in world.py:
```python
class LocationType(Enum):
    # ... existing
    NEW_LOCATION = "new_location"
```

2. Update encounter chances in Location.get_encounter_chance()

---

## Code Examples

### Example 1: Adding a New Boss Fight

```python
# 1. Create the enemy
from combat import register_enemy, Enemy, EnemyType

register_enemy(Enemy(
    enemy_id="mega_boss",
    name="Mega Boss",
    level=20,
    hp=1000,
    strength=60,
    defense=50,
    agility=30,
    xp_reward=2000,
    gold_reward=5000,
    enemy_type=EnemyType.DEMON,
    loot_table={
        'legendary_weapon': 1.0,  # Guaranteed drop
        'phoenix_down': 0.8,
        'health_potion_supreme': 1.0
    }
))

# 2. Create boss arena location
from world import Location, LocationType

world.add_location(Location(
    location_id="boss_arena",
    name="Mega Boss Arena",
    description="The lair of the Mega Boss",
    location_type=LocationType.DUNGEON,
    level_range=(20, 20),
    connections=["previous_location"],
    enemy_encounters=["mega_boss"],
    treasure_items=[]
))

# 3. Create quest to defeat boss
from quest import Quest, Objective, ObjectiveType

quest_manager.register_quest(Quest(
    quest_id="defeat_mega_boss",
    name="Defeat the Mega Boss",
    description="Challenge the legendary Mega Boss",
    objectives=[
        Objective(
            "kill_boss",
            "Defeat Mega Boss",
            ObjectiveType.KILL_ENEMY,
            "mega_boss",
            1
        )
    ],
    level_requirement=18,
    xp_reward=5000,
    gold_reward=10000,
    item_rewards=['legendary_weapon'],
    prerequisite_quests=['previous_quest']
))
```

### Example 2: Adding a New Crafting Chain

```python
from crafting import Recipe
from items import register_item, Material, Weapon, ItemRarity

# 1. Create new material
register_item(Material(
    "mythril_ore",
    "Mythril Ore",
    "Rare ore from deep mines",
    value=200,
    rarity=ItemRarity.RARE
))

# 2. Create processing recipe
system.register_recipe(Recipe(
    "smelt_mythril",
    "Mythril Ingot",
    "Smelt mythril ore into ingots",
    materials={'mythril_ore': 3},
    result_item_id='mythril_ingot',
    level_requirement=10
))

# 3. Create mythril ingot item
register_item(Material(
    "mythril_ingot",
    "Mythril Ingot",
    "Processed mythril ready for crafting",
    value=500,
    rarity=ItemRarity.RARE
))

# 4. Create weapon using mythril
register_item(Weapon(
    "mythril_blade",
    "Mythril Blade",
    "A blade forged from mythril",
    value=2000,
    damage=55,
    stats={'strength': 15, 'agility': 8},
    level_requirement=12,
    rarity=ItemRarity.EPIC
))

# 5. Create crafting recipe for weapon
system.register_recipe(Recipe(
    "craft_mythril_blade",
    "Mythril Blade",
    "Forge a blade from mythril",
    materials={
        'mythril_ingot': 5,
        'dragon_scale': 2
    },
    result_item_id='mythril_blade',
    level_requirement=12
))
```

### Example 3: Adding Achievement with Tracking

```python
from achievements import Achievement, AchievementCategory, AchievementRarity

# 1. Register achievement
manager.register_achievement(Achievement(
    "speed_demon",
    "Speed Demon",
    "Complete 10 battles in under 3 turns each",
    AchievementCategory.COMBAT,
    AchievementRarity.RARE,
    points=40,
    reward_gold=1000
))

# 2. Track progress in combat (in main.py or combat.py)
# After each battle:
if combat.turn_count <= 3 and combat.result == CombatResult.VICTORY:
    achievement = achievements.get_achievement("speed_demon")
    if achievement:
        achievement.progress_max = 10
        achievement.update_progress(1)

        if achievement.unlocked:
            print(f"🏆 Achievement Unlocked: {achievement.name}")
            # Grant rewards
            character.add_gold(achievement.reward_gold)
```

---

## Testing

### Running Tests

```bash
python test_game.py
```

### Writing Tests

```python
import unittest
from character import Character
from items import create_item

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.char = Character("Test")

    def test_new_functionality(self):
        # Your test code
        self.assertEqual(expected, actual)
```

---

## Performance Considerations

### Optimization Tips

1. **Lazy Loading**: Don't load all game data at startup
2. **Caching**: Cache frequently accessed data
3. **Efficient Data Structures**: Use dictionaries for O(1) lookups
4. **Minimize File I/O**: Batch save operations

### Memory Management

- Item instances are created on-demand (create_item())
- Templates stored in ITEMS_DB
- Inventory stores item IDs, not instances
- Save files are JSON (human-readable but larger)

---

## Best Practices

### Code Style

1. Follow PEP 8
2. Use type hints
3. Document with docstrings
4. Keep functions focused

### Data Design

1. Use IDs for references (not object references)
2. Make everything serializable
3. Validate input data
4. Provide defaults

### Error Handling

```python
def safe_operation(param):
    """
    Perform operation with error handling.
    Returns (success: bool, result: Any)
    """
    try:
        result = risky_operation(param)
        return True, result
    except Exception as e:
        print(f"Error: {e}")
        return False, None
```

---

## Debugging

### Debug Mode

Add debug prints:
```python
DEBUG = True

if DEBUG:
    print(f"DEBUG: Character HP: {character.hp}")
```

### Save File Inspection

Save files are JSON - can be edited manually:
```bash
cat saves/my_save.json | python -m json.tool
```

### Common Issues

1. **Item not appearing**: Check ITEMS_DB registration
2. **Quest not updating**: Verify objective type and target match
3. **Crash on load**: Check save file format version
4. **Balance issues**: Adjust formulas in combat.py

---

## Contributing

See CONTRIBUTING.md for:
- Code submission process
- Style guidelines
- Testing requirements
- Documentation standards

---

## API Changelog

### Version 1.0
- Initial API release
- Core game systems implemented
- Basic extensibility features

### Future Additions
- Event system for custom hooks
- Plugin architecture
- Mod support
- Multiplayer API

---

*For questions or clarifications, please open an issue on GitHub.*
