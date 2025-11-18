#!/usr/bin/env python3
"""
Epic Quest - A Text-Based RPG Adventure
Main game loop and entry point.
"""

import sys
import random
from typing import Optional

# Import game modules
from character import Character
from inventory import Inventory, create_general_shop, create_weapon_shop, create_armor_shop, create_magic_shop
from combat import Combat, CombatAction, CombatResult, create_enemy, get_random_enemy_for_level
from world import create_game_world, display_location, display_travel_options
from quest import create_all_quests, ObjectiveType
from items import create_item, get_item, ItemType
from crafting import create_crafting_system
from save_system import GameState, SaveGame
from ui import *


class Game:
    """
    Main game controller.
    """

    def __init__(self):
        self.game_state = GameState()
        self.running = True
        self.shops = {
            'general': create_general_shop(),
            'weapon': create_weapon_shop(),
            'armor': create_armor_shop(),
            'magic': create_magic_shop()
        }

    def start(self):
        """Start the game."""
        display_title_screen()

        # Main menu
        while True:
            print("\n")
            choice = display_menu(
                "MAIN MENU",
                ["New Game", "Load Game", "Exit"],
                allow_back=False
            )

            if choice == 0:  # New Game
                self.new_game()
                break
            elif choice == 1:  # Load Game
                if self.load_game_menu():
                    break
            elif choice == 2:  # Exit
                print("\nThanks for playing!")
                sys.exit(0)

        # Start main game loop
        if self.game_state.character:
            self.main_loop()

    def new_game(self):
        """Start a new game."""
        clear_screen()
        print_header("NEW GAME", "=", 60)

        # Character creation
        print("\nWelcome, brave adventurer!")
        name = input("Enter your character's name: ").strip()

        if not name:
            name = "Hero"

        self.game_state.new_game(name)

        # Allocate starting stats
        self.allocate_stats()

        print(f"\nWelcome, {name}! Your adventure begins...")
        pause()

    def load_game_menu(self) -> bool:
        """
        Show load game menu.
        Returns True if game was loaded.
        """
        saves = SaveGame.get_all_saves()

        if not saves:
            print("\nNo saved games found.")
            pause()
            return False

        clear_screen()
        print_header("LOAD GAME", "=", 60)

        print("\nAvailable saves:")
        for i, save in enumerate(saves, 1):
            timestamp = save['timestamp'].split('T')[0]  # Just show date
            print(f"{i}. {save['character_name']} (Lv.{save['level']}) - {timestamp}")

        print("0. Back")

        choice = get_number("\nSelect save: ", min_val=0, max_val=len(saves))

        if choice == 0:
            return False

        save_name = saves[choice - 1]['save_name']

        loading_animation("Loading game")

        if self.game_state.load_game(save_name):
            print("\nGame loaded successfully!")
            pause()
            return True
        else:
            print("\nFailed to load game.")
            pause()
            return False

    def main_loop(self):
        """Main game loop."""
        while self.running:
            # Check for game over
            if self.game_state.character.is_dead():
                self.game_over()
                break

            # Show main menu
            self.main_menu()

    def main_menu(self):
        """Display and handle main game menu."""
        clear_screen()

        # Display current status
        char = self.game_state.character
        location = self.game_state.world.get_current_location()

        print(f"\n{char.name} (Lv.{char.level}) | HP: {char.get_current_hp()}/{char.get_max_hp()} | Gold: {char.gold}g")
        print(f"Location: {location.name if location else 'Unknown'}")
        print_separator("-", 60)

        options = [
            "📊 View Character",
            "🎒 Inventory",
            "🗺️  Travel",
            "⚔️  Search for Enemies",
            "🔍 Explore Area",
            "📜 Quests",
            "⚒️  Crafting",
            "🏪 Shop",
            "🛏️  Rest",
            "💾 Save Game",
            "⚙️  Settings",
            "🚪 Quit"
        ]

        choice = display_menu("MAIN MENU", options, allow_back=False)

        if choice == 0:  # View Character
            self.view_character()
        elif choice == 1:  # Inventory
            self.inventory_menu()
        elif choice == 2:  # Travel
            self.travel_menu()
        elif choice == 3:  # Search for Enemies
            self.search_for_combat()
        elif choice == 4:  # Explore Area
            self.explore_area()
        elif choice == 5:  # Quests
            self.quest_menu()
        elif choice == 6:  # Crafting
            self.crafting_menu()
        elif choice == 7:  # Shop
            self.shop_menu()
        elif choice == 8:  # Rest
            self.rest()
        elif choice == 9:  # Save Game
            self.save_game()
        elif choice == 10:  # Settings
            self.settings_menu()
        elif choice == 11:  # Quit
            self.quit_game()

    def view_character(self):
        """Display character stats."""
        clear_screen()
        print(self.game_state.character.display_stats())

        if self.game_state.character.stat_points > 0:
            if get_yes_no("\nWould you like to allocate stat points?"):
                self.allocate_stats()

        pause()

    def allocate_stats(self):
        """Stat allocation menu."""
        char = self.game_state.character

        while char.stat_points > 0:
            clear_screen()
            print(f"\nStat Points Available: {char.stat_points}\n")
            print(f"1. Max HP: {char.get_stat('max_hp')}")
            print(f"2. Strength: {char.get_stat('strength')}")
            print(f"3. Defense: {char.get_stat('defense')}")
            print(f"4. Agility: {char.get_stat('agility')}")
            print(f"5. Intelligence: {char.get_stat('intelligence')}")
            print(f"6. Luck: {char.get_stat('luck')}")
            print("0. Done")

            choice = get_number("\nAllocate to which stat? ", min_val=0, max_val=6)

            if choice == 0:
                break

            points = get_number(f"How many points? (1-{char.stat_points}): ",
                                min_val=1, max_val=char.stat_points)

            stat_map = {
                1: 'max_hp',
                2: 'strength',
                3: 'defense',
                4: 'agility',
                5: 'intelligence',
                6: 'luck'
            }

            if char.allocate_stat(stat_map[choice], points):
                print(f"\nAllocated {points} points to {stat_map[choice]}!")
            else:
                print("\nFailed to allocate points.")

            pause()

    def inventory_menu(self):
        """Inventory management menu."""
        while True:
            clear_screen()
            print(self.game_state.inventory.display())

            options = [
                "Use Item",
                "Equip Item",
                "Unequip Item",
                "Drop Item",
                "Back"
            ]

            choice = display_menu("INVENTORY", options, allow_back=False)

            if choice == 0:  # Use Item
                self.use_item()
            elif choice == 1:  # Equip Item
                self.equip_item()
            elif choice == 2:  # Unequip Item
                self.unequip_item()
            elif choice == 3:  # Drop Item
                self.drop_item()
            elif choice == 4:  # Back
                break

    def use_item(self):
        """Use a consumable item."""
        consumables = self.game_state.inventory.get_items_by_type(ItemType.CONSUMABLE)

        if not consumables:
            print("\nNo consumable items.")
            pause()
            return

        print("\nConsumable Items:")
        for i, (item, qty) in enumerate(consumables, 1):
            print(f"{i}. {item.name} x{qty} - {item.description}")

        print("0. Cancel")

        choice = get_number("\nUse which item? ", min_val=0, max_val=len(consumables))

        if choice == 0:
            return

        item, qty = consumables[choice - 1]

        # Use the item
        msg = item.use(self.game_state.character)
        print(f"\n{msg}")

        # Remove from inventory
        self.game_state.inventory.remove_item(item.item_id, 1)

        pause()

    def equip_item(self):
        """Equip an equipment item."""
        equipment = (
            self.game_state.inventory.get_items_by_type(ItemType.WEAPON) +
            self.game_state.inventory.get_items_by_type(ItemType.ARMOR) +
            self.game_state.inventory.get_items_by_type(ItemType.ACCESSORY)
        )

        if not equipment:
            print("\nNo equipment to equip.")
            pause()
            return

        print("\nEquipment:")
        for i, (item, qty) in enumerate(equipment, 1):
            can_equip = item.can_equip(self.game_state.character)
            status = "✓" if can_equip else "✗"
            print(f"{i}. {status} {item.name} - {item.description}")

        print("0. Cancel")

        choice = get_number("\nEquip which item? ", min_val=0, max_val=len(equipment))

        if choice == 0:
            return

        item, qty = equipment[choice - 1]

        if not item.can_equip(self.game_state.character):
            print(f"\nCannot equip {item.name}. Level {item.level_requirement} required.")
            pause()
            return

        # Determine slot
        slot_map = {
            ItemType.WEAPON: 'weapon',
            ItemType.ARMOR: 'armor',
            ItemType.ACCESSORY: 'accessory'
        }

        slot = slot_map[item.item_type]

        # Remove from inventory
        self.game_state.inventory.remove_item(item.item_id, 1)

        # Equip
        old_item = self.game_state.character.equip_item(item, slot)

        # Add old item back to inventory
        if old_item:
            self.game_state.inventory.add_item(old_item.item_id, 1)

        print(f"\nEquipped {item.name}!")
        pause()

    def unequip_item(self):
        """Unequip an equipped item."""
        char = self.game_state.character

        equipped_items = []
        for slot, item in char.equipped.items():
            if item:
                equipped_items.append((slot, item))

        if not equipped_items:
            print("\nNo items equipped.")
            pause()
            return

        print("\nEquipped Items:")
        for i, (slot, item) in enumerate(equipped_items, 1):
            print(f"{i}. {item.name} ({slot})")

        print("0. Cancel")

        choice = get_number("\nUnequip which item? ", min_val=0, max_val=len(equipped_items))

        if choice == 0:
            return

        slot, item = equipped_items[choice - 1]

        if self.game_state.inventory.is_full():
            print("\nInventory is full!")
            pause()
            return

        # Unequip
        unequipped = char.unequip_item(slot)

        # Add to inventory
        self.game_state.inventory.add_item(unequipped.item_id, 1)

        print(f"\nUnequipped {unequipped.name}!")
        pause()

    def drop_item(self):
        """Drop an item from inventory."""
        all_items = self.game_state.inventory.get_all_items()

        if not all_items:
            print("\nInventory is empty.")
            pause()
            return

        print("\nItems:")
        for i, (item, qty) in enumerate(all_items, 1):
            print(f"{i}. {item.name} x{qty}")

        print("0. Cancel")

        choice = get_number("\nDrop which item? ", min_val=0, max_val=len(all_items))

        if choice == 0:
            return

        item, qty = all_items[choice - 1]

        if qty > 1:
            amount = get_number(f"Drop how many? (1-{qty}): ", min_val=1, max_val=qty)
        else:
            amount = 1

        if get_yes_no(f"Are you sure you want to drop {amount}x {item.name}?", default=False):
            self.game_state.inventory.remove_item(item.item_id, amount)
            print(f"\nDropped {amount}x {item.name}.")

        pause()

    def travel_menu(self):
        """Travel to a new location."""
        clear_screen()

        current = self.game_state.world.get_current_location()
        if current:
            print(display_location(current, detailed=True))

        destinations = self.game_state.world.get_available_destinations()

        if not destinations:
            print("\nNo destinations available.")
            pause()
            return

        print(display_travel_options(self.game_state.world))

        print(f"{len(destinations) + 1}. Stay here")

        choice = get_number("\nTravel to: ", min_val=1, max_val=len(destinations) + 1)

        if choice == len(destinations) + 1:
            return

        destination = destinations[choice - 1]

        loading_animation(f"Traveling to {destination.name}")

        if self.game_state.world.move_to(destination.location_id):
            print(f"\nArrived at {destination.name}!")

            # Update quest progress
            self.game_state.quest_manager.update_quest_progress(
                ObjectiveType.VISIT_LOCATION,
                destination.location_id
            )

            # Check for random encounter
            encounter = self.game_state.world.trigger_random_encounter()
            if encounter:
                print("\n⚠️ Random encounter!")
                pause()
                enemy = create_enemy(encounter)
                if enemy:
                    self.combat(enemy)
        else:
            print("\nCannot travel there.")

        pause()

    def search_for_combat(self):
        """Actively search for enemies."""
        clear_screen()

        char = self.game_state.character
        location = self.game_state.world.get_current_location()

        if not location or not location.enemy_encounters:
            print("\nNo enemies in this area.")
            pause()
            return

        print("\nSearching for enemies...")
        loading_animation("Searching", duration=1.5)

        # Always find an enemy when actively searching
        enemy_id = location.get_random_enemy()

        if enemy_id:
            enemy = create_enemy(enemy_id)
            if enemy:
                print(f"\n⚔️ You encounter a {enemy.name}!")
                pause()
                self.combat(enemy)
        else:
            print("\nNo enemies found.")
            pause()

    def combat(self, enemy):
        """Run a combat encounter."""
        combat = Combat(self.game_state.character, enemy)

        while combat.result == CombatResult.ONGOING:
            clear_screen()
            print(combat.get_status())

            # Show recent log
            if combat.combat_log:
                print("\nCombat Log:")
                for msg in combat.combat_log[-5:]:
                    print(f"  {msg}")

            print("\n")
            options = [
                "⚔️ Attack",
                "🛡️  Defend",
                "🧪 Use Item",
                "🏃 Flee"
            ]

            choice = display_menu("COMBAT ACTION", options, allow_back=False)

            item_to_use = None

            if choice == 0:  # Attack
                action = CombatAction.ATTACK
            elif choice == 1:  # Defend
                action = CombatAction.DEFEND
            elif choice == 2:  # Use Item
                item_to_use = self.select_combat_item()
                if not item_to_use:
                    continue
                action = CombatAction.USE_ITEM
            elif choice == 3:  # Flee
                action = CombatAction.FLEE

            # Execute turn
            messages = combat.execute_turn(action, item_to_use)

            # Show turn results
            for msg in messages:
                print(f"\n{msg}")

            pause("\nPress Enter to continue...")

        # Combat ended
        clear_screen()

        if combat.result == CombatResult.VICTORY:
            rewards = combat.get_rewards()
            display_combat_result(True, rewards)

            # Grant rewards
            leveled_up = self.game_state.character.add_xp(rewards['xp'])
            self.game_state.character.add_gold(rewards['gold'])

            # Add loot
            for item_id in rewards['loot']:
                if not self.game_state.inventory.is_full():
                    self.game_state.inventory.add_item(item_id, 1)

            # Update quest progress
            self.game_state.quest_manager.update_quest_progress(
                ObjectiveType.KILL_ENEMY,
                enemy.enemy_id
            )

            # Check for level up
            if leveled_up:
                display_level_up(self.game_state.character)
                self.allocate_stats()

        elif combat.result == CombatResult.DEFEAT:
            display_combat_result(False)

        elif combat.result == CombatResult.FLED:
            print("\nYou fled from combat!")

        pause()

    def select_combat_item(self) -> Optional[object]:
        """Select an item to use in combat."""
        consumables = self.game_state.inventory.get_items_by_type(ItemType.CONSUMABLE)

        if not consumables:
            print("\nNo items to use.")
            pause()
            return None

        print("\nSelect item to use:")
        for i, (item, qty) in enumerate(consumables, 1):
            print(f"{i}. {item.name} x{qty}")

        print("0. Cancel")

        choice = get_number("Use which item? ", min_val=0, max_val=len(consumables))

        if choice == 0:
            return None

        item, qty = consumables[choice - 1]

        # Remove from inventory
        self.game_state.inventory.remove_item(item.item_id, 1)

        return item

    def explore_area(self):
        """Explore the current area for treasures."""
        clear_screen()

        location = self.game_state.world.get_current_location()

        if not location:
            print("\nNowhere to explore.")
            pause()
            return

        print(f"\nExploring {location.name}...")
        loading_animation("Searching", duration=2.0)

        # Check for treasure
        if location.has_available_treasure():
            treasure_id = location.get_treasure()

            if treasure_id:
                treasure = get_item(treasure_id)

                if treasure and not self.game_state.inventory.is_full():
                    self.game_state.inventory.add_item(treasure_id, 1)
                    print(f"\n💎 Found treasure: {treasure.name}!")

                    # Update quest progress
                    self.game_state.quest_manager.update_quest_progress(
                        ObjectiveType.COLLECT_ITEM,
                        treasure_id
                    )

                    # Discover crafting recipe randomly
                    if random.random() < 0.3:
                        all_recipes = list(self.game_state.crafting_system.recipes.keys())
                        undiscovered = [
                            r for r in all_recipes
                            if r not in self.game_state.crafting_system.discovered_recipes
                        ]

                        if undiscovered:
                            recipe_id = random.choice(undiscovered)
                            if self.game_state.crafting_system.discover_recipe(recipe_id):
                                recipe = self.game_state.crafting_system.get_recipe(recipe_id)
                                print(f"\n📜 Discovered recipe: {recipe.name}!")
                else:
                    print("\n💎 Found treasure, but inventory is full!")
            else:
                print("\nNothing found.")
        else:
            print("\nNothing found. This area has been thoroughly searched.")

        # Random encounter chance
        if random.random() < 0.3:
            enemy_id = location.get_random_enemy()
            if enemy_id:
                print("\n⚠️ Enemy ambush!")
                pause()
                enemy = create_enemy(enemy_id)
                if enemy:
                    self.combat(enemy)
                return

        pause()

    def quest_menu(self):
        """Quest management menu."""
        while True:
            clear_screen()

            options = [
                "View Active Quests",
                "View Available Quests",
                "Complete Quest",
                "Back"
            ]

            choice = display_menu("QUESTS", options, allow_back=False)

            if choice == 0:  # View Active
                self.view_active_quests()
            elif choice == 1:  # View Available
                self.view_available_quests()
            elif choice == 2:  # Complete
                self.complete_quest()
            elif choice == 3:  # Back
                break

    def view_active_quests(self):
        """View all active quests."""
        clear_screen()

        quests = self.game_state.quest_manager.get_active_quests()

        if not quests:
            print("\nNo active quests.")
            pause()
            return

        for quest in quests:
            print(quest.get_progress_display())

        pause()

    def view_available_quests(self):
        """View and accept available quests."""
        clear_screen()

        quests = self.game_state.quest_manager.get_available_quests(
            self.game_state.character
        )

        if not quests:
            print("\nNo quests available.")
            pause()
            return

        print("\nAvailable Quests:")
        for i, quest in enumerate(quests, 1):
            print(f"\n{i}. {quest.name} (Lv.{quest.level_requirement})")
            print(f"   {quest.description}")
            print(f"   Rewards: {quest.xp_reward} XP, {quest.gold_reward} Gold")

        print("0. Back")

        choice = get_number("\nAccept which quest? ", min_val=0, max_val=len(quests))

        if choice == 0:
            return

        quest = quests[choice - 1]

        if self.game_state.quest_manager.start_quest(quest.quest_id):
            print(f"\n✓ Accepted quest: {quest.name}")
        else:
            print("\nFailed to accept quest.")

        pause()

    def complete_quest(self):
        """Complete a finished quest."""
        clear_screen()

        completable = self.game_state.quest_manager.get_completable_quests()

        if not completable:
            print("\nNo quests ready to complete.")
            pause()
            return

        print("\nCompletable Quests:")
        for i, quest in enumerate(completable, 1):
            print(f"{i}. {quest.name}")

        print("0. Cancel")

        choice = get_number("\nComplete which quest? ", min_val=0, max_val=len(completable))

        if choice == 0:
            return

        quest = completable[choice - 1]

        completed_quest = self.game_state.quest_manager.complete_quest(quest.quest_id)

        if completed_quest:
            print_header(f"✓ QUEST COMPLETE: {completed_quest.name}", "*", 60)

            # Grant rewards
            leveled_up = self.game_state.character.add_xp(completed_quest.xp_reward)
            self.game_state.character.add_gold(completed_quest.gold_reward)

            print(f"\nRewards:")
            print(f"  • {completed_quest.xp_reward} XP")
            print(f"  • {completed_quest.gold_reward} Gold")

            for item_id in completed_quest.item_rewards:
                if not self.game_state.inventory.is_full():
                    self.game_state.inventory.add_item(item_id, 1)
                    item = get_item(item_id)
                    if item:
                        print(f"  • {item.name}")

            print_separator("*", 60)

            if leveled_up:
                display_level_up(self.game_state.character)
                self.allocate_stats()
        else:
            print("\nFailed to complete quest.")

        pause()

    def crafting_menu(self):
        """Crafting menu."""
        while True:
            clear_screen()

            options = [
                "View Recipes",
                "Craft Item",
                "Back"
            ]

            choice = display_menu("CRAFTING", options, allow_back=False)

            if choice == 0:  # View Recipes
                clear_screen()
                print(self.game_state.crafting_system.display_recipes(
                    self.game_state.character,
                    self.game_state.inventory
                ))
                pause()
            elif choice == 1:  # Craft Item
                self.craft_item()
            elif choice == 2:  # Back
                break

    def craft_item(self):
        """Craft an item."""
        clear_screen()

        recipes = self.game_state.crafting_system.get_discovered_recipes()

        if not recipes:
            print("\nNo recipes discovered.")
            pause()
            return

        print("\nRecipes:")
        for i, recipe in enumerate(recipes, 1):
            can_craft, reason = recipe.can_craft(
                self.game_state.character,
                self.game_state.inventory
            )
            status = "✓" if can_craft else "✗"
            print(f"{i}. {status} {recipe.name} -> {recipe.get_result_display()}")
            print(f"   Materials: {recipe.get_materials_display()}")
            if not can_craft:
                print(f"   ({reason})")

        print("0. Cancel")

        choice = get_number("\nCraft which recipe? ", min_val=0, max_val=len(recipes))

        if choice == 0:
            return

        recipe = recipes[choice - 1]

        can_craft, reason = recipe.can_craft(
            self.game_state.character,
            self.game_state.inventory
        )

        if not can_craft:
            print(f"\nCannot craft: {reason}")
            pause()
            return

        if self.game_state.inventory.is_full():
            print("\nInventory is full!")
            pause()
            return

        loading_animation("Crafting", duration=1.5)

        if recipe.craft(self.game_state.inventory):
            result_item = get_item(recipe.result_item_id)
            print(f"\n✓ Crafted {result_item.name}!")
        else:
            print("\nFailed to craft item.")

        pause()

    def shop_menu(self):
        """Shop menu."""
        location = self.game_state.world.get_current_location()

        if not location or not location.has_shop:
            print("\nNo shop in this location.")
            pause()
            return

        # Determine which shop to show based on location
        shop = self.shops['general']  # Default

        while True:
            clear_screen()

            options = [
                "Buy Items",
                "Sell Items",
                "Back"
            ]

            choice = display_menu("SHOP", options, allow_back=False)

            if choice == 0:  # Buy
                self.buy_items(shop)
            elif choice == 1:  # Sell
                self.sell_items(shop)
            elif choice == 2:  # Back
                break

    def buy_items(self, shop):
        """Buy items from shop."""
        clear_screen()
        print(shop.display_stock())

        print(f"\nYour gold: {self.game_state.character.gold}g")

        # Build item list
        items = []
        for item_id, quantity in shop.inventory.items():
            if quantity != 0:
                item = get_item(item_id)
                if item:
                    items.append((item_id, item, quantity))

        if not items:
            print("\nShop is empty.")
            pause()
            return

        print("\nItems:")
        for i, (item_id, item, qty) in enumerate(items, 1):
            price = shop.get_buy_price(item_id)
            stock = f"({qty} left)" if qty > 0 else "(Unlimited)"
            print(f"{i}. {item.name} - {price}g {stock}")

        print("0. Cancel")

        choice = get_number("\nBuy which item? ", min_val=0, max_val=len(items))

        if choice == 0:
            return

        item_id, item, qty = items[choice - 1]

        success, msg = shop.buy_item(item_id, self.game_state.character, self.game_state.inventory)
        print(f"\n{msg}")

        pause()

    def sell_items(self, shop):
        """Sell items to shop."""
        clear_screen()

        all_items = self.game_state.inventory.get_all_items()

        if not all_items:
            print("\nNothing to sell.")
            pause()
            return

        # Filter out quest items
        sellable = [(item, qty) for item, qty in all_items if item.item_type != ItemType.QUEST]

        if not sellable:
            print("\nNothing to sell.")
            pause()
            return

        print("Items:")
        for i, (item, qty) in enumerate(sellable, 1):
            price = shop.get_sell_price(item.item_id)
            print(f"{i}. {item.name} x{qty} - {price}g each")

        print("0. Cancel")

        choice = get_number("\nSell which item? ", min_val=0, max_val=len(sellable))

        if choice == 0:
            return

        item, qty = sellable[choice - 1]

        success, msg = shop.sell_item(item.item_id, self.game_state.character, self.game_state.inventory)
        print(f"\n{msg}")

        pause()

    def rest(self):
        """Rest at an inn or camp."""
        clear_screen()

        location = self.game_state.world.get_current_location()

        if location and location.has_inn:
            cost = 20
            print(f"\nRest at the inn? (Costs {cost} gold)")
            print("Restores full HP and grants temporary bonuses.")

            if self.game_state.character.gold < cost:
                print("\nNot enough gold!")
                pause()
                return

            if get_yes_no("\nRest at inn?"):
                self.game_state.character.remove_gold(cost)
                self.game_state.character.heal(999999)
                print("\nYou rest at the inn and wake up fully refreshed!")
        else:
            print("\nYou rest in the wilderness...")
            loading_animation("Resting", duration=2.0)

            # Restore some HP
            heal_amount = self.game_state.character.get_max_hp() // 2
            self.game_state.character.heal(heal_amount)

            print(f"\nRestored {heal_amount} HP.")

            # Random encounter chance
            if random.random() < 0.2:
                print("\n⚠️ Ambushed while resting!")
                pause()

                char_level = self.game_state.character.level
                enemy = get_random_enemy_for_level(char_level)
                self.combat(enemy)
                return

        pause()

    def save_game(self):
        """Save the game."""
        clear_screen()
        print_header("SAVE GAME", "=", 60)

        save_name = input("\nEnter save name: ").strip()

        if not save_name:
            save_name = f"{self.game_state.character.name}_save"

        loading_animation("Saving game")

        if self.game_state.save_game(save_name):
            print("\n✓ Game saved successfully!")
        else:
            print("\n✗ Failed to save game.")

        pause()

    def settings_menu(self):
        """Settings menu."""
        clear_screen()

        options = [
            "View All Saves",
            "Delete Save",
            "Back"
        ]

        choice = display_menu("SETTINGS", options, allow_back=False)

        if choice == 0:  # View Saves
            self.view_saves()
        elif choice == 1:  # Delete Save
            self.delete_save()

    def view_saves(self):
        """View all saved games."""
        clear_screen()

        saves = SaveGame.get_all_saves()

        if not saves:
            print("\nNo saves found.")
            pause()
            return

        print("\nSaved Games:")
        for save in saves:
            timestamp = save['timestamp'].split('T')[0]
            print(f"  • {save['character_name']} (Lv.{save['level']}) - {timestamp}")

        pause()

    def delete_save(self):
        """Delete a save file."""
        clear_screen()

        saves = SaveGame.get_all_saves()

        if not saves:
            print("\nNo saves to delete.")
            pause()
            return

        print("\nSaved Games:")
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save['character_name']} (Lv.{save['level']})")

        print("0. Cancel")

        choice = get_number("\nDelete which save? ", min_val=0, max_val=len(saves))

        if choice == 0:
            return

        save = saves[choice - 1]

        if get_yes_no(f"Delete {save['character_name']}?", default=False):
            if SaveGame.delete_save(save['save_name']):
                print("\n✓ Save deleted.")
            else:
                print("\n✗ Failed to delete save.")

        pause()

    def quit_game(self):
        """Quit the game."""
        if get_yes_no("\nSave before quitting?"):
            self.save_game()

        print("\nThanks for playing Epic Quest!")
        self.running = False
        sys.exit(0)

    def game_over(self):
        """Handle game over."""
        display_game_over()

        if get_yes_no("\nLoad last save?"):
            if self.load_game_menu():
                self.main_loop()
        else:
            print("\nThanks for playing!")
            sys.exit(0)


def main():
    """Main entry point."""
    try:
        game = Game()
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
