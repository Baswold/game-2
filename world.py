"""
World module - Manages locations, exploration, and world navigation.
"""

from typing import Dict, List, Optional, Set
from enum import Enum
import random


class LocationType(Enum):
    """Types of locations."""
    TOWN = "town"
    DUNGEON = "dungeon"
    WILDERNESS = "wilderness"
    CAVE = "cave"
    CASTLE = "castle"
    RUINS = "ruins"


class Location:
    """
    Represents a location in the game world.
    """

    def __init__(self, location_id: str, name: str, description: str,
                 location_type: LocationType, level_range: tuple = (1, 99),
                 connections: List[str] = None,
                 has_shop: bool = False,
                 has_inn: bool = False,
                 enemy_encounters: List[str] = None,
                 treasure_items: List[str] = None):
        self.location_id = location_id
        self.name = name
        self.description = description
        self.location_type = location_type
        self.level_range = level_range
        self.connections = connections or []  # IDs of connected locations
        self.has_shop = has_shop
        self.has_inn = has_inn
        self.enemy_encounters = enemy_encounters or []  # Enemy IDs
        self.treasure_items = treasure_items or []  # Item IDs
        self.visited = False
        self.treasures_found = set()  # Track which treasures have been found

    def get_random_enemy(self) -> Optional[str]:
        """Get a random enemy that can be encountered here."""
        if not self.enemy_encounters:
            return None
        return random.choice(self.enemy_encounters)

    def get_encounter_chance(self) -> float:
        """Get the chance of random encounter in this location."""
        if self.location_type == LocationType.TOWN:
            return 0.0
        elif self.location_type == LocationType.WILDERNESS:
            return 0.3
        elif self.location_type == LocationType.CAVE:
            return 0.5
        elif self.location_type == LocationType.DUNGEON:
            return 0.6
        elif self.location_type == LocationType.RUINS:
            return 0.5
        return 0.3

    def has_available_treasure(self) -> bool:
        """Check if there are unfound treasures."""
        return len(self.treasures_found) < len(self.treasure_items)

    def get_treasure(self) -> Optional[str]:
        """
        Get a treasure item if available.
        Returns item ID or None.
        """
        available = [
            item for item in self.treasure_items
            if item not in self.treasures_found
        ]

        if not available:
            return None

        treasure = random.choice(available)
        self.treasures_found.add(treasure)
        return treasure

    def reset_treasures(self):
        """Reset treasures (for respawning)."""
        self.treasures_found.clear()

    def __str__(self) -> str:
        return f"{self.name} ({self.location_type.value})"


