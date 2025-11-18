# Contributing to Epic Quest

Thank you for your interest in contributing to Epic Quest! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Your environment (OS, Python version)
- Any relevant logs or screenshots

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear description of the feature
- Why this feature would be useful
- Possible implementation approaches
- Any relevant examples from other games

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`python test_game.py`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and single-purpose
- Comment complex logic

### Project Structure

```
game-2/
├── main.py              # Entry point and main game loop
├── character.py         # Character class and stats
├── combat.py           # Combat system
├── inventory.py        # Inventory management
├── items.py            # Item definitions
├── world.py            # World and locations
├── quest.py            # Quest system
├── crafting.py         # Crafting system
├── save_system.py      # Save/load functionality
├── ui.py              # UI utilities
└── test_game.py       # Test suite
```

### Adding New Content

#### Adding a New Item

1. Open `items.py`
2. Create item using appropriate class (Weapon, Armor, Consumable, etc.)
3. Register with `register_item()`
4. Add to shops if applicable (in `inventory.py`)

Example:
```python
register_item(Weapon(
    "cool_sword", "Cool Sword",
    "A really cool sword",
    value=100, damage=25,
    stats={'strength': 15},
    level_requirement=10,
    rarity=ItemRarity.RARE
))
```

#### Adding a New Enemy

1. Open `combat.py`
2. Create enemy template using `register_enemy()`
3. Add to location encounters in `world.py` if needed

Example:
```python
register_enemy(Enemy(
    "cool_monster", "Cool Monster", 10,
    hp=200, strength=30, defense=20, agility=15,
    xp_reward=150, gold_reward=100,
    enemy_type=EnemyType.BEAST,
    loot_table={'health_potion_large': 0.5}
))
```

#### Adding a New Location

1. Open `world.py`
2. Add location in `create_game_world()`
3. Connect to existing locations via `connections` parameter
4. Add enemies and treasures as appropriate

Example:
```python
world.add_location(Location(
    "cool_place", "Cool Place",
    "A very cool location to explore",
    LocationType.DUNGEON,
    level_range=(8, 12),
    connections=["other_location"],
    enemy_encounters=["cool_monster"],
    treasure_items=["cool_sword"]
))
```

#### Adding a New Quest

1. Open `quest.py`
2. Add quest in `create_all_quests()`
3. Define objectives and rewards

Example:
```python
manager.register_quest(Quest(
    "cool_quest", "Cool Quest",
    "A cool quest to complete",
    objectives=[
        Objective("do_thing", "Do the thing",
                 ObjectiveType.KILL_ENEMY, "cool_monster", 5)
    ],
    level_requirement=10,
    xp_reward=500,
    gold_reward=300,
    item_rewards=["cool_sword"]
))
```

### Testing

- Write tests for new features
- Ensure all existing tests pass
- Test edge cases and error conditions
- Run the full test suite: `python test_game.py`

### Documentation

- Update README.md if adding major features
- Add docstrings to new classes and functions
- Update this CONTRIBUTING.md if changing development process
- Comment complex algorithms or game mechanics

## Balance Guidelines

When adding new content, consider game balance:

### Items
- **Common**: 1-5x character level in value
- **Uncommon**: 5-10x character level
- **Rare**: 10-20x character level
- **Epic**: 20-50x character level
- **Legendary**: 50+ character level

### Enemies
- HP: Roughly 20-50 per level
- Damage: Roughly 10-30 per level
- XP Reward: 10-20 per level
- Gold Reward: 5-15 per level

### Quests
- XP should be 2-5x typical combat encounter
- Gold should be 2-3x typical combat encounter
- Item rewards should match quest difficulty

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Reach out to maintainers
- Check existing issues and pull requests

Thank you for contributing to Epic Quest!
