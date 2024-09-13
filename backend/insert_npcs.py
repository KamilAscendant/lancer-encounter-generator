import json
import sqlite3

# Load the JSON data from the file
with open('C:/Users/kamil/Desktop/cs/portfolio/lancer-encounter-generator/backend/npc_classes.json', 'r', encoding='utf-8') as file:
    npc_data = json.load(file)

# Connect to the SQLite database
conn = sqlite3.connect('npc.db') 
cursor = conn.cursor()

# Insert the NPCs into the database
for npc in npc_data:
    name = npc['name']
    role = npc['role']
    tier = 1   # Assign tier 1 for now
    description = npc['info']['flavor']
    tactics = npc['info']['tactics']
    
    # Insert the data
    cursor.execute('INSERT INTO npcs (name, tier, role, description, tactics) VALUES (?, ?, ?, ?, ?)', 
                   (name, tier, role, description, tactics))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("NPC data successfully inserted into the database.")
