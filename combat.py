"""
Combat module - Handles turn-based combat, enemies, and battle mechanics.
"""

import random
from typing import Dict, List, Optional, Tuple
from enum import Enum


class EnemyType(Enum):
    """Types of enemies."""
    BEAST = "beast"
    HUMANOID = "humanoid"
    UNDEAD = "undead"
    DRAGON = "dragon"
    DEMON = "demon"


class Enemy:
    """
    Represents an enemy in combat.
    """

    def __init__(self, enemy_id: str, name: str, level: int,
                 hp: int, strength: int, defense: int, agility: int,
                 xp_reward: int, gold_reward: int, enemy_type: EnemyType,
                 loot_table: Dict[str, float] = None):
        self.enemy_id = enemy_id
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.enemy_type = enemy_type
        self.loot_table = loot_table or {}  # item_id -> drop_chance (0.0-1.0)

    def take_damage(self, damage: int) -> int:
        """
        Take damage with defense reduction.
        Returns actual damage taken.
        """
        damage_reduction = self.defense * 0.5
        actual_damage = max(1, int(damage - damage_reduction))
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def is_alive(self) -> bool:
        """Check if enemy is alive."""
        return self.hp > 0

    def get_attack_damage(self) -> int:
        """Calculate enemy's attack damage."""
        base_damage = self.strength * 2
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)

    def get_loot(self) -> List[str]:
        """
        Generate loot drops based on loot table.
        Returns list of item IDs.
        """
        loot = []
        for item_id, drop_chance in self.loot_table.items():
            if random.random() < drop_chance:
                loot.append(item_id)
        return loot

    def __str__(self) -> str:
        return f"{self.name} (Lv.{self.level}) - HP: {self.hp}/{self.max_hp}"


class CombatAction(Enum):
    """Combat action types."""
    ATTACK = "attack"
    DEFEND = "defend"
    USE_ITEM = "use_item"
    FLEE = "flee"


class CombatResult(Enum):
    """Combat result states."""
    ONGOING = "ongoing"
    VICTORY = "victory"
    DEFEAT = "defeat"
    FLED = "fled"


