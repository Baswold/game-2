"""
Statistics module - Tracks detailed player statistics and records.
"""

from typing import Dict, List
from datetime import datetime, timedelta
from collections import defaultdict


class GameStatistics:
    """
    Tracks comprehensive game statistics.
    """

    def __init__(self):
        # Combat stats
        self.total_battles = 0
        self.battles_won = 0
        self.battles_fled = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.critical_hits = 0
        self.dodges = 0
        self.kills_by_enemy_type = defaultdict(int)
        self.deaths = 0
        self.flawless_victories = 0
        self.consecutive_wins = 0
        self.best_win_streak = 0

        # Exploration stats
        self.locations_visited = set()
        self.treasures_found = 0
        self.distance_traveled = 0  # Number of location transitions
        self.random_encounters = 0

        # Economy stats
        self.total_gold_earned = 0
        self.total_gold_spent = 0
        self.items_bought = 0
        self.items_sold = 0
        self.most_expensive_purchase = 0

        # Collection stats
        self.items_collected = set()
        self.unique_items_owned = 0
        self.items_crafted = 0
        self.recipes_discovered = 0

        # Progression stats
        self.quests_completed = 0
        self.quests_failed = 0
        self.total_xp_earned = 0
        self.highest_level_reached = 1
        self.stat_points_allocated = 0

        # Time stats
        self.game_start_time = datetime.now()
        self.total_play_time = timedelta(0)
        self.session_start_time = datetime.now()
        self.saves_created = 0
        self.loads_performed = 0

        # Achievements
        self.achievements_unlocked = 0

        # Records
        self.highest_damage_single_hit = 0
        self.fastest_battle_victory = None  # In turns
        self.longest_battle = None  # In turns
        self.highest_gold_owned = 0
        self.most_items_inventory = 0

    def record_battle_start(self):
        """Record start of battle."""
        self.total_battles += 1

    def record_battle_victory(self, turns: int, damage_dealt: int, damage_taken: int,
                               flawless: bool = False):
        """Record battle victory."""
        self.battles_won += 1
        self.total_damage_dealt += damage_dealt
        self.total_damage_taken += damage_taken

        if flawless:
            self.flawless_victories += 1

        self.consecutive_wins += 1
        self.best_win_streak = max(self.best_win_streak, self.consecutive_wins)

        # Update records
        if self.fastest_battle_victory is None or turns < self.fastest_battle_victory:
            self.fastest_battle_victory = turns

        if self.longest_battle is None or turns > self.longest_battle:
            self.longest_battle = turns

    def record_battle_defeat(self):
        """Record battle defeat."""
        self.deaths += 1
        self.consecutive_wins = 0

    def record_battle_fled(self):
        """Record fleeing from battle."""
        self.battles_fled += 1
        self.consecutive_wins = 0

    def record_enemy_killed(self, enemy_type: str):
        """Record enemy kill."""
        self.kills_by_enemy_type[enemy_type] += 1

    def record_damage_dealt(self, damage: int):
        """Record damage dealt."""
        self.highest_damage_single_hit = max(self.highest_damage_single_hit, damage)

    def record_critical_hit(self):
        """Record critical hit."""
        self.critical_hits += 1

    def record_dodge(self):
        """Record successful dodge."""
        self.dodges += 1

    def record_location_visit(self, location_id: str):
        """Record location visit."""
        if location_id not in self.locations_visited:
            self.locations_visited.add(location_id)

    def record_travel(self):
        """Record travel between locations."""
        self.distance_traveled += 1

    def record_random_encounter(self):
        """Record random encounter."""
        self.random_encounters += 1

    def record_treasure_found(self):
        """Record treasure found."""
        self.treasures_found += 1

    def record_gold_earned(self, amount: int):
        """Record gold earned."""
        self.total_gold_earned += amount

    def record_gold_spent(self, amount: int):
        """Record gold spent."""
        self.total_gold_spent += amount
        self.most_expensive_purchase = max(self.most_expensive_purchase, amount)

    def record_item_bought(self):
        """Record item purchase."""
        self.items_bought += 1

    def record_item_sold(self):
        """Record item sold."""
        self.items_sold += 1

    def record_item_collected(self, item_id: str):
        """Record item collected."""
        self.items_collected.add(item_id)
        self.unique_items_owned = len(self.items_collected)

    def record_item_crafted(self):
        """Record item crafted."""
        self.items_crafted += 1

    def record_recipe_discovered(self):
        """Record recipe discovered."""
        self.recipes_discovered += 1

    def record_quest_completed(self):
        """Record quest completed."""
        self.quests_completed += 1

    def record_quest_failed(self):
        """Record quest failed."""
        self.quests_failed += 1

    def record_xp_gained(self, amount: int):
        """Record XP gained."""
        self.total_xp_earned += amount

    def record_level_reached(self, level: int):
        """Record level reached."""
        self.highest_level_reached = max(self.highest_level_reached, level)

    def record_stat_allocated(self):
        """Record stat point allocation."""
        self.stat_points_allocated += 1

    def record_achievement_unlocked(self):
        """Record achievement unlocked."""
        self.achievements_unlocked += 1

    def record_save(self):
        """Record game saved."""
        self.saves_created += 1

    def record_load(self):
        """Record game loaded."""
        self.loads_performed += 1

    def update_gold_record(self, current_gold: int):
        """Update gold record."""
        self.highest_gold_owned = max(self.highest_gold_owned, current_gold)

    def update_inventory_record(self, current_items: int):
        """Update inventory record."""
        self.most_items_inventory = max(self.most_items_inventory, current_items)

    def update_session_time(self):
        """Update play time."""
        session_duration = datetime.now() - self.session_start_time
        self.total_play_time += session_duration
        self.session_start_time = datetime.now()

    def get_win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.total_battles == 0:
            return 0.0
        return (self.battles_won / self.total_battles) * 100

    def get_average_damage_per_battle(self) -> float:
        """Calculate average damage dealt per battle."""
        if self.battles_won == 0:
            return 0.0
        return self.total_damage_dealt / self.battles_won

    def get_survival_rate(self) -> float:
        """Calculate survival rate (battles without dying)."""
        if self.total_battles == 0:
            return 100.0
        return ((self.total_battles - self.deaths) / self.total_battles) * 100

    def get_critical_hit_rate(self) -> float:
        """Calculate critical hit rate."""
        if self.total_damage_dealt == 0:
            return 0.0
        # Estimate based on critical hits vs total attacks (rough estimate)
        estimated_attacks = self.battles_won * 3  # Assume avg 3 attacks per battle
        return (self.critical_hits / max(1, estimated_attacks)) * 100

    def display_statistics(self) -> str:
        """Display formatted statistics."""
        output = []
        output.append("\n" + "="*70)
        output.append("GAME STATISTICS")
        output.append("="*70)

        # Combat Statistics
        output.append("\n[COMBAT]")
        output.append(f"  Total Battles: {self.total_battles}")
        output.append(f"  Victories: {self.battles_won} | Defeats: {self.deaths} | "
                      f"Fled: {self.battles_fled}")
        output.append(f"  Win Rate: {self.get_win_rate():.1f}%")
        output.append(f"  Flawless Victories: {self.flawless_victories}")
        output.append(f"  Best Win Streak: {self.best_win_streak}")
        output.append(f"  Total Damage Dealt: {self.total_damage_dealt}")
        output.append(f"  Total Damage Taken: {self.total_damage_taken}")
        output.append(f"  Average Damage/Battle: {self.get_average_damage_per_battle():.1f}")
        output.append(f"  Critical Hits: {self.critical_hits}")
        output.append(f"  Successful Dodges: {self.dodges}")
        output.append(f"  Highest Damage (Single Hit): {self.highest_damage_single_hit}")

        if self.fastest_battle_victory:
            output.append(f"  Fastest Victory: {self.fastest_battle_victory} turns")

        # Top enemies killed
        if self.kills_by_enemy_type:
            top_kills = sorted(self.kills_by_enemy_type.items(),
                               key=lambda x: x[1], reverse=True)[:3]
            output.append(f"  Most Killed:")
            for enemy, count in top_kills:
                output.append(f"    • {enemy}: {count}")

        # Exploration Statistics
        output.append("\n[EXPLORATION]")
        output.append(f"  Locations Discovered: {len(self.locations_visited)}")
        output.append(f"  Distance Traveled: {self.distance_traveled} transitions")
        output.append(f"  Treasures Found: {self.treasures_found}")
        output.append(f"  Random Encounters: {self.random_encounters}")

        # Economy Statistics
        output.append("\n[ECONOMY]")
        output.append(f"  Gold Earned: {self.total_gold_earned}g")
        output.append(f"  Gold Spent: {self.total_gold_spent}g")
        output.append(f"  Net Gold: {self.total_gold_earned - self.total_gold_spent}g")
        output.append(f"  Highest Gold Owned: {self.highest_gold_owned}g")
        output.append(f"  Items Bought: {self.items_bought}")
        output.append(f"  Items Sold: {self.items_sold}")
        output.append(f"  Most Expensive Purchase: {self.most_expensive_purchase}g")

        # Collection Statistics
        output.append("\n[COLLECTION]")
        output.append(f"  Unique Items Collected: {self.unique_items_owned}")
        output.append(f"  Items Crafted: {self.items_crafted}")
        output.append(f"  Recipes Discovered: {self.recipes_discovered}")
        output.append(f"  Most Items in Inventory: {self.most_items_inventory}")

        # Progression Statistics
        output.append("\n[PROGRESSION]")
        output.append(f"  Highest Level: {self.highest_level_reached}")
        output.append(f"  Total XP Earned: {self.total_xp_earned}")
        output.append(f"  Quests Completed: {self.quests_completed}")
        output.append(f"  Quests Failed: {self.quests_failed}")
        output.append(f"  Stat Points Allocated: {self.stat_points_allocated}")
        output.append(f"  Achievements Unlocked: {self.achievements_unlocked}")

        # Time Statistics
        output.append("\n[TIME]")
        total_seconds = int(self.total_play_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        output.append(f"  Total Play Time: {hours}h {minutes}m")
        output.append(f"  Game Started: {self.game_start_time.strftime('%Y-%m-%d %H:%M')}")
        output.append(f"  Saves Created: {self.saves_created}")
        output.append(f"  Loads Performed: {self.loads_performed}")

        output.append("\n" + "="*70)
        return '\n'.join(output)

    def get_summary(self) -> str:
        """Get brief statistics summary."""
        return (f"Level {self.highest_level_reached} | "
                f"{self.battles_won}W/{self.deaths}L | "
                f"{self.quests_completed} Quests | "
                f"{self.achievements_unlocked} Achievements")

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        return {
            # Combat
            'total_battles': self.total_battles,
            'battles_won': self.battles_won,
            'battles_fled': self.battles_fled,
            'total_damage_dealt': self.total_damage_dealt,
            'total_damage_taken': self.total_damage_taken,
            'critical_hits': self.critical_hits,
            'dodges': self.dodges,
            'kills_by_enemy_type': dict(self.kills_by_enemy_type),
            'deaths': self.deaths,
            'flawless_victories': self.flawless_victories,
            'consecutive_wins': self.consecutive_wins,
            'best_win_streak': self.best_win_streak,

            # Exploration
            'locations_visited': list(self.locations_visited),
            'treasures_found': self.treasures_found,
            'distance_traveled': self.distance_traveled,
            'random_encounters': self.random_encounters,

            # Economy
            'total_gold_earned': self.total_gold_earned,
            'total_gold_spent': self.total_gold_spent,
            'items_bought': self.items_bought,
            'items_sold': self.items_sold,
            'most_expensive_purchase': self.most_expensive_purchase,

            # Collection
            'items_collected': list(self.items_collected),
            'unique_items_owned': self.unique_items_owned,
            'items_crafted': self.items_crafted,
            'recipes_discovered': self.recipes_discovered,

            # Progression
            'quests_completed': self.quests_completed,
            'quests_failed': self.quests_failed,
            'total_xp_earned': self.total_xp_earned,
            'highest_level_reached': self.highest_level_reached,
            'stat_points_allocated': self.stat_points_allocated,

            # Time
            'game_start_time': self.game_start_time.isoformat(),
            'total_play_time_seconds': self.total_play_time.total_seconds(),
            'saves_created': self.saves_created,
            'loads_performed': self.loads_performed,

            # Records
            'highest_damage_single_hit': self.highest_damage_single_hit,
            'fastest_battle_victory': self.fastest_battle_victory,
            'longest_battle': self.longest_battle,
            'highest_gold_owned': self.highest_gold_owned,
            'most_items_inventory': self.most_items_inventory,

            # Achievements
            'achievements_unlocked': self.achievements_unlocked
        }

    @staticmethod
    def from_dict(data: Dict) -> 'GameStatistics':
        """Create from dictionary."""
        stats = GameStatistics()

        # Combat
        stats.total_battles = data.get('total_battles', 0)
        stats.battles_won = data.get('battles_won', 0)
        stats.battles_fled = data.get('battles_fled', 0)
        stats.total_damage_dealt = data.get('total_damage_dealt', 0)
        stats.total_damage_taken = data.get('total_damage_taken', 0)
        stats.critical_hits = data.get('critical_hits', 0)
        stats.dodges = data.get('dodges', 0)
        stats.kills_by_enemy_type = defaultdict(int, data.get('kills_by_enemy_type', {}))
        stats.deaths = data.get('deaths', 0)
        stats.flawless_victories = data.get('flawless_victories', 0)
        stats.consecutive_wins = data.get('consecutive_wins', 0)
        stats.best_win_streak = data.get('best_win_streak', 0)

        # Exploration
        stats.locations_visited = set(data.get('locations_visited', []))
        stats.treasures_found = data.get('treasures_found', 0)
        stats.distance_traveled = data.get('distance_traveled', 0)
        stats.random_encounters = data.get('random_encounters', 0)

        # Economy
        stats.total_gold_earned = data.get('total_gold_earned', 0)
        stats.total_gold_spent = data.get('total_gold_spent', 0)
        stats.items_bought = data.get('items_bought', 0)
        stats.items_sold = data.get('items_sold', 0)
        stats.most_expensive_purchase = data.get('most_expensive_purchase', 0)

        # Collection
        stats.items_collected = set(data.get('items_collected', []))
        stats.unique_items_owned = data.get('unique_items_owned', 0)
        stats.items_crafted = data.get('items_crafted', 0)
        stats.recipes_discovered = data.get('recipes_discovered', 0)

        # Progression
        stats.quests_completed = data.get('quests_completed', 0)
        stats.quests_failed = data.get('quests_failed', 0)
        stats.total_xp_earned = data.get('total_xp_earned', 0)
        stats.highest_level_reached = data.get('highest_level_reached', 1)
        stats.stat_points_allocated = data.get('stat_points_allocated', 0)

        # Time
        if 'game_start_time' in data:
            stats.game_start_time = datetime.fromisoformat(data['game_start_time'])

        if 'total_play_time_seconds' in data:
            stats.total_play_time = timedelta(seconds=data['total_play_time_seconds'])

        stats.saves_created = data.get('saves_created', 0)
        stats.loads_performed = data.get('loads_performed', 0)

        # Records
        stats.highest_damage_single_hit = data.get('highest_damage_single_hit', 0)
        stats.fastest_battle_victory = data.get('fastest_battle_victory')
        stats.longest_battle = data.get('longest_battle')
        stats.highest_gold_owned = data.get('highest_gold_owned', 0)
        stats.most_items_inventory = data.get('most_items_inventory', 0)

        # Achievements
        stats.achievements_unlocked = data.get('achievements_unlocked', 0)

        return stats
