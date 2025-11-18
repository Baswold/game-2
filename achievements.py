"""
Achievements module - Tracks player accomplishments and milestones.
"""

from typing import Dict, List, Optional, Set
from enum import Enum
from datetime import datetime


class AchievementCategory(Enum):
    """Categories of achievements."""
    COMBAT = "combat"
    EXPLORATION = "exploration"
    COLLECTION = "collection"
    PROGRESSION = "progression"
    SPECIAL = "special"
    SECRET = "secret"


class AchievementRarity(Enum):
    """Rarity of achievements."""
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class Achievement:
    """
    Represents an achievement that can be unlocked.
    """

    def __init__(self, achievement_id: str, name: str, description: str,
                 category: AchievementCategory, rarity: AchievementRarity,
                 points: int = 10, secret: bool = False,
                 reward_gold: int = 0, reward_xp: int = 0,
                 reward_items: List[str] = None):
        self.achievement_id = achievement_id
        self.name = name
        self.description = description
        self.category = category
        self.rarity = rarity
        self.points = points
        self.secret = secret  # Hidden until unlocked
        self.reward_gold = reward_gold
        self.reward_xp = reward_xp
        self.reward_items = reward_items or []
        self.unlocked = False
        self.unlock_date = None
        self.progress = 0
        self.progress_max = 1

    def unlock(self) -> bool:
        """
        Unlock the achievement.
        Returns True if newly unlocked.
        """
        if self.unlocked:
            return False

        self.unlocked = True
        self.unlock_date = datetime.now()
        return True

    def get_display_name(self) -> str:
        """Get display name (hidden if secret and locked)."""
        if self.secret and not self.unlocked:
            return "???"
        return self.name

    def get_display_description(self) -> str:
        """Get display description (hidden if secret and locked)."""
        if self.secret and not self.unlocked:
            return "Secret Achievement - Keep exploring to discover!"
        return self.description

    def update_progress(self, amount: int = 1):
        """Update achievement progress."""
        if self.unlocked:
            return

        self.progress = min(self.progress_max, self.progress + amount)

        if self.progress >= self.progress_max:
            self.unlock()

    def get_progress_string(self) -> str:
        """Get progress as string."""
        if self.progress_max == 1:
            return "✓" if self.unlocked else "○"
        return f"{self.progress}/{self.progress_max}"

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        return {
            'achievement_id': self.achievement_id,
            'unlocked': self.unlocked,
            'unlock_date': self.unlock_date.isoformat() if self.unlock_date else None,
            'progress': self.progress
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.unlocked = data.get('unlocked', False)
        unlock_date_str = data.get('unlock_date')
        if unlock_date_str:
            self.unlock_date = datetime.fromisoformat(unlock_date_str)
        self.progress = data.get('progress', 0)


class AchievementManager:
    """
    Manages all achievements in the game.
    """

    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.unlocked_achievements: Set[str] = set()
        self.total_points = 0

    def register_achievement(self, achievement: Achievement):
        """Register an achievement."""
        self.achievements[achievement.achievement_id] = achievement

    def unlock_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """
        Unlock an achievement.
        Returns the achievement if newly unlocked, None otherwise.
        """
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return None

        if achievement.unlock():
            self.unlocked_achievements.add(achievement_id)
            self.total_points += achievement.points
            return achievement

        return None

    def check_and_unlock(self, achievement_id: str, condition: bool) -> Optional[Achievement]:
        """
        Check a condition and unlock if true.
        Returns achievement if unlocked.
        """
        if condition:
            return self.unlock_achievement(achievement_id)
        return None

    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get an achievement by ID."""
        return self.achievements.get(achievement_id)

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get all unlocked achievements."""
        return [a for a in self.achievements.values() if a.unlocked]

    def get_locked_achievements(self) -> List[Achievement]:
        """Get all locked achievements."""
        return [a for a in self.achievements.values() if not a.unlocked]

    def get_achievements_by_category(self, category: AchievementCategory) -> List[Achievement]:
        """Get all achievements in a category."""
        return [a for a in self.achievements.values() if a.category == category]

    def get_completion_percentage(self) -> float:
        """Get percentage of achievements unlocked."""
        if not self.achievements:
            return 0.0
        return (len(self.unlocked_achievements) / len(self.achievements)) * 100

    def display_achievements(self, show_locked: bool = True) -> str:
        """Display all achievements."""
        output = []
        output.append("\n" + "="*70)
        output.append("ACHIEVEMENTS")
        output.append("="*70)
        output.append(f"Unlocked: {len(self.unlocked_achievements)}/{len(self.achievements)} "
                      f"({self.get_completion_percentage():.1f}%)")
        output.append(f"Total Points: {self.total_points}")
        output.append("="*70)

        # Group by category
        for category in AchievementCategory:
            achievements = self.get_achievements_by_category(category)
            if not achievements:
                continue

            output.append(f"\n[{category.value.upper()}]")

            for achievement in achievements:
                if not show_locked and not achievement.unlocked:
                    continue

                status = "🏆" if achievement.unlocked else "○"
                rarity_symbol = self._get_rarity_symbol(achievement.rarity)

                output.append(f"  {status} {rarity_symbol} {achievement.get_display_name()} "
                              f"({achievement.points} pts)")
                output.append(f"      {achievement.get_display_description()}")

                if achievement.unlocked and achievement.unlock_date:
                    date_str = achievement.unlock_date.strftime("%Y-%m-%d")
                    output.append(f"      Unlocked: {date_str}")

        output.append("\n" + "="*70)
        return '\n'.join(output)

    def _get_rarity_symbol(self, rarity: AchievementRarity) -> str:
        """Get symbol for achievement rarity."""
        symbols = {
            AchievementRarity.COMMON: "○",
            AchievementRarity.UNCOMMON: "◆",
            AchievementRarity.RARE: "★",
            AchievementRarity.EPIC: "♦",
            AchievementRarity.LEGENDARY: "♛"
        }
        return symbols.get(rarity, "•")

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        achievements_data = {}
        for ach_id, ach in self.achievements.items():
            if ach.unlocked:
                achievements_data[ach_id] = ach.to_dict()

        return {
            'unlocked_achievements': list(self.unlocked_achievements),
            'total_points': self.total_points,
            'achievements': achievements_data
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.unlocked_achievements = set(data.get('unlocked_achievements', []))
        self.total_points = data.get('total_points', 0)

        achievements_data = data.get('achievements', {})
        for ach_id, ach_data in achievements_data.items():
            if ach_id in self.achievements:
                self.achievements[ach_id].from_dict(ach_data)


# =============================================================================
# ACHIEVEMENT DEFINITIONS
# =============================================================================

def create_achievement_manager() -> AchievementManager:
    """Create and populate the achievement manager."""
    manager = AchievementManager()

    # === COMBAT ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "first_blood", "First Blood",
        "Defeat your first enemy",
        AchievementCategory.COMBAT, AchievementRarity.COMMON,
        points=5, reward_gold=50
    ))

    manager.register_achievement(Achievement(
        "slayer_10", "Monster Slayer",
        "Defeat 10 enemies",
        AchievementCategory.COMBAT, AchievementRarity.COMMON,
        points=10, reward_gold=100
    ))

    manager.register_achievement(Achievement(
        "slayer_50", "Veteran Warrior",
        "Defeat 50 enemies",
        AchievementCategory.COMBAT, AchievementRarity.UNCOMMON,
        points=20, reward_gold=500
    ))

    manager.register_achievement(Achievement(
        "slayer_100", "Legendary Slayer",
        "Defeat 100 enemies",
        AchievementCategory.COMBAT, AchievementRarity.RARE,
        points=50, reward_gold=1000, reward_items=['phoenix_down']
    ))

    manager.register_achievement(Achievement(
        "boss_hunter", "Boss Hunter",
        "Defeat all boss enemies",
        AchievementCategory.COMBAT, AchievementRarity.EPIC,
        points=100, reward_gold=5000, reward_items=['crown_wisdom']
    ))

    manager.register_achievement(Achievement(
        "flawless_victory", "Flawless Victory",
        "Win a battle without taking damage",
        AchievementCategory.COMBAT, AchievementRarity.RARE,
        points=30, reward_gold=500
    ))

    manager.register_achievement(Achievement(
        "critical_master", "Critical Master",
        "Land 20 critical hits",
        AchievementCategory.COMBAT, AchievementRarity.UNCOMMON,
        points=15, reward_gold=300
    ))

    manager.register_achievement(Achievement(
        "dragon_slayer_ach", "Dragon Slayer",
        "Defeat the Ancient Dragon",
        AchievementCategory.COMBAT, AchievementRarity.EPIC,
        points=75, reward_gold=3000, reward_xp=500
    ))

    manager.register_achievement(Achievement(
        "lich_vanquisher", "Lich Vanquisher",
        "Defeat the Lich King",
        AchievementCategory.COMBAT, AchievementRarity.LEGENDARY,
        points=150, reward_gold=10000, reward_items=['star_fragment', 'elixir_vitality']
    ))

    # === EXPLORATION ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "explorer", "Explorer",
        "Visit 5 different locations",
        AchievementCategory.EXPLORATION, AchievementRarity.COMMON,
        points=10, reward_gold=100
    ))

    manager.register_achievement(Achievement(
        "world_traveler", "World Traveler",
        "Visit all locations",
        AchievementCategory.EXPLORATION, AchievementRarity.RARE,
        points=40, reward_gold=1000, reward_items=['ring_haste']
    ))

    manager.register_achievement(Achievement(
        "treasure_hunter", "Treasure Hunter",
        "Find 10 treasures",
        AchievementCategory.EXPLORATION, AchievementRarity.UNCOMMON,
        points=15, reward_gold=500
    ))

    manager.register_achievement(Achievement(
        "master_explorer", "Master Explorer",
        "Find all treasures in the game",
        AchievementCategory.EXPLORATION, AchievementRarity.EPIC,
        points=80, reward_gold=5000, reward_items=['pendant_phoenix']
    ))

    # === COLLECTION ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "collector", "Collector",
        "Own 20 different items",
        AchievementCategory.COLLECTION, AchievementRarity.COMMON,
        points=10, reward_gold=200
    ))

    manager.register_achievement(Achievement(
        "hoarder", "Hoarder",
        "Own 50 different items",
        AchievementCategory.COLLECTION, AchievementRarity.UNCOMMON,
        points=25, reward_gold=1000
    ))

    manager.register_achievement(Achievement(
        "legendary_gear", "Legendary Armory",
        "Obtain a legendary item",
        AchievementCategory.COLLECTION, AchievementRarity.RARE,
        points=50, reward_gold=2000
    ))

    manager.register_achievement(Achievement(
        "full_set", "Complete Arsenal",
        "Own all weapon types",
        AchievementCategory.COLLECTION, AchievementRarity.UNCOMMON,
        points=30, reward_gold=1500
    ))

    manager.register_achievement(Achievement(
        "wealthy", "Wealthy",
        "Accumulate 10,000 gold",
        AchievementCategory.COLLECTION, AchievementRarity.RARE,
        points=40, reward_xp=500
    ))

    manager.register_achievement(Achievement(
        "millionaire", "Millionaire",
        "Accumulate 100,000 gold",
        AchievementCategory.COLLECTION, AchievementRarity.EPIC,
        points=100, reward_items=['excalibur']
    ))

    # === PROGRESSION ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "level_5", "Apprentice",
        "Reach level 5",
        AchievementCategory.PROGRESSION, AchievementRarity.COMMON,
        points=10, reward_gold=200
    ))

    manager.register_achievement(Achievement(
        "level_10", "Journeyman",
        "Reach level 10",
        AchievementCategory.PROGRESSION, AchievementRarity.UNCOMMON,
        points=25, reward_gold=500, reward_items=['health_potion_large']
    ))

    manager.register_achievement(Achievement(
        "level_15", "Master",
        "Reach level 15",
        AchievementCategory.PROGRESSION, AchievementRarity.RARE,
        points=50, reward_gold=1000, reward_items=['phoenix_down']
    ))

    manager.register_achievement(Achievement(
        "level_20", "Legendary Hero",
        "Reach level 20",
        AchievementCategory.PROGRESSION, AchievementRarity.EPIC,
        points=100, reward_gold=5000, reward_items=['celestial_robe']
    ))

    manager.register_achievement(Achievement(
        "quest_complete_5", "Quest Starter",
        "Complete 5 quests",
        AchievementCategory.PROGRESSION, AchievementRarity.COMMON,
        points=10, reward_gold=200
    ))

    manager.register_achievement(Achievement(
        "quest_complete_all", "Quest Master",
        "Complete all quests",
        AchievementCategory.PROGRESSION, AchievementRarity.EPIC,
        points=100, reward_gold=5000, reward_xp=1000
    ))

    manager.register_achievement(Achievement(
        "crafter", "Crafter",
        "Craft 10 items",
        AchievementCategory.PROGRESSION, AchievementRarity.UNCOMMON,
        points=20, reward_gold=500
    ))

    manager.register_achievement(Achievement(
        "master_crafter", "Master Crafter",
        "Discover all recipes",
        AchievementCategory.PROGRESSION, AchievementRarity.RARE,
        points=50, reward_gold=2000
    ))

    # === SPECIAL ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "survivor", "Survivor",
        "Survive 100 battles",
        AchievementCategory.SPECIAL, AchievementRarity.RARE,
        points=40, reward_items=['elixir_vitality']
    ))

    manager.register_achievement(Achievement(
        "speed_runner", "Speed Runner",
        "Complete the game in under 50 battles",
        AchievementCategory.SPECIAL, AchievementRarity.EPIC,
        points=80, secret=True, reward_gold=10000
    ))

    manager.register_achievement(Achievement(
        "pacifist", "Pacifist Route",
        "Complete 10 quests without killing enemies",
        AchievementCategory.SPECIAL, AchievementRarity.RARE,
        points=50, secret=True, reward_items=['staff_mage']
    ))

    manager.register_achievement(Achievement(
        "no_death", "Deathless",
        "Complete the game without dying",
        AchievementCategory.SPECIAL, AchievementRarity.LEGENDARY,
        points=200, secret=True, reward_gold=50000,
        reward_items=['excalibur', 'dragon_armor', 'pendant_phoenix']
    ))

    manager.register_achievement(Achievement(
        "lucky_seven", "Lucky Seven",
        "Win 7 battles in a row by critical hits",
        AchievementCategory.SPECIAL, AchievementRarity.RARE,
        points=35, secret=True, reward_items=['bronze_ring']
    ))

    manager.register_achievement(Achievement(
        "merchant", "Master Merchant",
        "Buy and sell 100 items",
        AchievementCategory.SPECIAL, AchievementRarity.UNCOMMON,
        points=25, reward_gold=1000
    ))

    # === SECRET ACHIEVEMENTS ===

    manager.register_achievement(Achievement(
        "secret_1", "The Beginning",
        "Start your first game",
        AchievementCategory.SECRET, AchievementRarity.COMMON,
        points=5, secret=True
    ))

    manager.register_achievement(Achievement(
        "secret_2", "Persistent",
        "Load a save game 10 times",
        AchievementCategory.SECRET, AchievementRarity.UNCOMMON,
        points=10, secret=True, reward_gold=100
    ))

    manager.register_achievement(Achievement(
        "secret_3", "True Hero",
        "Complete every achievement",
        AchievementCategory.SECRET, AchievementRarity.LEGENDARY,
        points=500, secret=True, reward_gold=100000,
        reward_items=['star_fragment', 'star_fragment', 'star_fragment']
    ))

    return manager
