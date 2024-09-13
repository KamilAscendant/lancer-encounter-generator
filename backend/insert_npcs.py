import json
import sqlite3

# Load the JSON data from the file
with open('C:\Users\kamil\Desktop\cs\portfolio\lancer-encounter-generator\backend\npc_classes.json', 'r') as file:
    npc_data = json.load(file)

# Connect to the SQLite database
conn = sqlite3.connect('encounters.db')  # Adjust path if needed
cursor = conn.cursor()

# Iterate through the NPCs and insert them into the database
for npc in npc_data:
    name = npc['name']
    role = npc['role']
    tier = 1   #just t1 for now 
    description = npc['flavor']
    tactics = npc['tactics']
    
    cursor.execute('INSERT INTO npcs (name, tier, role) VALUES (?, ?, ?)', (name, tier, role))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("NPC data successfully inserted into the database.")