"""
Quest module - Manages quests, objectives, and rewards.
"""

from typing import Dict, List, Optional, Callable
from enum import Enum


class QuestStatus(Enum):
    """Quest status states."""
    NOT_STARTED = "not_started"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class ObjectiveType(Enum):
    """Types of quest objectives."""
    KILL_ENEMY = "kill_enemy"
    COLLECT_ITEM = "collect_item"
    VISIT_LOCATION = "visit_location"
    DELIVER_ITEM = "deliver_item"
    TALK_TO_NPC = "talk_to_npc"
    REACH_LEVEL = "reach_level"


class Objective:
    """
    Represents a quest objective.
    """

    def __init__(self, objective_id: str, description: str,
                 objective_type: ObjectiveType, target: str,
                 required_amount: int = 1):
        self.objective_id = objective_id
        self.description = description
        self.objective_type = objective_type
        self.target = target  # Enemy ID, item ID, location ID, etc.
        self.required_amount = required_amount
        self.current_amount = 0
        self.completed = False

    def update_progress(self, amount: int = 1):
        """Update objective progress."""
        self.current_amount = min(self.required_amount, self.current_amount + amount)
        if self.current_amount >= self.required_amount:
            self.completed = True

    def is_complete(self) -> bool:
        """Check if objective is complete."""
        return self.completed

    def get_progress_string(self) -> str:
        """Get progress as a string."""
        if self.completed:
            return f"✓ {self.description}"
        return f"○ {self.description} ({self.current_amount}/{self.required_amount})"

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'objective_id': self.objective_id,
            'current_amount': self.current_amount,
            'completed': self.completed
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.current_amount = data.get('current_amount', 0)
        self.completed = data.get('completed', False)


