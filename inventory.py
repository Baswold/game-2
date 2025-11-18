"""
Inventory module - Manages player inventory and item interactions.
"""

from typing import Dict, List, Optional
from items import Item, ItemType, create_item, get_item


class Inventory:
    """
    Manages the player's inventory with stacking, sorting, and organization.
    """

    def __init__(self, max_capacity: int = 50):
        self.max_capacity = max_capacity
        self.items: Dict[str, int] = {}  # item_id -> quantity

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Add item(s) to inventory.
        Returns True if successful.
        """
        if not get_item(item_id):
            return False

        # Check capacity
        current_total = sum(self.items.values())
        if current_total + quantity > self.max_capacity:
            return False

        self.items[item_id] = self.items.get(item_id, 0) + quantity
        return True

    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Remove item(s) from inventory.
        Returns True if successful.
        """
        if item_id not in self.items:
            return False

        if self.items[item_id] < quantity:
            return False

        self.items[item_id] -= quantity

        if self.items[item_id] <= 0:
            del self.items[item_id]

        return True

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        """Check if inventory contains item(s)."""
        return self.items.get(item_id, 0) >= quantity

    def get_item_count(self, item_id: str) -> int:
        """Get quantity of a specific item."""
        return self.items.get(item_id, 0)

    def get_total_items(self) -> int:
        """Get total number of items in inventory."""
        return sum(self.items.values())

    def get_items_by_type(self, item_type: ItemType) -> List[tuple]:
        """
        Get all items of a specific type.
        Returns list of (item, quantity) tuples.
        """
        result = []
        for item_id, quantity in self.items.items():
            item = get_item(item_id)
            if item and item.item_type == item_type:
                result.append((item, quantity))
        return result

    def get_all_items(self) -> List[tuple]:
        """
        Get all items in inventory.
        Returns list of (item, quantity) tuples.
        """
        result = []
        for item_id, quantity in self.items.items():
            item = get_item(item_id)
            if item:
                result.append((item, quantity))
        return result

    def sort_items(self) -> List[tuple]:
        """
        Get sorted items (by type, rarity, then name).
        Returns list of (item, quantity) tuples.
        """
        items = self.get_all_items()

        # Sort by: type, rarity (descending), name
        type_order = {
            ItemType.WEAPON: 0,
            ItemType.ARMOR: 1,
            ItemType.ACCESSORY: 2,
            ItemType.CONSUMABLE: 3,
            ItemType.MATERIAL: 4,
            ItemType.QUEST: 5
        }

        rarity_values = {
            'LEGENDARY': 5,
            'EPIC': 4,
            'RARE': 3,
            'UNCOMMON': 2,
            'COMMON': 1
        }

        def sort_key(item_tuple):
            item, _ = item_tuple
            type_val = type_order.get(item.item_type, 999)
            rarity_val = -rarity_values.get(item.rarity.name, 0)
            return (type_val, rarity_val, item.name)

        return sorted(items, key=sort_key)

    def is_full(self) -> bool:
        """Check if inventory is at max capacity."""
        return self.get_total_items() >= self.max_capacity

    def get_free_space(self) -> int:
        """Get number of free inventory slots."""
        return self.max_capacity - self.get_total_items()

    def clear(self):
        """Remove all items from inventory."""
        self.items.clear()

    def display(self) -> str:
        """Get formatted string displaying all inventory items."""
        items = self.sort_items()

        if not items:
            return "\nInventory is empty.\n"

        output = []
        output.append(f"\n{'='*60}")
        output.append(f"INVENTORY ({self.get_total_items()}/{self.max_capacity})")
        output.append(f"{'='*60}")

        current_type = None
        for item, quantity in items:
            # Add category headers
            if item.item_type != current_type:
                current_type = item.item_type
                output.append(f"\n[{item.item_type.value.upper()}]")

            # Format item display
            qty_str = f"x{quantity}" if quantity > 1 else ""
            rarity_indicator = self._get_rarity_indicator(item.rarity.name)

            if item.item_type == ItemType.WEAPON:
                output.append(f"  {rarity_indicator} {item.name} {qty_str}")
                output.append(f"      Damage: {item.damage} | {item.get_stats_description()}")
                output.append(f"      {item.description}")
            elif item.item_type == ItemType.ARMOR:
                output.append(f"  {rarity_indicator} {item.name} {qty_str}")
                output.append(f"      Defense: +{item.defense_bonus} | {item.get_stats_description()}")
                output.append(f"      {item.description}")
            elif item.item_type == ItemType.ACCESSORY:
                output.append(f"  {rarity_indicator} {item.name} {qty_str}")
                output.append(f"      {item.get_stats_description()}")
                output.append(f"      {item.description}")
            elif item.item_type == ItemType.CONSUMABLE:
                output.append(f"  {rarity_indicator} {item.name} {qty_str}")
                output.append(f"      {item.description}")
            else:
                output.append(f"  {rarity_indicator} {item.name} {qty_str}")
                output.append(f"      {item.description}")

        output.append(f"{'='*60}\n")
        return '\n'.join(output)

    def _get_rarity_indicator(self, rarity: str) -> str:
        """Get a visual indicator for item rarity."""
        indicators = {
            'COMMON': '○',
            'UNCOMMON': '◆',
            'RARE': '★',
            'EPIC': '♦',
            'LEGENDARY': '♛'
        }
        return indicators.get(rarity, '•')

    def to_dict(self) -> Dict:
        """Convert inventory to dictionary for saving."""
        return {
            'max_capacity': self.max_capacity,
            'items': self.items.copy()
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Inventory':
        """Create inventory from dictionary."""
        inventory = Inventory(data['max_capacity'])
        inventory.items = data['items'].copy()
        return inventory


class Shop:
    """
    Represents a shop where players can buy and sell items.
    """

    def __init__(self, name: str, inventory: Dict[str, int], buy_multiplier: float = 1.0,
                 sell_multiplier: float = 0.5):
        self.name = name
        self.inventory = inventory  # item_id -> quantity (-1 for unlimited)
        self.buy_multiplier = buy_multiplier  # Price multiplier for buying
        self.sell_multiplier = sell_multiplier  # Price multiplier for selling

    def has_item(self, item_id: str) -> bool:
        """Check if shop has item in stock."""
        return item_id in self.inventory and self.inventory[item_id] != 0

    def get_buy_price(self, item_id: str) -> int:
        """Get the price to buy an item from shop."""
        item = get_item(item_id)
        if not item:
            return 0
        return int(item.value * self.buy_multiplier)

    def get_sell_price(self, item_id: str) -> int:
        """Get the price to sell an item to shop."""
        item = get_item(item_id)
        if not item:
            return 0
        return int(item.value * self.sell_multiplier)

    def buy_item(self, item_id: str, character, player_inventory: Inventory) -> tuple:
        """
        Player buys item from shop.
        Returns (success: bool, message: str).
        """
        if not self.has_item(item_id):
            return False, "Item not in stock."

        item = get_item(item_id)
        if not item:
            return False, "Invalid item."

        price = self.get_buy_price(item_id)

        if character.gold < price:
            return False, f"Not enough gold. Need {price}g, have {character.gold}g."

        if player_inventory.is_full():
            return False, "Inventory is full."

        # Process transaction
        character.remove_gold(price)
        player_inventory.add_item(item_id, 1)

        # Reduce shop stock (if not unlimited)
        if self.inventory[item_id] > 0:
            self.inventory[item_id] -= 1

        return True, f"Purchased {item.name} for {price}g."

    def sell_item(self, item_id: str, character, player_inventory: Inventory) -> tuple:
        """
        Player sells item to shop.
        Returns (success: bool, message: str).
        """
        if not player_inventory.has_item(item_id):
            return False, "You don't have that item."

        item = get_item(item_id)
        if not item:
            return False, "Invalid item."

        if item.item_type == ItemType.QUEST:
            return False, "Cannot sell quest items."

        price = self.get_sell_price(item_id)

        # Process transaction
        player_inventory.remove_item(item_id, 1)
        character.add_gold(price)

        # Add to shop stock
        if item_id in self.inventory:
            if self.inventory[item_id] >= 0:
                self.inventory[item_id] += 1
        else:
            self.inventory[item_id] = 1

        return True, f"Sold {item.name} for {price}g."

    def display_stock(self) -> str:
        """Get formatted string of shop inventory."""
        output = []
        output.append(f"\n{'='*60}")
        output.append(f"{self.name.upper()}")
        output.append(f"{'='*60}")

        # Group items by type
        items_by_type = {}
        for item_id, quantity in self.inventory.items():
            if quantity == 0:
                continue

            item = get_item(item_id)
            if not item:
                continue

            item_type = item.item_type
            if item_type not in items_by_type:
                items_by_type[item_type] = []

            price = self.get_buy_price(item_id)
            stock_text = f"({quantity} in stock)" if quantity > 0 else "(Unlimited)"
            items_by_type[item_type].append((item, price, stock_text))

        # Display by category
        for item_type in [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY,
                          ItemType.CONSUMABLE, ItemType.MATERIAL]:
            if item_type not in items_by_type:
                continue

            output.append(f"\n[{item_type.value.upper()}]")

            for item, price, stock_text in items_by_type[item_type]:
                output.append(f"  • {item.name} - {price}g {stock_text}")
                output.append(f"    {item.description}")

        output.append(f"\n{'='*60}\n")
        return '\n'.join(output)


# =============================================================================
# SHOP DEFINITIONS
# =============================================================================

def create_general_shop() -> Shop:
    """Create the general store."""
    inventory = {
        'health_potion_small': -1,
        'health_potion_medium': -1,
        'health_potion_large': 5,
        'rusty_sword': 3,
        'iron_sword': 2,
        'cloth_armor': 3,
        'leather_armor': 2,
        'bronze_ring': 5,
    }
    return Shop("General Store", inventory, buy_multiplier=1.0, sell_multiplier=0.5)


def create_weapon_shop() -> Shop:
    """Create the weapon shop."""
    inventory = {
        'iron_sword': -1,
        'steel_sword': 2,
        'silver_rapier': 1,
        'staff_apprentice': -1,
        'staff_mage': 1,
    }
    return Shop("Blacksmith's Forge", inventory, buy_multiplier=1.2, sell_multiplier=0.6)


def create_armor_shop() -> Shop:
    """Create the armor shop."""
    inventory = {
        'leather_armor': -1,
        'chain_mail': 2,
        'plate_armor': 1,
    }
    return Shop("Armor Emporium", inventory, buy_multiplier=1.2, sell_multiplier=0.6)


def create_magic_shop() -> Shop:
    """Create the magic shop."""
    inventory = {
        'health_potion_medium': -1,
        'health_potion_large': -1,
        'health_potion_supreme': 3,
        'elixir_vitality': 2,
        'phoenix_down': 1,
        'silver_amulet': 3,
        'staff_mage': 1,
    }
    return Shop("Mystical Emporium", inventory, buy_multiplier=1.5, sell_multiplier=0.7)
