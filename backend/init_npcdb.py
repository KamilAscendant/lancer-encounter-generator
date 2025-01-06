import sqlite3

# Initialize the database and create the table
conn = sqlite3.connect('npc.db')
cursor = conn.cursor()

# Create a more detailed NPC table
cursor.execute('''CREATE TABLE IF NOT EXISTS npcs (
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
    base_size TEXT,  # This will be JSON since it's an array
    base_activations INTEGER,
    description TEXT,
    tactics TEXT,
    tier_multipliers TEXT,  # JSON string containing stat multipliers for each tier
    base_features TEXT,     # JSON array of base features
    optional_features TEXT  # JSON array of optional features
)''')

conn.commit()
conn.close()

print("Database initialized successfully.")

