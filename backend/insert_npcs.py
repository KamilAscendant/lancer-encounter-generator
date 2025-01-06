import json
import sqlite3

def calculate_tier_multipliers(npc):
    """Calculate how stats scale between tiers"""
    stats = ['hp', 'armor', 'evade', 'edef', 'heatcap', 'speed', 
             'sensor', 'save', 'hull', 'agility', 'systems', 'engineering']
    
    multipliers = {}
    for stat in stats:
        base = max(1, npc['stats'][stat][0])  # Avoid division by zero
        multipliers[stat] = [
            1.0,
            npc['stats'][stat][1] / base,
            npc['stats'][stat][2] / base
        ]
    
    return json.dumps(multipliers)

def insert_npc(cursor, npc):
    """Insert a single NPC into the database"""
    base_stats = calculate_base_stats(npc)
    tier_multipliers = calculate_tier_multipliers(npc)
    description = npc.get('description', '')
    tactics = npc.get('tactics', '')
    base_features = json.dumps(npc.get('base_features', []))
    optional_features = json.dumps(npc.get('optional_features', []))
    
    cursor.execute('''
        INSERT INTO npcs (
            name, role, base_hp, base_armor, base_evade, base_edef,
            base_heatcap, base_speed, base_sensor, base_save,
            base_hull, base_agility, base_systems, base_engineering,
            base_size, base_activations,
            description, tactics, tier_multipliers, base_features, optional_features
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        npc['name'], npc['role'],
        base_stats['hp'], base_stats['armor'], base_stats['evade'], base_stats['edef'],
        base_stats['heatcap'], base_stats['speed'], base_stats['sensor'], base_stats['save'],
        base_stats['hull'], base_stats['agility'], base_stats['systems'], base_stats['engineering'],
        json.dumps(base_stats['size']), base_stats['activations'],
        description, tactics,
        tier_multipliers, base_features, optional_features
    ))

# Load the JSON data
with open('npc_classes.json', 'r', encoding='utf-8') as file:
    npc_data = json.load(file)

conn = sqlite3.connect('npc.db')
cursor = conn.cursor()

for npc in npc_data:
    name = npc['name']
    role = npc['role']
    stats = npc['stats']
    
    # Get base (Tier 1) stats
    base_stats = {
        'hp': stats['hp'][0],
        'armor': stats['armor'][0],
        'evade': stats['evade'][0],
        'edef': stats['edef'][0],
        'heatcap': stats['heatcap'][0],
        'speed': stats['speed'][0],
        'sensor': stats['sensor'][0],
        'save': stats['save'][0],
        'hull': stats['hull'][0],
        'agility': stats['agility'][0],
        'systems': stats['systems'][0],
        'engineering': stats['engineering'][0],
        'size': json.dumps(stats['size'][0]),
        'activations': stats['activations'][0]
    }
    
    description = npc['info']['flavor']
    tactics = npc['info']['tactics']
    tier_multipliers = calculate_tier_multipliers(npc)
    base_features = json.dumps(npc['base_features'])
    optional_features = json.dumps(npc['optional_features'])
    
    cursor.execute('''
        INSERT INTO npcs (
            name, role, 
            base_hp, base_armor, base_evade, base_edef,
            base_heatcap, base_speed, base_sensor, base_save,
            base_hull, base_agility, base_systems, base_engineering,
            base_size, base_activations,
            description, tactics, 
            tier_multipliers, base_features, optional_features
        ) VALUES (
            ?, ?, 
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?,
            ?, ?, 
            ?, ?, ?
        )
    ''', (
        name, role,
        base_stats['hp'], base_stats['armor'], base_stats['evade'], base_stats['edef'],
        base_stats['heatcap'], base_stats['speed'], base_stats['sensor'], base_stats['save'],
        base_stats['hull'], base_stats['agility'], base_stats['systems'], base_stats['engineering'],
        base_stats['size'], base_stats['activations'],
        description, tactics,
        tier_multipliers, base_features, optional_features
    ))

conn.commit()
conn.close()

print("NPC data successfully inserted into the database.")