class Quest:
    """
    Represents a quest with objectives and rewards.
    """

    def __init__(self, quest_id: str, name: str, description: str,
                 objectives: List[Objective], level_requirement: int = 1,
                 xp_reward: int = 0, gold_reward: int = 0,
                 item_rewards: List[str] = None,
                 prerequisite_quests: List[str] = None):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.level_requirement = level_requirement
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.item_rewards = item_rewards or []
        self.prerequisite_quests = prerequisite_quests or []
        self.status = QuestStatus.NOT_STARTED

    def can_start(self, character, completed_quests: set) -> tuple:
        """
        Check if quest can be started.
        Returns (can_start: bool, reason: str).
        """
        if self.status != QuestStatus.NOT_STARTED:
            return False, "Quest already started or completed."

        if character.level < self.level_requirement:
            return False, f"Requires level {self.level_requirement}."

        for prereq in self.prerequisite_quests:
            if prereq not in completed_quests:
                return False, "Missing prerequisite quest."

        return True, ""

    def start(self):
        """Start the quest."""
        self.status = QuestStatus.ACTIVE

    def update_objective(self, objective_type: ObjectiveType, target: str, amount: int = 1):
        """
        Update progress for objectives matching type and target.
        """
        for objective in self.objectives:
            if (objective.objective_type == objective_type and
                    objective.target == target and
                    not objective.completed):
                objective.update_progress(amount)

    def check_completion(self) -> bool:
        """
        Check if all objectives are complete.
        Returns True if quest can be completed.
        """
        if self.status != QuestStatus.ACTIVE:
            return False

        return all(obj.is_complete() for obj in self.objectives)

    def complete(self) -> bool:
        """
        Complete the quest.
        Returns True if successful.
        """
        if not self.check_completion():
            return False

        self.status = QuestStatus.COMPLETED
        return True

    def fail(self):
        """Mark quest as failed."""
        self.status = QuestStatus.FAILED

    def get_progress_display(self) -> str:
        """Get formatted quest progress."""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"📜 {self.name}")
        output.append(f"{'='*60}")
        output.append(f"{self.description}")
        output.append(f"\nStatus: {self.status.value.replace('_', ' ').title()}")

        if self.status == QuestStatus.ACTIVE:
            output.append(f"\nObjectives:")
            for obj in self.objectives:
                output.append(f"  {obj.get_progress_string()}")

        output.append(f"\nRewards:")
        if self.xp_reward > 0:
            output.append(f"  • {self.xp_reward} XP")
        if self.gold_reward > 0:
            output.append(f"  • {self.gold_reward} Gold")
        if self.item_rewards:
            from items import get_item
            for item_id in self.item_rewards:
                item = get_item(item_id)
                if item:
                    output.append(f"  • {item.name}")

        output.append(f"{'='*60}\n")
        return '\n'.join(output)

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        return {
            'quest_id': self.quest_id,
            'status': self.status.value,
            'objectives': [obj.to_dict() for obj in self.objectives]
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.status = QuestStatus(data.get('status', 'not_started'))

        objectives_data = data.get('objectives', [])
        for i, obj_data in enumerate(objectives_data):
            if i < len(self.objectives):
                self.objectives[i].from_dict(obj_data)


class QuestManager:
    """
    Manages all quests in the game.
    """

    def __init__(self):
        self.available_quests: Dict[str, Quest] = {}
        self.active_quests: Dict[str, Quest] = {}
        self.completed_quests: set = set()

    def register_quest(self, quest: Quest):
        """Register a quest as available."""
        self.available_quests[quest.quest_id] = quest

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Get a quest by ID from any category."""
        if quest_id in self.active_quests:
            return self.active_quests[quest_id]
        elif quest_id in self.available_quests:
            return self.available_quests[quest_id]
        return None

    def can_start_quest(self, quest_id: str, character) -> tuple:
        """Check if a quest can be started."""
        quest = self.available_quests.get(quest_id)
        if not quest:
            return False, "Quest not found."

        return quest.can_start(character, self.completed_quests)

    def start_quest(self, quest_id: str) -> bool:
        """Start a quest."""
        if quest_id not in self.available_quests:
            return False

        quest = self.available_quests[quest_id]
        quest.start()
        self.active_quests[quest_id] = quest
        del self.available_quests[quest_id]
        return True

    def update_quest_progress(self, objective_type: ObjectiveType, target: str, amount: int = 1):
        """Update progress for all relevant active quests."""
        for quest in self.active_quests.values():
            quest.update_objective(objective_type, target, amount)

    def complete_quest(self, quest_id: str) -> Optional[Quest]:
        """
        Complete a quest and move it to completed.
        Returns the quest if successful, None otherwise.
        """
        if quest_id not in self.active_quests:
            return None

        quest = self.active_quests[quest_id]
        if quest.complete():
            self.completed_quests.add(quest_id)
            del self.active_quests[quest_id]
            return quest

        return None

    def get_completable_quests(self) -> List[Quest]:
        """Get all active quests that can be completed."""
        return [q for q in self.active_quests.values() if q.check_completion()]

    def get_active_quests(self) -> List[Quest]:
        """Get all active quests."""
        return list(self.active_quests.values())

    def get_available_quests(self, character) -> List[Quest]:
        """Get all quests that can be started."""
        available = []
        for quest in self.available_quests.values():
            can_start, _ = quest.can_start(character, self.completed_quests)
            if can_start:
                available.append(quest)
        return available

    def display_active_quests(self) -> str:
        """Display all active quests."""
        if not self.active_quests:
            return "\nNo active quests.\n"

        output = []
        output.append("\n=== ACTIVE QUESTS ===\n")

        for quest in self.active_quests.values():
            completable = "✓" if quest.check_completion() else "○"
            output.append(f"{completable} {quest.name}")

            for obj in quest.objectives:
                output.append(f"    {obj.get_progress_string()}")

        return '\n'.join(output)

    def to_dict(self) -> Dict:
        """Convert to dictionary for saving."""
        active_data = {}
        for quest_id, quest in self.active_quests.items():
            active_data[quest_id] = quest.to_dict()

        available_data = {}
        for quest_id, quest in self.available_quests.items():
            available_data[quest_id] = quest.to_dict()

        return {
            'active_quests': active_data,
            'available_quests': available_data,
            'completed_quests': list(self.completed_quests)
        }

    def from_dict(self, data: Dict):
        """Load from dictionary."""
        self.completed_quests = set(data.get('completed_quests', []))

        # Active quests need to be reconstructed from templates
        # This would require access to quest templates
        # For now, just track the IDs and status


# =============================================================================
# QUEST DEFINITIONS
# =============================================================================

def create_all_quests() -> QuestManager:
    """Create and register all quests in the game."""
    manager = QuestManager()

    # === STARTER QUESTS ===

    manager.register_quest(Quest(
        "first_steps", "First Steps",
        "The village elder asks you to prove yourself by defeating some slimes in the meadow.",
        objectives=[
            Objective("kill_slimes", "Defeat 3 Slimes", ObjectiveType.KILL_ENEMY, "slime", 3)
        ],
        level_requirement=1,
        xp_reward=50,
        gold_reward=25,
        item_rewards=["health_potion_small", "health_potion_small"]
    ))

    manager.register_quest(Quest(
        "wolf_problem", "Wolf Problem",
        "Wolves have been attacking travelers on the forest path. Help clear them out.",
        objectives=[
            Objective("kill_wolves", "Defeat 5 Wolves", ObjectiveType.KILL_ENEMY, "wolf", 5)
        ],
        level_requirement=2,
        xp_reward=100,
        gold_reward=50,
        item_rewards=["leather_armor"]
    ))

    manager.register_quest(Quest(
        "goblin_threat", "The Goblin Threat",
        "Goblins have established a camp near the forest. Defeat their chief to scatter them.",
        objectives=[
            Objective("kill_chief", "Defeat the Goblin Chief", ObjectiveType.KILL_ENEMY, "goblin_chief", 1),
            Objective("collect_head", "Collect proof of victory", ObjectiveType.COLLECT_ITEM, "goblin_chief_head", 1)
        ],
        level_requirement=4,
        xp_reward=200,
        gold_reward=150,
        item_rewards=["steel_sword", "health_potion_medium"],
        prerequisite_quests=["first_steps"]
    ))

    # === EXPLORATION QUESTS ===

    manager.register_quest(Quest(
        "explore_coast", "Coastal Explorer",
        "Visit the port city and explore the coastal areas.",
        objectives=[
            Objective("visit_port", "Visit Port City", ObjectiveType.VISIT_LOCATION, "port_city", 1),
            Objective("visit_beach", "Explore Beach Cave", ObjectiveType.VISIT_LOCATION, "beach_cave", 1)
        ],
        level_requirement=4,
        xp_reward=150,
        gold_reward=100,
        item_rewards=["silver_amulet"]
    ))

    manager.register_quest(Quest(
        "mountain_expedition", "Mountain Expedition",
        "Reach the mountain village and survey the snowy peaks.",
        objectives=[
            Objective("visit_village", "Reach Mountain Village", ObjectiveType.VISIT_LOCATION, "mountain_village", 1),
            Objective("visit_peaks", "Survey Snowy Peaks", ObjectiveType.VISIT_LOCATION, "snowy_peaks", 1)
        ],
        level_requirement=8,
        xp_reward=300,
        gold_reward=200,
        item_rewards=["ring_haste", "health_potion_large"]
    ))

    # === COLLECTION QUESTS ===

    manager.register_quest(Quest(
        "herb_gathering", "Herb Gathering",
        "The village healer needs rare herbs. Search the witch's hut area.",
        objectives=[
            Objective("collect_herb", "Find Rare Healing Herb", ObjectiveType.COLLECT_ITEM, "rare_herb", 1)
        ],
        level_requirement=5,
        xp_reward=120,
        gold_reward=80,
        item_rewards=["health_potion_large", "elixir_vitality"]
    ))

    manager.register_quest(Quest(
        "crystal_collector", "Crystal Collector",
        "A wizard needs enchanted crystals for research. Bring him 3 crystals.",
        objectives=[
            Objective("collect_crystals", "Collect Enchanted Crystals",
                      ObjectiveType.COLLECT_ITEM, "enchanted_crystal", 3)
        ],
        level_requirement=7,
        xp_reward=250,
        gold_reward=200,
        item_rewards=["staff_mage", "health_potion_supreme"]
    ))

    manager.register_quest(Quest(
        "dragon_scales", "Dragon Scale Armor",
        "A master blacksmith will craft legendary armor if you bring dragon scales.",
        objectives=[
            Objective("collect_scales", "Collect Dragon Scales",
                      ObjectiveType.COLLECT_ITEM, "dragon_scale", 5)
        ],
        level_requirement=12,
        xp_reward=500,
        gold_reward=500,
        item_rewards=["dragon_armor", "dragon_slayer"]
    ))

    # === COMBAT QUESTS ===

    manager.register_quest(Quest(
        "skeleton_slayer", "Skeleton Slayer",
        "Undead skeletons have been spotted near the ruins. Clear them out.",
        objectives=[
            Objective("kill_skeletons", "Defeat 8 Skeleton Warriors",
                      ObjectiveType.KILL_ENEMY, "skeleton", 8)
        ],
        level_requirement=5,
        xp_reward=180,
        gold_reward=120,
        item_rewards=["silver_rapier", "chain_mail"]
    ))

    manager.register_quest(Quest(
        "vampire_hunter", "Vampire Hunter",
        "A vampire lord has been terrorizing travelers. Hunt it down.",
        objectives=[
            Objective("kill_vampire", "Defeat the Vampire Lord",
                      ObjectiveType.KILL_ENEMY, "vampire", 1)
        ],
        level_requirement=10,
        xp_reward=400,
        gold_reward=300,
        item_rewards=["amulet_protection", "phoenix_down"]
    ))

    manager.register_quest(Quest(
        "demon_bane", "Demon Bane",
        "Lesser demons have emerged from the underworld. Send them back!",
        objectives=[
            Objective("kill_demons", "Defeat 5 Lesser Demons",
                      ObjectiveType.KILL_ENEMY, "demon", 5)
        ],
        level_requirement=12,
        xp_reward=600,
        gold_reward=400,
        item_rewards=["ring_strength", "crown_wisdom", "health_potion_supreme"]
    ))

    # === BOSS QUESTS ===

    manager.register_quest(Quest(
        "dragon_slayer_quest", "Dragon Slayer",
        "An ancient dragon threatens the realm. Only a true hero can defeat it.",
        objectives=[
            Objective("kill_dragon", "Defeat the Ancient Dragon",
                      ObjectiveType.KILL_ENEMY, "dragon", 1)
        ],
        level_requirement=15,
        xp_reward=1000,
        gold_reward=1000,
        item_rewards=["excalibur", "dragon_armor", "phoenix_down", "elixir_vitality"],
        prerequisite_quests=["demon_bane", "vampire_hunter"]
    ))

    manager.register_quest(Quest(
        "lich_king", "The Lich King",
        "The ultimate evil - defeat the Lich King and save the world!",
        objectives=[
            Objective("kill_lich", "Defeat the Lich King",
                      ObjectiveType.KILL_ENEMY, "lich", 1)
        ],
        level_requirement=18,
        xp_reward=2000,
        gold_reward=2000,
        item_rewards=["celestial_robe", "pendant_phoenix", "star_fragment"],
        prerequisite_quests=["dragon_slayer_quest"]
    ))

    # === LEVEL PROGRESSION QUESTS ===

    manager.register_quest(Quest(
        "prove_strength", "Prove Your Strength",
        "Train and reach level 5 to prove you're ready for greater challenges.",
        objectives=[
            Objective("reach_level", "Reach Level 5", ObjectiveType.REACH_LEVEL, "5", 5)
        ],
        level_requirement=1,
        xp_reward=100,
        gold_reward=100,
        item_rewards=["health_potion_medium", "iron_sword"]
    ))

    manager.register_quest(Quest(
        "master_warrior", "Master Warrior",
        "Become a master warrior by reaching level 10.",
        objectives=[
            Objective("reach_level", "Reach Level 10", ObjectiveType.REACH_LEVEL, "10", 10)
        ],
        level_requirement=5,
        xp_reward=300,
        gold_reward=300,
        item_rewards=["plate_armor", "health_potion_large", "phoenix_down"],
        prerequisite_quests=["prove_strength"]
    ))

    return manager