class World:
    """
    Manages the game world and navigation.
    """

    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_location_id: Optional[str] = None

    def add_location(self, location: Location):
        """Add a location to the world."""
        self.locations[location.location_id] = location

    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID."""
        return self.locations.get(location_id)

    def get_current_location(self) -> Optional[Location]:
        """Get the current location."""
        if not self.current_location_id:
            return None
        return self.get_location(self.current_location_id)

    def move_to(self, location_id: str) -> bool:
        """
        Move to a new location.
        Returns True if successful.
        """
        if location_id not in self.locations:
            return False

        # Check if accessible from current location
        current = self.get_current_location()
        if current and location_id not in current.connections:
            return False

        self.current_location_id = location_id
        location = self.get_location(location_id)
        location.visited = True
        return True

    def get_available_destinations(self) -> List[Location]:
        """Get list of locations accessible from current location."""
        current = self.get_current_location()
        if not current:
            return []

        destinations = []
        for loc_id in current.connections:
            loc = self.get_location(loc_id)
            if loc:
                destinations.append(loc)

        return destinations

    def trigger_random_encounter(self) -> Optional[str]:
        """
        Check for random encounter in current location.
        Returns enemy ID if encounter triggered, None otherwise.
        """
        current = self.get_current_location()
        if not current:
            return None

        encounter_chance = current.get_encounter_chance()
        if random.random() < encounter_chance:
            return current.get_random_enemy()

        return None

    def to_dict(self) -> Dict:
        """Convert world state to dictionary for saving."""
        locations_data = {}
        for loc_id, loc in self.locations.items():
            locations_data[loc_id] = {
                'visited': loc.visited,
                'treasures_found': list(loc.treasures_found)
            }

        return {
            'current_location_id': self.current_location_id,
            'locations': locations_data
        }

    def from_dict(self, data: Dict):
        """Load world state from dictionary."""
        self.current_location_id = data.get('current_location_id')

        locations_data = data.get('locations', {})
        for loc_id, loc_data in locations_data.items():
            if loc_id in self.locations:
                self.locations[loc_id].visited = loc_data.get('visited', False)
                self.locations[loc_id].treasures_found = set(loc_data.get('treasures_found', []))


# =============================================================================
# WORLD CREATION
# =============================================================================

def create_game_world() -> World:
    """Create and populate the game world."""
    world = World()

    # === TOWNS ===

    world.add_location(Location(
        "hometown", "Hometown Village",
        "A peaceful village where your adventure begins. "
        "Humble cottages line the dirt roads, and friendly villagers go about their daily lives.",
        LocationType.TOWN,
        level_range=(1, 99),
        connections=["forest_path", "meadow"],
        has_shop=True,
        has_inn=True
    ))

    world.add_location(Location(
        "port_city", "Port City",
        "A bustling coastal city filled with merchants and sailors. "
        "The smell of salt and fish fills the air.",
        LocationType.TOWN,
        level_range=(5, 99),
        connections=["coastal_road", "city_outskirts"],
        has_shop=True,
        has_inn=True
    ))

    world.add_location(Location(
        "mountain_village", "Mountain Village",
        "A remote village nestled in the mountains. "
        "The air is thin and cold, but the people are warm and welcoming.",
        LocationType.TOWN,
        level_range=(8, 99),
        connections=["mountain_path", "snowy_peaks"],
        has_shop=True,
        has_inn=True
    ))

    # === WILDERNESS AREAS ===

    world.add_location(Location(
        "meadow", "Sunny Meadow",
        "A bright meadow filled with wildflowers. "
        "Small creatures scurry through the tall grass.",
        LocationType.WILDERNESS,
        level_range=(1, 3),
        connections=["hometown", "forest_path"],
        enemy_encounters=["slime", "wolf"],
        treasure_items=["health_potion_small", "bronze_ring"]
    ))

    world.add_location(Location(
        "forest_path", "Forest Path",
        "A winding path through dense woods. "
        "The canopy above blocks out much of the sunlight.",
        LocationType.WILDERNESS,
        level_range=(2, 4),
        connections=["hometown", "meadow", "dark_forest", "goblin_camp"],
        enemy_encounters=["goblin", "wolf", "bandit"],
        treasure_items=["health_potion_medium", "iron_sword", "leather_scrap"]
    ))

    world.add_location(Location(
        "dark_forest", "Dark Forest",
        "An ominous forest where few dare to venture. "
        "Strange sounds echo through the twisted trees.",
        LocationType.WILDERNESS,
        level_range=(5, 7),
        connections=["forest_path", "ancient_ruins", "witch_hut"],
        enemy_encounters=["skeleton", "dark_mage", "wolf"],
        treasure_items=["health_potion_large", "staff_mage", "enchanted_crystal"]
    ))

    world.add_location(Location(
        "coastal_road", "Coastal Road",
        "A scenic road following the coastline. "
        "Waves crash against the rocky shore.",
        LocationType.WILDERNESS,
        level_range=(4, 6),
        connections=["port_city", "beach_cave", "city_outskirts"],
        enemy_encounters=["bandit", "orc"],
        treasure_items=["silver_amulet", "health_potion_medium"]
    ))

    world.add_location(Location(
        "mountain_path", "Mountain Path",
        "A treacherous path winding up the mountain. "
        "One wrong step could mean a fatal fall.",
        LocationType.WILDERNESS,
        level_range=(7, 9),
        connections=["mountain_village", "snowy_peaks", "dragon_lair"],
        enemy_encounters=["orc", "troll", "wyvern"],
        treasure_items=["plate_armor", "health_potion_large", "ring_haste"]
    ))

    # === DUNGEONS & CAVES ===

    world.add_location(Location(
        "goblin_camp", "Goblin Camp",
        "A ramshackle camp full of goblins. "
        "Crude weapons and stolen goods are scattered everywhere.",
        LocationType.DUNGEON,
        level_range=(3, 5),
        connections=["forest_path"],
        enemy_encounters=["goblin", "goblin_chief", "bandit"],
        treasure_items=["steel_sword", "chain_mail", "health_potion_medium", "iron_ore"]
    ))

    world.add_location(Location(
        "beach_cave", "Beach Cave",
        "A damp cave carved by the sea. "
        "Water drips from the ceiling and pools on the floor.",
        LocationType.CAVE,
        level_range=(4, 6),
        connections=["coastal_road"],
        enemy_encounters=["bandit", "skeleton"],
        treasure_items=["silver_ore", "health_potion_large", "leather_armor"]
    ))

    world.add_location(Location(
        "abandoned_mine", "Abandoned Mine",
        "An old mine shaft that goes deep underground. "
        "Support beams creak ominously in the darkness.",
        LocationType.CAVE,
        level_range=(6, 8),
        connections=["city_outskirts"],
        enemy_encounters=["skeleton", "orc", "troll"],
        treasure_items=["steel_ingot", "iron_ore", "health_potion_large", "ring_strength"]
    ))

    world.add_location(Location(
        "crystal_cavern", "Crystal Cavern",
        "A beautiful cavern filled with glowing crystals. "
        "The air hums with magical energy.",
        LocationType.CAVE,
        level_range=(8, 10),
        connections=["snowy_peaks"],
        enemy_encounters=["dark_mage", "demon"],
        treasure_items=[
            "enchanted_crystal", "enchanted_crystal", "staff_mage",
            "health_potion_supreme", "elixir_vitality"
        ]
    ))

    # === RUINS & SPECIAL LOCATIONS ===

    world.add_location(Location(
        "ancient_ruins", "Ancient Ruins",
        "Crumbling stone structures from a long-lost civilization. "
        "Magic still lingers in the air.",
        LocationType.RUINS,
        level_range=(6, 8),
        connections=["dark_forest"],
        enemy_encounters=["skeleton", "vampire", "dark_mage"],
        treasure_items=[
            "silver_rapier", "amulet_protection", "health_potion_large",
            "ancient_key", "enchanted_crystal"
        ]
    ))

    world.add_location(Location(
        "witch_hut", "Witch's Hut",
        "A mysterious hut deep in the forest. "
        "Strange herbs and potions line the shelves.",
        LocationType.RUINS,
        level_range=(5, 7),
        connections=["dark_forest"],
        has_shop=True,  # Witch sells rare items
        enemy_encounters=["dark_mage"],
        treasure_items=["phoenix_down", "elixir_vitality", "rare_herb"]
    ))

    world.add_location(Location(
        "dragon_lair", "Dragon's Lair",
        "A massive cave that reeks of sulfur and charred bones. "
        "This is the home of an ancient dragon.",
        LocationType.CAVE,
        level_range=(15, 20),
        connections=["mountain_path"],
        enemy_encounters=["dragon", "wyvern"],
        treasure_items=[
            "dragon_slayer", "dragon_armor", "dragon_scale",
            "health_potion_supreme", "phoenix_down", "excalibur"
        ]
    ))

    world.add_location(Location(
        "cursed_castle", "Cursed Castle",
        "An ancient castle shrouded in darkness. "
        "Undead creatures roam its halls, serving the Lich King.",
        LocationType.CASTLE,
        level_range=(18, 20),
        connections=["city_outskirts"],
        enemy_encounters=["vampire", "skeleton", "lich"],
        treasure_items=[
            "excalibur", "celestial_robe", "crown_wisdom",
            "pendant_phoenix", "phoenix_down", "star_fragment"
        ]
    ))

    # === CONNECTING AREAS ===

    world.add_location(Location(
        "city_outskirts", "City Outskirts",
        "The outer edges of the port city. "
        "Less safe than the city proper, but still civilized.",
        LocationType.WILDERNESS,
        level_range=(5, 7),
        connections=["port_city", "coastal_road", "abandoned_mine", "cursed_castle"],
        enemy_encounters=["bandit", "orc"],
        treasure_items=["health_potion_medium", "leather_armor"]
    ))

    world.add_location(Location(
        "snowy_peaks", "Snowy Peaks",
        "The highest peaks of the mountain range. "
        "Howling winds and blinding snow make travel dangerous.",
        LocationType.WILDERNESS,
        level_range=(9, 12),
        connections=["mountain_village", "mountain_path", "crystal_cavern"],
        enemy_encounters=["wyvern", "troll", "demon"],
        treasure_items=[
            "dragon_scale", "health_potion_supreme",
            "ring_haste", "phoenix_down"
        ]
    ))

    # Set starting location
    world.current_location_id = "hometown"
    world.locations["hometown"].visited = True

    return world


def display_location(location: Location, detailed: bool = True) -> str:
    """Format location information for display."""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"📍 {location.name.upper()}")
    output.append(f"{'='*60}")
    output.append(f"\n{location.description}")

    if detailed:
        output.append(f"\nType: {location.location_type.value.title()}")
        output.append(f"Recommended Level: {location.level_range[0]}-{location.level_range[1]}")

        features = []
        if location.has_shop:
            features.append("🏪 Shop")
        if location.has_inn:
            features.append("🛏️ Inn")
        if location.enemy_encounters:
            features.append("⚔️ Monsters")
        if location.has_available_treasure():
            features.append("💎 Treasure")

        if features:
            output.append(f"\nFeatures: {' | '.join(features)}")

    output.append(f"{'='*60}\n")
    return '\n'.join(output)


def display_travel_options(world: World) -> str:
    """Display available travel destinations."""
    destinations = world.get_available_destinations()

    if not destinations:
        return "\nNo destinations available from here.\n"

    output = []
    output.append("\n--- Available Destinations ---")

    for i, dest in enumerate(destinations, 1):
        visited_marker = "✓" if dest.visited else "?"
        output.append(f"{i}. {visited_marker} {dest.name} (Lv.{dest.level_range[0]}-{dest.level_range[1]})")

    return '\n'.join(output)
