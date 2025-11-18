"""
Test suite for Epic Quest game.
Run with: python test_game.py
"""

import unittest
from character import Character
from inventory import Inventory
from items import create_item, ItemType
from combat import create_enemy, Combat, CombatAction, CombatResult
from world import create_game_world
from quest import create_all_quests, ObjectiveType
from crafting import create_crafting_system


class TestCharacter(unittest.TestCase):
    """Test character functionality."""

    def setUp(self):
        self.char = Character("Test Hero")

    def test_character_creation(self):
        """Test character is created with correct defaults."""
        self.assertEqual(self.char.name, "Test Hero")
        self.assertEqual(self.char.level, 1)
        self.assertEqual(self.char.base_stats['hp'], 100)
        self.assertTrue(self.char.is_alive)

    def test_take_damage(self):
        """Test damage calculation."""
        initial_hp = self.char.base_stats['hp']
        damage = self.char.take_damage(20)
        self.assertLess(self.char.base_stats['hp'], initial_hp)
        self.assertGreater(damage, 0)

    def test_healing(self):
        """Test healing."""
        self.char.take_damage(50)
        healed = self.char.heal(30)
        self.assertEqual(healed, 30)

    def test_level_up(self):
        """Test leveling up."""
        initial_level = self.char.level
        self.char.xp = self.char.xp_to_next_level
        leveled = self.char.level_up()
        self.assertTrue(leveled)
        self.assertEqual(self.char.level, initial_level + 1)
        self.assertGreater(self.char.stat_points, 0)

    def test_stat_allocation(self):
        """Test stat point allocation."""
        self.char.stat_points = 5
        initial_str = self.char.base_stats['strength']
        success = self.char.allocate_stat('strength', 3)
        self.assertTrue(success)
        self.assertEqual(self.char.stat_points, 2)
        self.assertEqual(self.char.base_stats['strength'], initial_str + 3)

    def test_equipment(self):
        """Test equipping items."""
        weapon = create_item('iron_sword')
        self.assertIsNotNone(weapon)

        old = self.char.equip_item(weapon, 'weapon')
        self.assertIsNone(old)
        self.assertEqual(self.char.equipped['weapon'], weapon)

        # Stats should increase
        self.assertGreater(self.char.get_stat('strength'),
                           self.char.base_stats['strength'])

    def test_gold(self):
        """Test gold management."""
        initial_gold = self.char.gold
        self.char.add_gold(100)
        self.assertEqual(self.char.gold, initial_gold + 100)

        success = self.char.remove_gold(50)
        self.assertTrue(success)
        self.assertEqual(self.char.gold, initial_gold + 50)

        success = self.char.remove_gold(1000)
        self.assertFalse(success)


class TestInventory(unittest.TestCase):
    """Test inventory functionality."""

    def setUp(self):
        self.inventory = Inventory(max_capacity=20)

    def test_add_item(self):
        """Test adding items."""
        success = self.inventory.add_item('health_potion_small', 3)
        self.assertTrue(success)
        self.assertEqual(self.inventory.get_item_count('health_potion_small'), 3)

    def test_remove_item(self):
        """Test removing items."""
        self.inventory.add_item('health_potion_small', 5)
        success = self.inventory.remove_item('health_potion_small', 2)
        self.assertTrue(success)
        self.assertEqual(self.inventory.get_item_count('health_potion_small'), 3)

    def test_capacity(self):
        """Test inventory capacity limits."""
        # Fill inventory
        for i in range(20):
            self.inventory.add_item('health_potion_small', 1)

        self.assertTrue(self.inventory.is_full())

        # Should fail to add more
        success = self.inventory.add_item('health_potion_medium', 1)
        self.assertFalse(success)

    def test_has_item(self):
        """Test checking for items."""
        self.inventory.add_item('iron_sword', 1)
        self.assertTrue(self.inventory.has_item('iron_sword'))
        self.assertFalse(self.inventory.has_item('steel_sword'))

    def test_get_items_by_type(self):
        """Test filtering items by type."""
        self.inventory.add_item('health_potion_small', 2)
        self.inventory.add_item('iron_sword', 1)

        consumables = self.inventory.get_items_by_type(ItemType.CONSUMABLE)
        self.assertEqual(len(consumables), 1)
        self.assertEqual(consumables[0][1], 2)  # quantity