class Combat:
    """
    Manages a combat encounter.
    """

    def __init__(self, character, enemy: Enemy):
        self.character = character
        self.enemy = enemy
        self.turn_count = 0
        self.result = CombatResult.ONGOING
        self.combat_log = []
        self.is_defending = False
        self.flee_attempts = 0

    def log(self, message: str):
        """Add message to combat log."""
        self.combat_log.append(message)

    def get_turn_order(self) -> List[str]:
        """
        Determine turn order based on agility.
        Returns list with 'player' and 'enemy'.
        """
        player_agility = self.character.get_stat('agility')
        enemy_agility = self.enemy.agility

        # Add some randomness
        player_roll = player_agility + random.randint(0, 10)
        enemy_roll = enemy_agility + random.randint(0, 10)

        if player_roll >= enemy_roll:
            return ['player', 'enemy']
        else:
            return ['enemy', 'player']

    def player_attack(self) -> str:
        """
        Execute player attack.
        Returns message describing the attack.
        """
        # Calculate damage
        base_damage = self.character.get_attack_damage()

        # Check for critical hit
        crit_chance = self.character.get_crit_chance()
        is_crit = random.random() < crit_chance

        if is_crit:
            damage = int(base_damage * 1.5)
            damage_dealt = self.enemy.take_damage(damage)
            self.log(f"💥 CRITICAL HIT! You deal {damage_dealt} damage to {self.enemy.name}!")
            return f"💥 CRITICAL HIT! You deal {damage_dealt} damage!"
        else:
            damage_dealt = self.enemy.take_damage(base_damage)
            self.log(f"You attack {self.enemy.name} for {damage_dealt} damage.")
            return f"You deal {damage_dealt} damage!"

    def enemy_attack(self) -> str:
        """
        Execute enemy attack.
        Returns message describing the attack.
        """
        # Check if player dodges
        dodge_chance = self.character.get_dodge_chance()
        if random.random() < dodge_chance:
            self.log(f"You dodge {self.enemy.name}'s attack!")
            return "You dodged the attack!"

        # Calculate damage
        damage = self.enemy.get_attack_damage()

        # Reduce damage if defending
        if self.is_defending:
            damage = int(damage * 0.5)
            self.is_defending = False
            self.log(f"{self.enemy.name} attacks! Your defense reduces damage.")

        damage_taken = self.character.take_damage(damage)
        self.log(f"{self.enemy.name} attacks you for {damage_taken} damage!")

        return f"{self.enemy.name} deals {damage_taken} damage!"

    def player_defend(self) -> str:
        """
        Player takes defensive stance.
        Returns message.
        """
        self.is_defending = True
        self.log("You take a defensive stance.")
        return "You brace for the next attack!"

    def player_use_item(self, item) -> Tuple[bool, str]:
        """
        Player uses an item.
        Returns (success, message).
        """
        if not item:
            return False, "No item selected."

        # Use the item
        from items import ItemType
        if item.item_type == ItemType.CONSUMABLE:
            effect_msg = item.use(self.character)
            self.log(f"You use {item.name}. {effect_msg}")
            return True, effect_msg
        else:
            return False, "Cannot use that item in combat."

    def attempt_flee(self) -> Tuple[bool, str]:
        """
        Attempt to flee from combat.
        Returns (success, message).
        """
        self.flee_attempts += 1

        # Base flee chance 50%, decreases with each attempt
        flee_chance = 0.5 - (self.flee_attempts * 0.1)

        # Agility increases flee chance
        player_agility = self.character.get_stat('agility')
        agility_bonus = player_agility * 0.01
        flee_chance += agility_bonus

        # Enemy level affects flee difficulty
        level_difference = self.enemy.level - self.character.level
        flee_chance -= level_difference * 0.05

        # Clamp between 10% and 90%
        flee_chance = max(0.1, min(0.9, flee_chance))

        if random.random() < flee_chance:
            self.result = CombatResult.FLED
            self.log("You successfully fled from combat!")
            return True, "You escaped!"
        else:
            self.log("Failed to flee!")
            return False, "Couldn't escape!"

    def execute_turn(self, player_action: CombatAction,
                     item=None) -> List[str]:
        """
        Execute a full combat turn.
        Returns list of messages for this turn.
        """
        turn_messages = []
        self.turn_count += 1

        # Determine turn order
        turn_order = self.get_turn_order()

        for actor in turn_order:
            # Check if combat ended
            if self.result != CombatResult.ONGOING:
                break

            if actor == 'player':
                # Execute player action
                if player_action == CombatAction.ATTACK:
                    msg = self.player_attack()
                    turn_messages.append(msg)
                elif player_action == CombatAction.DEFEND:
                    msg = self.player_defend()
                    turn_messages.append(msg)
                elif player_action == CombatAction.USE_ITEM:
                    success, msg = self.player_use_item(item)
                    turn_messages.append(msg)
                    if not success:
                        # Failed to use item, don't continue turn
                        return turn_messages
                elif player_action == CombatAction.FLEE:
                    success, msg = self.attempt_flee()
                    turn_messages.append(msg)
                    if success:
                        return turn_messages
                    # If flee failed, enemy still gets to attack

                # Check if enemy died
                if not self.enemy.is_alive():
                    self.result = CombatResult.VICTORY
                    break

            else:  # enemy turn
                msg = self.enemy_attack()
                turn_messages.append(msg)

                # Check if player died
                if self.character.is_dead():
                    self.result = CombatResult.DEFEAT
                    break

        return turn_messages

    def get_status(self) -> str:
        """Get current combat status display."""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"⚔️  COMBAT - Turn {self.turn_count}")
        output.append(f"{'='*60}")
        output.append(f"\n{self.enemy}")
        output.append(f"\nYour HP: {self.character.get_current_hp()}/{self.character.get_max_hp()}")
        output.append(f"{'='*60}\n")
        return '\n'.join(output)

    def get_rewards(self) -> Dict:
        """
        Get rewards from victory.
        Returns dict with xp, gold, and loot.
        """
        if self.result != CombatResult.VICTORY:
            return {'xp': 0, 'gold': 0, 'loot': []}

        # Base rewards
        xp = self.enemy.xp_reward
        gold = self.enemy.gold_reward

        # Luck bonus to gold
        luck = self.character.get_stat('luck')
        gold_bonus = int(gold * (luck * 0.01))
        gold += gold_bonus

        # Generate loot
        loot = self.enemy.get_loot()

        return {
            'xp': xp,
            'gold': gold,
            'loot': loot
        }


# =============================================================================
# ENEMY DATABASE
# =============================================================================

ENEMIES_DB = {}


def register_enemy(enemy: Enemy):
    """Register an enemy template."""
    ENEMIES_DB[enemy.enemy_id] = enemy


# Early game enemies (Level 1-3)
register_enemy(Enemy(
    "slime", "Slime", 1,
    hp=30, strength=5, defense=2, agility=3,
    xp_reward=10, gold_reward=5, enemy_type=EnemyType.BEAST,
    loot_table={'health_potion_small': 0.3, 'leather_scrap': 0.2}
))

register_enemy(Enemy(
    "goblin", "Goblin", 2,
    hp=50, strength=8, defense=5, agility=6,
    xp_reward=20, gold_reward=10, enemy_type=EnemyType.HUMANOID,
    loot_table={'health_potion_small': 0.4, 'iron_ore': 0.3, 'rusty_sword': 0.1}
))

register_enemy(Enemy(
    "wolf", "Wolf", 2,
    hp=45, strength=10, defense=3, agility=9,
    xp_reward=18, gold_reward=8, enemy_type=EnemyType.BEAST,
    loot_table={'health_potion_small': 0.3, 'leather_scrap': 0.5}
))

register_enemy(Enemy(
    "bandit", "Bandit", 3,
    hp=70, strength=12, defense=8, agility=7,
    xp_reward=30, gold_reward=20, enemy_type=EnemyType.HUMANOID,
    loot_table={'health_potion_medium': 0.3, 'iron_sword': 0.15, 'bronze_ring': 0.1}
))

