from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import random
import json
from collections import defaultdict

app = Flask(__name__)
CORS(app)

def connect_db():
    conn = sqlite3.connect('npc.db')
    conn.row_factory = sqlite3.Row
    return conn

def scale_npc_stats(npc, tier, multipliers):
    """Scale NPC stats based on tier"""
    stats = {}
    for stat in ['hp', 'armor', 'evade', 'edef', 'heatcap', 'speed', 
                 'sensor', 'save', 'hull', 'agility', 'systems', 'engineering']:
        base_value = npc[f'base_{stat}']
        multiplier = multipliers[stat][tier-1]
        stats[stat] = int(base_value * multiplier)
    
    stats['size'] = json.loads(npc['base_size'])
    stats['activations'] = npc['base_activations']
    return stats

def select_npcs_by_role(all_npcs, num_npcs):
    """Select NPCs with balanced role distribution"""
    # Group NPCs by role
    npcs_by_role = defaultdict(list)
    for npc in all_npcs:
        npcs_by_role[npc['role']].append(npc)
    
    # Try to ensure at least one of each core role if possible
    core_roles = ['striker', 'defender', 'support', 'controller', 'artillery']
    selected_npcs = []
    
    # First, try to add one of each core role
    for role in core_roles:
        if len(npcs_by_role[role]) > 0 and len(selected_npcs) < num_npcs:
            selected_npcs.append(random.choice(npcs_by_role[role]))
    
    # Fill remaining slots randomly
    while len(selected_npcs) < num_npcs:
        role = random.choice(list(npcs_by_role.keys()))
        selected_npcs.append(random.choice(npcs_by_role[role]))
    
    return selected_npcs

@app.route('/api/encounter', methods=['GET'])
def get_encounter():
    try:
        # Validate player count and level
        try:
            num_players = int(request.args.get('players', 1))
            player_level = int(request.args.get('level', 1))
        except ValueError:
            return jsonify({"error": "Player count and level must be whole numbers"}), 400
            
        # Validate ranges
        if num_players < 1 or num_players > 6:
            return jsonify({"error": "Player count must be between 1 and 6"}), 400
        if player_level < 0 or player_level > 12:
            return jsonify({"error": "Player level must be between 0 and 12"}), 400
        
        # Calculate tier based on level
        tier = 1
        if player_level >= 5:
            tier = 2
        if player_level >= 10:
            tier = 3
            
        # Calculate number of NPCs
        num_npcs = num_players * 2
        
        conn = connect_db()
        cursor = conn.cursor()
        
        # Get all NPCs from database
        cursor.execute("""
            SELECT * FROM npcs
        """)
        all_npcs = cursor.fetchall()
        
        if not all_npcs:
            return jsonify({"error": "No NPCs found in database"}), 404
            
        # Select NPCs with balanced roles
        selected_npcs = select_npcs_by_role(all_npcs, num_npcs)
        
        # Scale and format NPCs for response
        formatted_npcs = []
        for npc in selected_npcs:
            multipliers = json.loads(npc['tier_multipliers'])
            scaled_npc = {
                "name": npc['name'],
                "role": npc['role'],
                "tier": tier,
                "description": npc['description'],
                "tactics": npc['tactics'],
                "stats": scale_npc_stats(npc, tier, multipliers),
                "features": {
                    "base": json.loads(npc['base_features']),
                    "optional": json.loads(npc['optional_features'])
                }
            }
            formatted_npcs.append(scaled_npc)
        
        # Group NPCs by role in response
        npcs_by_role = defaultdict(list)
        for npc in formatted_npcs:
            npcs_by_role[npc['role']].append(npc)
        
        encounter = {
            "number_of_players": num_players,
            "player_level": player_level,
            "tier": tier,
            "number_of_npcs": num_npcs,
            "npcs_by_role": dict(npcs_by_role)  # Convert defaultdict to regular dict
        }
        
        return jsonify(encounter)
        
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
