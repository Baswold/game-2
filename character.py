"""
Character module - Manages player character stats, leveling, and progression.
"""

import math
from typing import Dict, Optional


class Character:
    """
    Represents the player character with stats, level, experience, and equipment.
    """

    def __init__(self, name: str = "Hero"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

        # Base stats
        self.base_stats = {
            'max_hp': 100,
            'hp': 100,
            'strength': 10,
            'defense': 10,
            'agility': 10,
            'intelligence': 10,
            'luck': 10
        }

        # Equipment bonuses
        self.equipment_bonuses = {
            'max_hp': 0,
            'strength': 0,
            'defense': 0,
            'agility': 0,
            'intelligence': 0,
            'luck': 0
        }

        # Equipped items
        self.equipped = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }

        # Status
        self.is_alive = True
        self.gold = 50
        self.stat_points = 5  # Starting points to allocate

    def get_stat(self, stat_name: str) -> int:
        """Get total stat value including equipment bonuses."""
        base = self.base_stats.get(stat_name, 0)
        bonus = self.equipment_bonuses.get(stat_name, 0)
        return base + bonus

    def get_max_hp(self) -> int:
        """Get maximum HP including equipment bonuses."""
        return self.get_stat('max_hp')

    def get_current_hp(self) -> int:
        """Get current HP."""
        return self.base_stats['hp']

    def heal(self, amount: int) -> int:
        """
        Heal the character by the specified amount.
        Returns the actual amount healed.
        """
        old_hp = self.base_stats['hp']
        max_hp = self.get_max_hp()
        self.base_stats['hp'] = min(max_hp, self.base_stats['hp'] + amount)
        actual_healed = self.base_stats['hp'] - old_hp
        return actual_healed

    def take_damage(self, damage: int) -> int:
        """
        Take damage, applying defense reduction.
        Returns the actual damage taken.
        """
        # Calculate damage reduction from defense
        defense = self.get_stat('defense')
        damage_reduction = defense * 0.5
        actual_damage = max(1, int(damage - damage_reduction))

        self.base_stats['hp'] -= actual_damage

        if self.base_stats['hp'] <= 0:
            self.base_stats['hp'] = 0
            self.is_alive = False

        return actual_damage

    def is_dead(self) -> bool:
        """Check if character is dead."""
        return not self.is_alive or self.base_stats['hp'] <= 0

    def revive(self, hp_percentage: float = 0.5):
        """Revive the character with a percentage of max HP."""
        if not self.is_alive:
            self.is_alive = True
            max_hp = self.get_max_hp()
            self.base_stats['hp'] = int(max_hp * hp_percentage)

    def add_xp(self, amount: int) -> bool:
        """
        Add experience points. Returns True if leveled up.
        """
        # Intelligence bonus to XP gain
        intel_bonus = 1.0 + (self.get_stat('intelligence') * 0.01)
        actual_xp = int(amount * intel_bonus)

        self.xp += actual_xp

        if self.xp >= self.xp_to_next_level:
            return self.level_up()
        return False

    def level_up(self) -> bool:
        """
        Level up the character and grant stat points.
        Returns True if successful.
        """
        if self.xp < self.xp_to_next_level:
            return False

        self.level += 1
        self.xp -= self.xp_to_next_level

        # Calculate next level XP requirement (exponential growth)
        self.xp_to_next_level = int(100 * math.pow(1.5, self.level - 1))

        # Grant stat points (more points at higher levels)
        points_gained = 3 + (self.level // 5)
        self.stat_points += points_gained

        # Restore HP on level up
        old_max = self.get_max_hp()
        self.base_stats['max_hp'] += 10
        hp_increase = self.get_max_hp() - old_max
        self.base_stats['hp'] = self.get_max_hp()

        return True

    def allocate_stat(self, stat_name: str, points: int = 1) -> bool:
        """
        Allocate stat points to a specific stat.
        Returns True if successful.
        """
        if stat_name not in self.base_stats:
            return False

        if stat_name == 'hp':
            return False  # Can't directly allocate to HP

        if points > self.stat_points:
            return False

        if stat_name == 'max_hp':
            self.base_stats['max_hp'] += points * 5
            self.base_stats['hp'] += points * 5
        else:
            self.base_stats[stat_name] += points

        self.stat_points -= points
        return True

    def equip_item(self, item, slot: str) -> Optional[object]:
        """
        Equip an item in the specified slot.
        Returns previously equipped item if any.
        """
        if slot not in self.equipped:
            return None

        # Unequip current item
        old_item = self.equipped[slot]
        if old_item:
            self.unequip_item(slot)

        # Equip new item
        self.equipped[slot] = item

        # Apply equipment bonuses
        if hasattr(item, 'stats'):
            for stat, value in item.stats.items():
                if stat in self.equipment_bonuses:
                    self.equipment_bonuses[stat] += value

                    # If max_hp increased, also increase current HP
                    if stat == 'max_hp':
                        self.base_stats['hp'] += value

        return old_item

    def unequip_item(self, slot: str) -> Optional[object]:
        """
        Unequip item from the specified slot.
        Returns the unequipped item if any.
        """
        if slot not in self.equipped or not self.equipped[slot]:
            return None

        item = self.equipped[slot]

        # Remove equipment bonuses
        if hasattr(item, 'stats'):
            for stat, value in item.stats.items():
                if stat in self.equipment_bonuses:
                    self.equipment_bonuses[stat] -= value

                    # Adjust current HP if max_hp changed
                    if stat == 'max_hp':
                        max_hp = self.get_max_hp()
                        self.base_stats['hp'] = min(self.base_stats['hp'], max_hp)

        self.equipped[slot] = None
        return item

    def get_attack_damage(self) -> int:
        """Calculate attack damage based on strength and weapon."""
        base_damage = self.get_stat('strength') * 2
        weapon = self.equipped.get('weapon')

        if weapon and hasattr(weapon, 'damage'):
            base_damage += weapon.damage

        return base_damage

    def get_dodge_chance(self) -> float:
        """Calculate chance to dodge attacks based on agility."""
        agility = self.get_stat('agility')
        # 1% dodge per agility point, capped at 50%
        return min(0.5, agility * 0.01)

    def get_crit_chance(self) -> float:
        """Calculate critical hit chance based on luck."""
        luck = self.get_stat('luck')
        # 0.5% crit per luck point, capped at 50%
        return min(0.5, luck * 0.005)

    def add_gold(self, amount: int):
        """Add gold to character."""
        self.gold += amount

    def remove_gold(self, amount: int) -> bool:
        """
        Remove gold from character.
        Returns True if successful (had enough gold).
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def get_info(self) -> Dict:
        """Get character information as a dictionary."""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level,
            'hp': self.base_stats['hp'],
            'max_hp': self.get_max_hp(),
            'strength': self.get_stat('strength'),
            'defense': self.get_stat('defense'),
            'agility': self.get_stat('agility'),
            'intelligence': self.get_stat('intelligence'),
            'luck': self.get_stat('luck'),
            'gold': self.gold,
            'stat_points': self.stat_points,
            'equipped_weapon': self.equipped['weapon'].name if self.equipped['weapon'] else 'None',
            'equipped_armor': self.equipped['armor'].name if self.equipped['armor'] else 'None',
            'equipped_accessory': self.equipped['accessory'].name if self.equipped['accessory'] else 'None',
        }

    def display_stats(self) -> str:
        """Get formatted string of character stats."""
        info = self.get_info()
        output = []
        output.append(f"\n{'='*50}")
        output.append(f"CHARACTER: {info['name']}")
        output.append(f"{'='*50}")
        output.append(f"Level: {info['level']} | XP: {info['xp']}/{info['xp_to_next_level']}")
        output.append(f"Gold: {info['gold']}g | Stat Points: {info['stat_points']}")
        output.append(f"\nVital Stats:")
        output.append(f"  HP: {info['hp']}/{info['max_hp']}")
        output.append(f"\nCombat Stats:")
        output.append(f"  Strength:     {info['strength']}")
        output.append(f"  Defense:      {info['defense']}")
        output.append(f"  Agility:      {info['agility']}")
        output.append(f"  Intelligence: {info['intelligence']}")
        output.append(f"  Luck:         {info['luck']}")
        output.append(f"\nEquipment:")
        output.append(f"  Weapon:    {info['equipped_weapon']}")
        output.append(f"  Armor:     {info['equipped_armor']}")
        output.append(f"  Accessory: {info['equipped_accessory']}")
        output.append(f"{'='*50}\n")

        return '\n'.join(output)

    def to_dict(self) -> Dict:
        """Convert character to dictionary for saving."""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level,
            'base_stats': self.base_stats.copy(),
            'equipment_bonuses': self.equipment_bonuses.copy(),
            'equipped': {
                'weapon': self.equipped['weapon'].to_dict() if self.equipped['weapon'] else None,
                'armor': self.equipped['armor'].to_dict() if self.equipped['armor'] else None,
                'accessory': self.equipped['accessory'].to_dict() if self.equipped['accessory'] else None,
            },
            'is_alive': self.is_alive,
            'gold': self.gold,
            'stat_points': self.stat_points
        }

    @staticmethod
    def from_dict(data: Dict, items_dict: Dict = None) -> 'Character':
        """Create character from dictionary."""
        char = Character(data['name'])
        char.level = data['level']
        char.xp = data['xp']
        char.xp_to_next_level = data['xp_to_next_level']
        char.base_stats = data['base_stats'].copy()
        char.equipment_bonuses = data['equipment_bonuses'].copy()
        char.is_alive = data['is_alive']
        char.gold = data['gold']
        char.stat_points = data['stat_points']

        # Equipment will be restored by inventory system

        return char
