# Epic Quest: A Text-Based RPG Adventure

## Overview
Epic Quest is a comprehensive text-based role-playing game featuring character progression, turn-based combat, inventory management, quest systems, and an explorable world.

## Features
- **Character System**: Create your character with customizable stats and leveling
- **Character Classes**: Choose from 5 unique classes (Warrior, Mage, Rogue, Paladin, Ranger)
- **Combat System**: Turn-based battles with multiple enemy types
- **Inventory Management**: Collect, use, and manage items and equipment
- **Quest System**: Complete quests to earn rewards and advance the story
- **World Exploration**: Navigate through multiple interconnected locations
- **Save/Load System**: Save your progress and continue your adventure later
- **Crafting System**: Combine items to create powerful equipment
- **Achievement System**: Unlock 40+ achievements for completing challenges
- **Statistics Tracking**: Detailed stats tracking for all your accomplishments
- **Shop System**: Buy and sell items at various shops
- **NPC Interactions**: Meet and interact with various characters

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd game-2

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# No additional dependencies required - uses only Python standard library
```

## How to Play

### Starting the Game
```bash
python main.py
```

### Controls
The game uses a text-based menu system. Simply enter the number or letter corresponding to your choice.

### Basic Gameplay
1. **Create Your Character**: Choose your name and allocate starting stat points
2. **Explore the World**: Move between locations and discover new areas
3. **Complete Quests**: Accept and complete quests from NPCs
4. **Battle Enemies**: Engage in turn-based combat with various foes
5. **Manage Inventory**: Collect items, equip gear, and use consumables
6. **Level Up**: Gain experience and improve your character's abilities
7. **Craft Items**: Combine materials to create powerful equipment

### Game Mechanics

#### Stats
- **HP (Health Points)**: Your life force - when it reaches 0, game over
- **Strength**: Increases physical damage in combat
- **Defense**: Reduces incoming damage
- **Agility**: Affects dodge chance and turn order
- **Intelligence**: Improves magic abilities and XP gain
- **Luck**: Affects critical hit chance and loot quality

#### Combat
- Turn-based system where you choose actions each turn
- Actions include: Attack, Defend, Use Item, or Flee
- Defeating enemies grants XP and loot
- Strategic use of items and abilities is key to victory

#### Leveling
- Gain experience points (XP) by defeating enemies and completing quests
- Each level grants stat points to allocate
- XP required increases with each level

#### Items
- **Consumables**: Healing potions, stat boosters
- **Equipment**: Weapons and armor to enhance your stats
- **Materials**: Used in crafting recipes
- **Quest Items**: Required for specific quests

## Game Structure

### File Organization
```
game-2/
├── main.py              # Entry point and main game loop
├── character.py         # Character class and stats management
├── combat.py           # Combat system and enemy AI
├── inventory.py        # Inventory and item management
├── world.py            # Location and world exploration
├── quest.py            # Quest system and objectives
├── items.py            # Item definitions and effects
├── save_system.py      # Save/load functionality
├── crafting.py         # Crafting recipes and system
├── ui.py              # User interface utilities
└── game_data.py       # Game data and configuration
```

## Strategy Tips
1. Balance your stats - don't neglect defense!
2. Keep healing potions in your inventory at all times
3. Explore thoroughly to find hidden items and quests
4. Complete easier quests first to level up
5. Craft equipment when you have the materials
6. Save your game frequently!

## Documentation

- **[Game Guide](GAME_GUIDE.md)**: Complete strategy guide and walkthrough
- **[API Reference](API_REFERENCE.md)**: Developer documentation for extending the game
- **[Design Document](DESIGN.md)**: Game design philosophy and systems
- **[Contributing](CONTRIBUTING.md)**: How to contribute to the project
- **[Changelog](CHANGELOG.md)**: Version history and updates

## Content Summary

### Items (20+)
- 8 Weapons (Rusty Sword to Excalibur)
- 6 Armor Sets (Cloth to Dragon Scale)
- 7 Accessories (Bronze Ring to Phoenix Pendant)
- 6 Consumables (Health Potions to Phoenix Down)
- 8 Crafting Materials
- 5 Quest Items

### Enemies (13+)
- Early: Slimes, Wolves, Goblins, Bandits
- Mid: Skeletons, Orcs, Trolls, Dark Mages
- Late: Vampires, Wyverns, Demons
- Bosses: Goblin Chief, Ancient Dragon, Lich King

### Locations (15+)
- 3 Towns with shops and inns
- 5 Wilderness areas
- 4 Caves and dungeons
- 3 Special locations

### Quests (15+)
- Combat quests
- Collection quests
- Exploration quests
- Boss battles

### Achievements (40+)
- Combat achievements
- Exploration achievements
- Collection achievements
- Progression achievements
- Secret achievements

### Character Classes (5)
- Warrior: Tank and damage dealer
- Mage: Intelligence and magic focus
- Rogue: Agility and critical hits
- Paladin: Balanced holy warrior
- Ranger: Wilderness specialist

## Future Enhancements
- [ ] Magic system with spells and MP
- [ ] Skill trees for deeper customization
- [ ] More boss encounters
- [ ] Random dungeon generation
- [ ] Multiplayer features
- [ ] Trading system with NPCs
- [ ] Pet/companion system
- [ ] New Game Plus mode
- [ ] Difficulty settings
- [ ] More quests and storylines

## Contributing
Feel free to fork this project and add your own features! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Testing
Run the test suite:
```bash
python test_game.py
```

All tests should pass (37/37 tests passing).

## License
MIT License - Feel free to use and modify as you wish.

## Credits
Created as a demonstration of Python game development principles and comprehensive game design.