class TestItems(unittest.TestCase):
    """Test item system."""

    def test_create_item(self):
        """Test item creation."""
        item = create_item('iron_sword')
        self.assertIsNotNone(item)
        self.assertEqual(item.name, "Iron Sword")

    def test_weapon_stats(self):
        """Test weapon has correct stats."""
        weapon = create_item('steel_sword')
        self.assertIsNotNone(weapon)
        self.assertGreater(weapon.damage, 0)
        self.assertIn('strength', weapon.stats)

    def test_consumable_use(self):
        """Test using consumable."""
        potion = create_item('health_potion_small')
        char = Character("Test")
        char.take_damage(50)

        initial_hp = char.base_stats['hp']
        msg = potion.use(char)
        self.assertGreater(char.base_stats['hp'], initial_hp)
        self.assertIn("Healed", msg)

    def test_equipment_requirements(self):
        """Test equipment level requirements."""
        char = Character("Test")
        char.level = 3

        low_level_item = create_item('iron_sword')
        self.assertTrue(low_level_item.can_equip(char))

        high_level_item = create_item('dragon_slayer')
        self.assertFalse(high_level_item.can_equip(char))


class TestCombat(unittest.TestCase):
    """Test combat system."""

    def setUp(self):
        self.char = Character("Test Hero")
        self.enemy = create_enemy('slime')

    def test_enemy_creation(self):
        """Test enemy creation."""
        self.assertIsNotNone(self.enemy)
        self.assertEqual(self.enemy.name, "Slime")
        self.assertTrue(self.enemy.is_alive())

    def test_combat_creation(self):
        """Test combat initialization."""
        combat = Combat(self.char, self.enemy)
        self.assertIsNotNone(combat)
        self.assertEqual(combat.turn_count, 0)

    def test_player_attack(self):
        """Test player attack."""
        combat = Combat(self.char, self.enemy)
        initial_enemy_hp = self.enemy.hp

        msg = combat.player_attack()
        self.assertLess(self.enemy.hp, initial_enemy_hp)
        self.assertIn("damage", msg.lower())

    def test_enemy_attack(self):
        """Test enemy attack."""
        combat = Combat(self.char, self.enemy)
        initial_player_hp = self.char.base_stats['hp']

        msg = combat.enemy_attack()
        # Player might dodge, so check for either damage or dodge
        self.assertTrue("damage" in msg.lower() or "dodge" in msg.lower())

    def test_combat_victory(self):
        """Test combat victory."""
        # Create weak enemy
        weak_enemy = create_enemy('slime')
        weak_enemy.hp = 1

        combat = Combat(self.char, weak_enemy)
        combat.execute_turn(CombatAction.ATTACK)

        self.assertFalse(weak_enemy.is_alive())


class TestWorld(unittest.TestCase):
    """Test world and location system."""

    def setUp(self):
        self.world = create_game_world()

    def test_world_creation(self):
        """Test world is created with locations."""
        self.assertIsNotNone(self.world)
        self.assertGreater(len(self.world.locations), 0)

    def test_starting_location(self):
        """Test starting location is set."""
        current = self.world.get_current_location()
        self.assertIsNotNone(current)
        self.assertEqual(current.location_id, "hometown")

    def test_travel(self):
        """Test traveling between locations."""
        destinations = self.world.get_available_destinations()
        self.assertGreater(len(destinations), 0)

        dest = destinations[0]
        success = self.world.move_to(dest.location_id)
        self.assertTrue(success)
        self.assertEqual(self.world.current_location_id, dest.location_id)

    def test_invalid_travel(self):
        """Test cannot travel to unconnected location."""
        success = self.world.move_to("invalid_location_id")
        self.assertFalse(success)

    def test_location_features(self):
        """Test location has expected features."""
        hometown = self.world.get_location("hometown")
        self.assertIsNotNone(hometown)
        self.assertTrue(hometown.has_shop)
        self.assertTrue(hometown.has_inn)


class TestQuests(unittest.TestCase):
    """Test quest system."""

    def setUp(self):
        self.quest_manager = create_all_quests()
        self.char = Character("Test Hero")

    def test_quest_manager_creation(self):
        """Test quest manager has quests."""
        self.assertGreater(len(self.quest_manager.available_quests), 0)

    def test_start_quest(self):
        """Test starting a quest."""
        available = self.quest_manager.get_available_quests(self.char)
        self.assertGreater(len(available), 0)

        quest = available[0]
        success = self.quest_manager.start_quest(quest.quest_id)
        self.assertTrue(success)
        self.assertIn(quest.quest_id, self.quest_manager.active_quests)

    def test_quest_progress(self):
        """Test quest progress tracking."""
        # Start first quest
        quest = self.quest_manager.get_quest('first_steps')
        if quest:
            self.quest_manager.start_quest('first_steps')

            # Update progress
            self.quest_manager.update_quest_progress(
                ObjectiveType.KILL_ENEMY, 'slime', 3
            )

            # Check if completable
            completable = self.quest_manager.get_completable_quests()
            self.assertGreater(len(completable), 0)

    def test_quest_completion(self):
        """Test completing a quest."""
        quest = self.quest_manager.get_quest('first_steps')
        if quest:
            self.quest_manager.start_quest('first_steps')

            # Manually complete objectives
            for obj in quest.objectives:
                obj.completed = True

            # Complete quest
            completed = self.quest_manager.complete_quest('first_steps')
            self.assertIsNotNone(completed)
            self.assertIn('first_steps', self.quest_manager.completed_quests)


