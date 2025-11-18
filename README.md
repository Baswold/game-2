# Epic Quest: A Text-Based RPG Adventure

## Overview
Epic Quest is a comprehensive text-based role-playing game featuring character progression, turn-based combat, inventory management, quest systems, and an explorable world.

## Features
- **Character System**: Create your character with customizable stats and leveling
- **Combat System**: Turn-based battles with multiple enemy types
- **Inventory Management**: Collect, use, and manage items and equipment
- **Quest System**: Complete quests to earn rewards and advance the story
- **World Exploration**: Navigate through multiple interconnected locations
- **Save/Load System**: Save your progress and continue your adventure later
- **Crafting System**: Combine items to create powerful equipment
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

## Future Enhancements (TODO)
- [ ] Magic system with spells
- [ ] More diverse enemy types
- [ ] Boss battles
- [ ] Multiple character classes
- [ ] Skill trees
- [ ] Multiplayer features
- [ ] Achievements system
- [ ] Random dungeon generation
- [ ] Trading system with NPCs
- [ ] Pet/companion system

## Contributing
Feel free to fork this project and add your own features!

## License
MIT License - Feel free to use and modify as you wish.

## Credits
Created as a demonstration of Python game development principles.
