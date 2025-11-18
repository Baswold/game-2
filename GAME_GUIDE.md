# Epic Quest - Complete Game Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Character Creation](#character-creation)
3. [Combat Mechanics](#combat-mechanics)
4. [Exploration Guide](#exploration-guide)
5. [Questing](#questing)
6. [Crafting](#crafting)
7. [Character Builds](#character-builds)
8. [Advanced Strategies](#advanced-strategies)
9. [Enemy Guide](#enemy-guide)
10. [Item Guide](#item-guide)
11. [Achievement Guide](#achievement-guide)
12. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### First Steps
1. Launch the game: `python main.py`
2. Create a new character or load an existing save
3. Choose your character name and class
4. Allocate your starting stat points
5. Begin your adventure in Hometown Village!

### Understanding the Interface
- **Main Menu**: Your hub for all game actions
- **Character Screen**: View and manage your stats
- **Inventory**: Manage items and equipment
- **Map/Travel**: Move between locations
- **Quests**: Track and complete objectives

### Save System
- **Manual Saves**: Use the Save Game option from main menu
- **Multiple Slots**: Create multiple characters
- **Auto-Save**: Save before attempting dangerous content
- **Backup**: Save files stored in `saves/` directory

---

## Character Creation

### Choosing a Class

#### Warrior
**Best for**: Beginners, straightforward gameplay
**Playstyle**: Tank damage, deal damage, survive
**Strengths**: High HP and defense, consistent damage
**Weaknesses**: Low agility (dodges less), slower leveling

**Recommended Stats**:
- Primary: Strength, Defense
- Secondary: Max HP
- Dump: Intelligence (not needed for warrior)

#### Mage
**Best for**: Experienced players, efficiency focused
**Playstyle**: Glass cannon, fast progression
**Strengths**: Fast leveling, great loot, high crits
**Weaknesses**: Low HP, fragile in early game

**Recommended Stats**:
- Primary: Intelligence, Luck
- Secondary: Agility (for dodging)
- Dump: Strength (compensate with better weapons)

#### Rogue
**Best for**: Risk/reward players, skilled gameplay
**Playstyle**: Dodge and crit, high skill ceiling
**Strengths**: Best dodge chance, excellent crits, good loot
**Weaknesses**: Requires good timing, moderate HP

**Recommended Stats**:
- Primary: Agility, Luck
- Secondary: Strength
- Dump: Defense (rely on dodging)

#### Paladin
**Best for**: Balanced gameplay, versatility
**Playstyle**: All-rounder, adaptable
**Strengths**: No major weaknesses, good survivability
**Weaknesses**: No major strengths, jack-of-all-trades

**Recommended Stats**:
- Balanced across all stats
- Slight emphasis on HP and Defense

#### Ranger
**Best for**: Exploration focused, beast hunters
**Playstyle**: Wilderness specialist
**Strengths**: Great vs beasts, good survivability, extra potions
**Weaknesses**: Less effective vs undead/demons

**Recommended Stats**:
- Primary: Agility, Strength
- Secondary: Luck
- Balanced approach

### Starting Stat Allocation

You get 5 starting stat points. Here are recommended distributions:

**New Players**:
- +2 Max HP, +2 Strength, +1 Defense

**Experienced Players**:
- +3 Primary Stat, +2 Secondary Stat

**Min-Maxers**:
- +5 to single stat for extreme build

---

## Combat Mechanics

### Turn Order
- Determined by Agility + random roll
- Higher agility = more likely to go first
- Going first can be crucial for healing or escaping

### Actions

#### Attack
- **Damage Formula**: (Strength × 2) + Weapon Damage
- **Critical Hits**: Chance based on Luck (0.5% per point)
- **Critical Multiplier**: 1.5x damage
- **When to Use**: Default action in most situations

#### Defend
- **Damage Reduction**: 50% damage reduction on next hit
- **Duration**: One turn only
- **When to Use**:
  - Low HP and waiting to heal next turn
  - Enemy is about to attack and you can't kill them
  - Boss battles for survival

#### Use Item
- **Takes a turn**: Healing costs your action
- **Strategic**: Use between enemy attacks
- **When to Use**:
  - Below 30% HP (danger zone)
  - Before boss battles (buff items)
  - After defending to recover safely

#### Flee
- **Success Chance**: Base 50%, affected by:
  - Agility: +1% per point
  - Level difference: -5% per level higher enemy
  - Multiple attempts: -10% per attempt
- **When to Use**:
  - Severely outmatched
  - Low HP and no healing items
  - Want to preserve resources

### Defense Mechanics
- **Flat Reduction**: Defense × 0.5 subtracted from damage
- **Minimum Damage**: Always take at least 1 damage
- **Stacking**: Base defense + armor + buffs

### Dodge Mechanics
- **Dodge Chance**: 1% per Agility point (max 50%)
- **Total Avoidance**: Dodge = take 0 damage
- **Luck Factor**: Slight random variance

### Enemy Behavior
- Enemies attack every turn (no defend/flee)
- Damage variance: ±2 from base
- No special abilities (yet)
- Predictable patterns

---

## Exploration Guide

### World Map

#### Starting Zone (Levels 1-3)
1. **Hometown Village** (Safe Zone)
   - Shops, inn, quest givers
   - Your starting location

2. **Sunny Meadow** (Level 1-3)
   - Slimes, Wolves
   - Easy treasures
   - Good starter zone

3. **Forest Path** (Level 2-4)
   - Goblins, Wolves, Bandits
   - Connects to many areas
   - Important hub location

#### Mid Zone (Levels 4-8)
4. **Port City** (Safe Zone)
   - Better shops
   - Advanced quests

5. **Dark Forest** (Level 5-7)
   - Skeletons, Dark Mages
   - Magical items
   - Witch's Hut shop

6. **Goblin Camp** (Level 3-5)
   - Goblin Chief boss
   - Good loot
   - Quest location

7. **Beach Cave** (Level 4-6)
   - Bandits, Skeletons
   - Silver ore
   - Coastal loot

#### High Zone (Levels 8-12)
8. **Mountain Village** (Safe Zone)
   - Mountain gear shops
   - Cold weather items

9. **Snowy Peaks** (Level 9-12)
   - Wyverns, Trolls, Demons
   - Dragon scales
   - Extreme danger

10. **Crystal Cavern** (Level 8-10)
    - Dark Mages, Demons
    - Enchanted crystals
    - Magic items

#### Endgame (Levels 13+)
11. **Dragon's Lair** (Level 15+)
    - Ancient Dragon boss
    - Best loot in game
    - Legendary items

12. **Cursed Castle** (Level 18+)
    - Lich King final boss
    - Ultimate challenge
    - Legendary rewards

### Exploration Tips

#### Treasure Hunting
- **Check Everything**: Explore action in each location
- **One-Time Loot**: Treasures don't respawn
- **Risk vs Reward**: Dangerous areas have better loot
- **Luck Matters**: Higher luck = better treasure quality

#### Random Encounters
- **Encounter Rates**:
  - Towns: 0%
  - Wilderness: 30%
  - Caves: 50%
  - Dungeons: 60%
- **When Traveling**: Can trigger encounter
- **When Exploring**: Higher chance but also treasure

#### Safe Travel
1. Stock up on potions before leaving town
2. Save before entering dangerous areas
3. Keep HP above 50% between fights
4. Retreat to town if resources low
5. Use inn to restore HP cheaply (20g)

---

## Questing

### Quest Types

#### Kill Quests
- **Objective**: Defeat specific enemies
- **Tips**:
  - Progress tracks automatically
  - Can complete while exploring
  - Good for grinding levels

#### Collection Quests
- **Objective**: Collect specific items
- **Tips**:
  - Check enemy loot tables
  - Some items are treasures
  - Craft if possible

#### Exploration Quests
- **Objective**: Visit locations
- **Tips**:
  - Easiest quest type
  - Combine with other objectives
  - Unlock new areas

#### Boss Quests
- **Objective**: Defeat boss enemies
- **Tips**:
  - Prepare thoroughly
  - Stock healing items
  - Save beforehand
  - Boss-specific loot

### Quest Rewards
- **XP**: Often 2-5x combat XP
- **Gold**: 2-3x combat gold
- **Items**: Unique or rare items
- **Unlock**: Some quests unlock others

### Quest Strategy
1. Accept all available quests
2. Complete passively while exploring
3. Turn in when ready
4. Prioritize XP rewards when underleveled
5. Save boss quests for appropriate level

---

## Crafting

### Recipe System
- **Discovery**: Find recipes exploring or automatically
- **Requirements**: Materials + Level
- **One-Time**: Each craft uses materials

### Material Farming

#### Common Materials
- **Iron Ore**: Goblin Camp, Mines (Goblins, Bandits)
- **Leather Scraps**: Meadow, Forest (Slimes, Wolves)
- **Wood Planks**: Forest areas (treasures)

#### Uncommon Materials
- **Steel Ingots**: Craft from 3x Iron Ore
- **Silver Ore**: Beach Cave, Ruins (Vampires)
- **Enchanted Crystals**: Dark Forest, Crystal Cavern (Mages)

#### Rare Materials
- **Dragon Scales**: Dragon's Lair, Snowy Peaks (Dragons, Wyverns)
- **Star Fragments**: Cursed Castle (Lich King)

### Essential Recipes

#### Early Game
1. **Steel Ingot** (from Iron Ore)
   - Enables better crafting
   - Farm iron ore first

2. **Iron Sword**
   - First weapon upgrade
   - Better than rusty sword

3. **Leather Armor**
   - Defense boost
   - Easy materials

#### Mid Game
1. **Steel Sword**
   - Significant damage upgrade
   - Worth the investment

2. **Chain Mail**
   - Good defense
   - Bridges to plate armor

3. **Medium Health Potions**
   - Combine 3 small potions
   - More efficient healing

#### Late Game
1. **Dragon Slayer** (sword)
   - Legendary weapon
   - Dragon scales required

2. **Dragon Armor**
   - Best craftable armor
   - High defense

3. **Crown of Wisdom**
   - Intelligence boost
   - Rare materials

### Crafting Strategy
1. Unlock Steel Ingot early
2. Craft weapons > armor > accessories
3. Don't craft items you can buy cheap
4. Save rare materials for legendary items
5. Craft consumables if excess materials

---

## Character Builds

### The Tank (Warrior Focus)
**Stats**: HP > Defense > Strength
**Equipment**: Plate Armor, any weapon, defensive accessory
**Strategy**: Face-tank everything, outlast enemies
**Pros**: Very forgiving, great for beginners
**Cons**: Slow battles, less XP gain

### The Glass Cannon (Mage Focus)
**Stats**: Intelligence > Luck > Agility
**Equipment**: Mage Staff, light armor, luck accessories
**Strategy**: Fast leveling, dodge and crit
**Pros**: Fastest progression, best loot
**Cons**: Can die quickly if unlucky

### The Dodge Master (Rogue Focus)
**Stats**: Agility > Luck > Strength
**Equipment**: Fast weapons, light armor, agility rings
**Strategy**: Never get hit, crit when you do hit
**Pros**: Most fun, high skill ceiling
**Cons**: RNG dependent

### The Balanced Hero (Paladin Focus)
**Stats**: Balanced allocation
**Equipment**: Best available in all slots
**Strategy**: Adapt to situation
**Pros**: No weaknesses, versatile
**Cons**: Not optimal at anything

### The Critical Striker
**Stats**: Luck > Strength > Agility
**Equipment**: High damage weapon, crit accessories
**Strategy**: Stack luck, fish for crits
**Pros**: Satisfying gameplay, good damage
**Cons**: Inconsistent

### The Lucky Looter
**Stats**: Luck > Intelligence > Agility
**Equipment**: All luck accessories
**Strategy**: Maximize drops and XP
**Pros**: Best loot, fastest leveling
**Cons**: Weaker in combat

---

## Advanced Strategies

### Gold Farming
1. **Quest Rewards**: Most reliable gold source
2. **Boss Farming**: Revisit beatable bosses
3. **Selling Loot**: Sell duplicate equipment
4. **Smart Shopping**: Buy low rarity, sell found high rarity

### XP Optimization
1. **Intelligence**: Each point = 1% more XP
2. **Quest Chain**: Complete quests for XP bursts
3. **Level Range**: Fight enemies near your level
4. **Mage Class**: Best for fast leveling

### Resource Management
1. **Potions**: Keep 5-10 small potions always
2. **Gold**: Save 1000g for emergencies
3. **Inventory**: Don't hoard, sell excess
4. **Save Slots**: Use multiple for experiments

### Combat Optimization
1. **First Turn**: Try to go first (Agility)
2. **One-Shot**: If you can kill, always attack
3. **Defend + Heal**: Defend one turn, heal next
4. **Flee Early**: Don't waste resources on unwinnable fights

### Achievement Hunting
1. **Secret Start**: New game triggers achievements
2. **Combat**: Track kills for slayer achievements
3. **Collection**: Don't sell unique items until achievement
4. **Exploration**: Visit all locations for completion

---

## Enemy Guide

### Early Game (Levels 1-4)
- **Slime** (Lv.1): Weakest enemy, good for starting
- **Wolf** (Lv.2): Fast, can dodge
- **Goblin** (Lv.2): Balanced threat
- **Bandit** (Lv.3): Decent gold drops
- **Goblin Chief** (Lv.5): First boss, prepare potions

### Mid Game (Levels 5-8)
- **Skeleton Warrior** (Lv.5): Undead, high defense
- **Orc Brute** (Lv.6): High HP and damage
- **Dark Mage** (Lv.7): Agile, magic themed
- **Troll** (Lv.8): Tank, slow but hard hitting

### Late Game (Levels 9-12)
- **Vampire Lord** (Lv.10): Fast, high damage
- **Wyvern** (Lv.11): Dragon-type, balanced
- **Lesser Demon** (Lv.12): Powerful, good loot

### Endgame Bosses (Levels 13+)
- **Ancient Dragon** (Lv.15): 500 HP, massive damage, best loot
- **Lich King** (Lv.18): 600 HP, ultimate challenge

### Enemy-Specific Strategies

#### vs High Damage (Orcs, Dragons)
- Prioritize Defense
- Use Defend action
- Keep HP high

#### vs High Agility (Wolves, Mages)
- Increase Accuracy (not implemented, just keep attacking)
- Use crowd control (future)
- Stack strength for higher damage

#### vs Bosses
- Full HP before engaging
- 10+ healing potions
- Best equipment
- Save beforehand
- Defend when low, heal when safe

---

## Item Guide

### Weapon Tiers
1. **Rusty Sword** (5 dmg): Starting weapon
2. **Iron Sword** (12 dmg): Early upgrade
3. **Steel Sword** (20 dmg): Mid game standard
4. **Silver Rapier** (28 dmg): Mid-late game
5. **Dragon Slayer** (45 dmg): Late game
6. **Excalibur** (80 dmg): Legendary

### Armor Tiers
1. **Cloth** (+3 def): Starting
2. **Leather** (+8 def): Early game
3. **Chain Mail** (+15 def): Mid game
4. **Plate** (+25 def): Late game
5. **Dragon Scale** (+40 def): Endgame

### Best Accessories
- **Phoenix Pendant**: Legendary, all stats
- **Crown of Wisdom**: +20 INT, best for mages
- **Ring of Haste**: +15 AGI, best for rogues
- **Amulet of Protection**: +15 DEF, best for tanks

### Potion Economy
- **Small** (20g): 50 HP - Best early game
- **Medium** (50g): 100 HP - Mid game standard
- **Large** (100g): 200 HP - Late game
- **Supreme** (250g): Full HP - Bosses only

### Must-Have Items
1. Phoenix Down (revive) - For mistakes
2. Health Potion Supreme - For bosses
3. Elixir of Vitality - Permanent stats
4. Best weapon for your level
5. Best armor for your level

---

## Achievement Guide

### Easy Achievements
- **First Blood**: Defeat 1 enemy
- **Explorer**: Visit 5 locations
- **Level 5**: Reach level 5
- **Collector**: Own 20 items

### Medium Achievements
- **Monster Slayer**: Defeat 10 enemies
- **Treasure Hunter**: Find 10 treasures
- **Quest Starter**: Complete 5 quests
- **Crafter**: Craft 10 items

### Hard Achievements
- **Legendary Slayer**: Defeat 100 enemies
- **World Traveler**: Visit all locations
- **Dragon Slayer**: Defeat Ancient Dragon
- **Master Crafter**: Discover all recipes

### Very Hard Achievements
- **Boss Hunter**: Defeat all bosses
- **Quest Master**: Complete all quests
- **Lich Vanquisher**: Defeat Lich King
- **Legendary Hero**: Reach level 20

### Secret Achievements
- **The Beginning**: Hidden condition
- **Speed Runner**: Time-based challenge
- **Deathless**: No deaths (hardest achievement)
- **True Hero**: Complete everything

---

## Frequently Asked Questions

### Q: What's the best class?
**A**: Mage for progression, Warrior for beginners, Rogue for fun.

### Q: How do I beat the Dragon?
**A**: Level 15+, Dragon Slayer weapon, Plate Armor, 10+ Supreme Potions, Defend when below 50% HP.

### Q: Where do I get Dragon Scales?
**A**: Dragon's Lair treasures and Wyvern/Dragon enemy drops.

### Q: Can I respec stats?
**A**: No, choose carefully or start new character.

### Q: What's the level cap?
**A**: No hard cap, but content goes to level 20.

### Q: Can I miss quests?
**A**: No, all quests remain available.

### Q: Do treasures respawn?
**A**: No, one-time collection only.

### Q: What's the fastest way to level?
**A**: High intelligence + quest completion + appropriate level enemies.

### Q: Should I craft or buy?
**A**: Buy early game, craft late game (cheaper for expensive items).

### Q: How do I save?
**A**: Main menu > Save Game, enter save name.

### Q: Can I transfer saves?
**A**: Yes, copy files from saves/ directory.

### Q: Is there New Game Plus?
**A**: Not yet, future feature.

---

## Quick Reference

### Stat Priorities by Goal
- **Tank**: HP > DEF > STR
- **Damage**: STR > LUCK > AGI
- **Dodge**: AGI > LUCK > STR
- **Loot**: LUCK > INT > AGI
- **XP**: INT > LUCK > STR

### Gold Priorities
1. Health Potions (always)
2. Weapon upgrade (if 2+ tiers behind)
3. Armor upgrade (if 2+ tiers behind)
4. Accessories (late game)
5. Save remainder (1000g minimum)

### Level Progression Guide
- **Levels 1-5**: Meadow, Forest Path
- **Levels 6-10**: Dark Forest, Port Area, Mountains
- **Levels 11-15**: Snowy Peaks, Crystal Cavern
- **Levels 16-20**: Dragon's Lair, Cursed Castle

---

*Good luck, Hero! May your blade stay sharp and your potions plentiful!*