class TestCrafting(unittest.TestCase):
    """Test crafting system."""

    def setUp(self):
        self.crafting = create_crafting_system()
        self.char = Character("Test")
        self.inventory = Inventory()

    def test_crafting_system_creation(self):
        """Test crafting system has recipes."""
        self.assertGreater(len(self.crafting.recipes), 0)

    def test_discover_recipe(self):
        """Test recipe discovery."""
        recipe_id = 'craft_steel_sword'
        discovered = self.crafting.discover_recipe(recipe_id)
        self.assertTrue(discovered)
        self.assertIn(recipe_id, self.crafting.discovered_recipes)

    def test_craft_item(self):
        """Test crafting an item."""
        # Discover and prepare to craft iron sword
        self.crafting.discover_recipe('craft_iron_sword')

        # Set level requirement
        self.char.level = 2

        # Add materials
        self.inventory.add_item('iron_ore', 3)
        self.inventory.add_item('wood_plank', 1)

        recipe = self.crafting.get_recipe('craft_iron_sword')
        can_craft, _ = recipe.can_craft(self.char, self.inventory)
        self.assertTrue(can_craft)

        # Craft
        success = recipe.craft(self.inventory)
        self.assertTrue(success)

        # Check result
        self.assertTrue(self.inventory.has_item('iron_sword'))

    def test_cannot_craft_without_materials(self):
        """Test cannot craft without materials."""
        self.crafting.discover_recipe('craft_iron_sword')

        # Set level to meet requirement
        self.char.level = 2

        recipe = self.crafting.get_recipe('craft_iron_sword')
        can_craft, reason = recipe.can_craft(self.char, self.inventory)

        self.assertFalse(can_craft)
        # Should fail due to missing materials
        self.assertTrue("Need" in reason or "level" in reason.lower())


class TestIntegration(unittest.TestCase):
    """Integration tests for game systems."""

    def test_combat_rewards(self):
        """Test combat gives proper rewards."""
        char = Character("Test")
        inventory = Inventory()
        enemy = create_enemy('slime')

        initial_xp = char.xp
        initial_gold = char.gold

        # Simulate victory
        combat = Combat(char, enemy)
        combat.result = CombatResult.VICTORY

        rewards = combat.get_rewards()

        self.assertGreater(rewards['xp'], 0)
        self.assertGreater(rewards['gold'], 0)

    def test_equipment_affects_combat(self):
        """Test equipment improves combat performance."""
        char = Character("Test")

        base_damage = char.get_attack_damage()

        # Equip weapon
        weapon = create_item('iron_sword')
        char.equip_item(weapon, 'weapon')

        equipped_damage = char.get_attack_damage()

        self.assertGreater(equipped_damage, base_damage)

    def test_quest_item_collection(self):
        """Test collecting quest items."""
        quest_manager = create_all_quests()
        char = Character("Test")

        # Start goblin quest
        quest = quest_manager.get_quest('goblin_threat')
        if quest:
            char.level = quest.level_requirement
            quest_manager.start_quest('goblin_threat')

            # Simulate killing goblin chief and getting item
            quest_manager.update_quest_progress(
                ObjectiveType.KILL_ENEMY, 'goblin_chief', 1
            )
            quest_manager.update_quest_progress(
                ObjectiveType.COLLECT_ITEM, 'goblin_chief_head', 1
            )

            # Check if completable
            self.assertTrue(quest.check_completion())


def run_tests():
    """Run all tests."""
    print("="*60)
    print("Running Epic Quest Test Suite")
    print("="*60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCharacter))
    suite.addTests(loader.loadTestsFromTestCase(TestInventory))
    suite.addTests(loader.loadTestsFromTestCase(TestItems))
    suite.addTests(loader.loadTestsFromTestCase(TestCombat))
    suite.addTests(loader.loadTestsFromTestCase(TestWorld))
    suite.addTests(loader.loadTestsFromTestCase(TestQuests))
    suite.addTests(loader.loadTestsFromTestCase(TestCrafting))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)

    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
