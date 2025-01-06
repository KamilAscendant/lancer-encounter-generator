import sqlite3
import os

# Delete the database if it exists
if os.path.exists('npc.db'):
    os.remove('npc.db')

# Initialize the database and create the table
conn = sqlite3.connect('npc.db')
cursor = conn.cursor()

# Create a more detailed NPC table
cursor.execute('''CREATE TABLE npcs (
    name TEXT,
    role TEXT,
    base_hp INTEGER,
    base_armor INTEGER,
    base_evade INTEGER,
    base_edef INTEGER,
    base_heatcap INTEGER,
    base_speed INTEGER,
    base_sensor INTEGER,
    base_save INTEGER,
    base_hull INTEGER,
    base_agility INTEGER,
    base_systems INTEGER,
    base_engineering INTEGER,
    base_size TEXT,
    base_activations INTEGER,
    description TEXT,
    tactics TEXT,
    tier_multipliers TEXT,
    base_features TEXT,
    optional_features TEXT
)''')

conn.commit()
conn.close()

print("Database initialized successfully.")

