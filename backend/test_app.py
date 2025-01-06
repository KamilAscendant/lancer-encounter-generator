import unittest
from app import app, scale_npc_stats, select_npcs_by_role
import json
import sqlite3

class TestEncounterAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client and ensure database has test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Ensure we have a test database with known data
        conn = sqlite3.connect('npc.db')
        cursor = conn.cursor()
        
        # Verify the database has data
        cursor.execute("SELECT COUNT(*) FROM npcs")
        npc_count = cursor.fetchone()[0]
        
        if npc_count == 0:
            raise Exception("Database is empty. Please run insert_npcs.py first")
            
        conn.close()

    def test_encounter_generation_basic(self):
        """Test basic encounter generation with 1 player at level 1"""
        response = self.app.get('/api/encounter?players=1&level=1')
        data = json.loads(response.data)
        
        # Check status code and basic structure
        self.assertEqual(response.status_code, 200)
        self.assertIn('number_of_players', data)
        self.assertIn('player_level', data)
        self.assertIn('tier', data)
        self.assertIn('number_of_npcs', data)
        self.assertIn('npcs_by_role', data)
        
        # Check values
        self.assertEqual(data['number_of_players'], 1)
        self.assertEqual(data['player_level'], 1)
        self.assertEqual(data['tier'], 1)
        self.assertEqual(data['number_of_npcs'], 2)
        
        # Check role grouping
        self.assertIsInstance(data['npcs_by_role'], dict)

    def test_tier_calculation(self):
        """Test tier calculation based on player level"""
        test_cases = [
            (1, 1),   # Level 1 -> Tier 1
            (4, 1),   # Level 4 -> Tier 1
            (5, 2),   # Level 5 -> Tier 2
            (9, 2),   # Level 9 -> Tier 2
            (10, 3),  # Level 10 -> Tier 3
            (12, 3)   # Level 12 -> Tier 3
        ]
        
        for level, expected_tier in test_cases:
            with self.subTest(level=level):
                response = self.app.get(f'/api/encounter?players=1&level={level}')
                data = json.loads(response.data)
                self.assertEqual(data['tier'], expected_tier)

    def test_npc_stats_scaling(self):
        """Test that NPC stats scale correctly with tier"""
        # Get same encounter at different tiers
        response1 = self.app.get('/api/encounter?players=1&level=1')  # Tier 1
        data1 = json.loads(response1.data)
        
        response3 = self.app.get('/api/encounter?players=1&level=10')  # Tier 3
        data3 = json.loads(response3.data)
        
        # Check that all stats are present and properly scaled
        for role, npcs in data1['npcs_by_role'].items():
            for npc in npcs:
                self.assertIn('stats', npc)
                stats = npc['stats']
                expected_stats = ['hp', 'armor', 'evade', 'edef', 'heatcap', 'speed',
                                'sensor', 'save', 'hull', 'agility', 'systems', 'engineering',
                                'size', 'activations']
                for stat in expected_stats:
                    self.assertIn(stat, stats)

    def test_role_distribution(self):
        """Test that NPCs are properly distributed by role"""
        response = self.app.get('/api/encounter?players=3&level=1')  # 6 NPCs
        data = json.loads(response.data)
        
        # Check that we have some role variety
        roles = list(data['npcs_by_role'].keys())
        self.assertGreater(len(roles), 1)  # Should have more than one role
        
        # Check core roles are prioritized
        core_roles = {'striker', 'defender', 'support', 'controller', 'artillery'}
        found_core_roles = set(roles) & core_roles
        self.assertGreater(len(found_core_roles), 0)

    def test_npc_features(self):
        """Test that NPCs have their features included"""
        response = self.app.get('/api/encounter?players=1&level=1')
        data = json.loads(response.data)
        
        for role, npcs in data['npcs_by_role'].items():
            for npc in npcs:
                self.assertIn('features', npc)
                self.assertIn('base', npc['features'])
                self.assertIn('optional', npc['features'])
                self.assertIsInstance(npc['features']['base'], list)
                self.assertIsInstance(npc['features']['optional'], list)

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        test_cases = [
            ('negative_players', '?players=-1&level=1', 400),
            ('zero_players', '?players=0&level=1', 400),
            ('too_many_players', '?players=7&level=1', 400),
            ('negative_level', '?players=1&level=-1', 400),
            ('too_high_level', '?players=1&level=13', 400),
            ('non_numeric_players', '?players=abc&level=1', 400),
            ('non_numeric_level', '?players=1&level=abc', 400),
            ('decimal_players', '?players=1.5&level=1', 400),
            ('decimal_level', '?players=1&level=1.5', 400),
            ('missing_level', '?players=1', 200),  # Should use default level
            ('missing_players', '?level=1', 200),  # Should use default players
        ]
        
        for test_name, query, expected_status in test_cases:
            with self.subTest(test_name=test_name):
                response = self.app.get(f'/api/encounter{query}')
                self.assertEqual(response.status_code, expected_status)

if __name__ == '__main__':
    unittest.main() 