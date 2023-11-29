import sys
import os
CURRENT_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(PARENT_DIR))
from game.gamefiles import item
import unittest

class TestItem(unittest.TestCase):

    def test_init(self):
        """Test that an Item instance is initialized properly"""
        effects = {'ATK': 10, 'DEF': 5}
        item = item.Item('Potion', 0, 5, effects)
        
        self.assertEqual(item.name, 'Potion')
        self.assertEqual(item.cat, 0) 
        self.assertEqual(item.uses, 5)
        self.assertEqual(item.effects, effects)
        
    def test_str(self):
        """Test the string representation is formatted correctly"""
        effects = {'ATK': 10, 'DEF': 5} 
        item = item.Item('Potion', 0, 5, effects)
        
        expected = "Potion - Type: 0 Uses: 5, Effects [ATK: 10 DEF: 5 ]"
        self.assertEqual(str(item), expected)
        
    def test_validate_effects(self):
        """Test validate_effects method"""
        valid_effects = {'ATK': 10, 'DEF': 5}
        invalid_effects = {'ATK': 100, 'DEF': 5}
        
        valid_item = item.Item('Potion', 0, 5, valid_effects)
        self.assertTrue(valid_item.validate_effects())
        
        invalid_item = item.Item('Potion', 0, 5, invalid_effects) 
        self.assertFalse(invalid_item.validate_effects())
        
    def test_use(self):
        """Test use method under different conditions"""
        effects = {'ATK': 10, 'DEF': 5}
        usable_item = item.Item('Potion', 0, 5, effects)
        broken_item = item.Item('Potion', 0, 0, effects)
        infinite_item = item.Item('Potion', 0, -99, effects)
        
        self.assertEqual(usable_item.use(), effects)
        self.assertEqual(usable_item.uses, 4)
        
        self.assertEqual(broken_item.use(), {})
        
        self.assertEqual(infinite_item.use(), effects)
        self.assertEqual(infinite_item.uses, -99)
        
if __name__ == '__main__':
    unittest.main()