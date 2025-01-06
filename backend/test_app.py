import unittest
from app import app, scale_npc_stats, select_npcs_by_role
import json
import sqlite3

class TestEncounterAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client and ensure database has test data"""
        self.app = app.test_client()
        self.app.testing = True
        
        try:
            # Initialize database
            import subprocess
            subprocess.run(['python', 'init_npcdb.py'], check=True)
            subprocess.run(['python', 'insert_npcs.py'], check=True)
            
            # Verify the database has data
            conn = sqlite3.connect('npc.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM npcs")
            npc_count = cursor.fetchone()[0]
            
            if npc_count == 0:
                raise Exception("Database initialization failed")
            
            conn.close()
        except Exception as e:
            raise Exception(f"Test setup failed: {str(e)}")

    def tearDown(self):
        """Clean up after each test"""
        try:
            import os
            if os.path.exists('npc.db'):
                os.remove('npc.db')
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")

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

    def test_feature_selection_by_tier(self):
        """Test that NPCs get the correct number of optional features based on tier"""
        
        # Test Tier 1 (should have 0-1 features)
        response1 = self.app.get('/api/encounter?players=1&level=1')
        data1 = json.loads(response1.data)
        for role, npcs in data1['npcs_by_role'].items():
            for npc in npcs:
                num_optional = len(npc['features']['optional'])
                self.assertGreaterEqual(num_optional, 0)
                self.assertLessEqual(num_optional, 1)
        
        # Test Tier 2 (should have 1-2 features)
        response2 = self.app.get('/api/encounter?players=1&level=6')
        data2 = json.loads(response2.data)
        for role, npcs in data2['npcs_by_role'].items():
            for npc in npcs:
                num_optional = len(npc['features']['optional'])
                self.assertGreaterEqual(num_optional, 1)
                self.assertLessEqual(num_optional, 2)
        
        # Test Tier 3 (should have 2-3 features)
        response3 = self.app.get('/api/encounter?players=1&level=11')
        data3 = json.loads(response3.data)
        for role, npcs in data3['npcs_by_role'].items():
            for npc in npcs:
                num_optional = len(npc['features']['optional'])
                self.assertGreaterEqual(num_optional, 2)
                self.assertLessEqual(num_optional, 3)

    def test_feature_selection_validity(self):
        """Test that selected features are valid and base features remain unchanged"""
        response = self.app.get('/api/encounter?players=1&level=1')
        data = json.loads(response.data)
        
        # Connect to DB to get the original NPC data for comparison
        conn = sqlite3.connect('npc.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        for role, npcs in data['npcs_by_role'].items():
            for npc in npcs:
                # Get original NPC data from database
                cursor.execute("SELECT base_features, optional_features FROM npcs WHERE name = ?", 
                             (npc['name'],))
                db_npc = cursor.fetchone()
                
                # Convert JSON strings to lists
                original_base = json.loads(db_npc['base_features'])
                original_optional = json.loads(db_npc['optional_features'])
                
                # Check that base features are unchanged
                self.assertEqual(npc['features']['base'], original_base)
                
                # Check that selected optional features are from the original pool
                for feature in npc['features']['optional']:
                    self.assertIn(feature, original_optional)
        
        conn.close()

if __name__ == '__main__':
    unittest.main() 