# Mid game enemies (Level 4-7)
register_enemy(Enemy(
    "skeleton", "Skeleton Warrior", 5,
    hp=100, strength=15, defense=10, agility=8,
    xp_reward=50, gold_reward=30, enemy_type=EnemyType.UNDEAD,
    loot_table={'health_potion_medium': 0.4, 'steel_ingot': 0.3, 'steel_sword': 0.1}
))

register_enemy(Enemy(
    "orc", "Orc Brute", 6,
    hp=130, strength=20, defense=15, agility=5,
    xp_reward=70, gold_reward=40, enemy_type=EnemyType.HUMANOID,
    loot_table={'health_potion_large': 0.3, 'chain_mail': 0.1, 'iron_ore': 0.5}
))

register_enemy(Enemy(
    "dark_mage", "Dark Mage", 7,
    hp=90, strength=12, defense=8, agility=12,
    xp_reward=80, gold_reward=60, enemy_type=EnemyType.HUMANOID,
    loot_table={'health_potion_large': 0.4, 'staff_mage': 0.15, 'enchanted_crystal': 0.3}
))

register_enemy(Enemy(
    "troll", "Cave Troll", 8,
    hp=180, strength=25, defense=20, agility=4,
    xp_reward=100, gold_reward=50, enemy_type=EnemyType.HUMANOID,
    loot_table={'health_potion_large': 0.5, 'plate_armor': 0.1, 'steel_ingot': 0.4}
))

# High level enemies (Level 9-12)
register_enemy(Enemy(
    "vampire", "Vampire Lord", 10,
    hp=200, strength=30, defense=25, agility=15,
    xp_reward=150, gold_reward=100, enemy_type=EnemyType.UNDEAD,
    loot_table={'health_potion_supreme': 0.3, 'silver_rapier': 0.15, 'silver_ore': 0.5}
))

register_enemy(Enemy(
    "wyvern", "Wyvern", 11,
    hp=250, strength=35, defense=30, agility=18,
    xp_reward=200, gold_reward=120, enemy_type=EnemyType.DRAGON,
    loot_table={'health_potion_supreme': 0.4, 'dragon_scale': 0.6, 'dragon_armor': 0.05}
))

register_enemy(Enemy(
    "demon", "Lesser Demon", 12,
    hp=220, strength=40, defense=28, agility=20,
    xp_reward=250, gold_reward=150, enemy_type=EnemyType.DEMON,
    loot_table={
        'health_potion_supreme': 0.5,
        'phoenix_down': 0.2,
        'ring_strength': 0.1,
        'enchanted_crystal': 0.4
    }
))

# Boss enemies (Level 13+)
register_enemy(Enemy(
    "dragon", "Ancient Dragon", 15,
    hp=500, strength=50, defense=40, agility=25,
    xp_reward=500, gold_reward=500, enemy_type=EnemyType.DRAGON,
    loot_table={
        'dragon_slayer': 0.5,
        'dragon_armor': 0.4,
        'dragon_scale': 1.0,
        'health_potion_supreme': 0.8,
        'phoenix_down': 0.3
    }
))

register_enemy(Enemy(
    "goblin_chief", "Goblin Chief", 5,
    hp=120, strength=18, defense=12, agility=10,
    xp_reward=100, gold_reward=80, enemy_type=EnemyType.HUMANOID,
    loot_table={
        'health_potion_large': 0.6,
        'steel_sword': 0.3,
        'chain_mail': 0.2,
        'goblin_chief_head': 1.0  # Quest item
    }
))

register_enemy(Enemy(
    "lich", "Lich King", 18,
    hp=600, strength=45, defense=35, agility=30,
    xp_reward=1000, gold_reward=1000, enemy_type=EnemyType.UNDEAD,
    loot_table={
        'excalibur': 0.3,
        'celestial_robe': 0.3,
        'crown_wisdom': 0.4,
        'phoenix_down': 0.8,
        'star_fragment': 0.5
    }
))


def create_enemy(enemy_id: str) -> Optional[Enemy]:
    """
    Create a new enemy instance from template.
    """
    template = ENEMIES_DB.get(enemy_id)
    if not template:
        return None

    return Enemy(
        template.enemy_id,
        template.name,
        template.level,
        template.max_hp,
        template.strength,
        template.defense,
        template.agility,
        template.xp_reward,
        template.gold_reward,
        template.enemy_type,
        template.loot_table.copy()
    )


def get_random_enemy_for_level(level: int) -> Enemy:
    """
    Get a random enemy appropriate for character level.
    """
    # Get enemies within level range
    min_level = max(1, level - 1)
    max_level = level + 2

    appropriate_enemies = [
        e for e in ENEMIES_DB.values()
        if min_level <= e.level <= max_level
    ]

    if not appropriate_enemies:
        # Fallback to any enemy
        appropriate_enemies = list(ENEMIES_DB.values())

    template = random.choice(appropriate_enemies)
    return create_enemy(template.enemy_id)


def get_enemies_by_level(min_level: int, max_level: int) -> List[Enemy]:
    """Get all enemies within level range."""
    return [
        e for e in ENEMIES_DB.values()
        if min_level <= e.level <= max_level
    ]
