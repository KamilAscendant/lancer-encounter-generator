import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('npc.db') 
cursor = conn.cursor()

# Check if the 'npcs' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='npcs';")
table_exists = cursor.fetchone()

if table_exists:
    print("NPC table exists.\n")
    
    # Retrieve all NPC data from the table
    cursor.execute('SELECT * FROM npcs')
    npcs = cursor.fetchall()

    if npcs:
        print("NPC manifest:")
        for npc in npcs:
            print(f"Name: {npc[0]}, Tier: {npc[1]}, Role: {npc[2]}, Description: {npc[3]}, Tactics: {npc[4]}")
    else:
        print("No NPCs found in the database.")
else:
    print("NPC table does not exist.")

# Close the connection
conn.close()
