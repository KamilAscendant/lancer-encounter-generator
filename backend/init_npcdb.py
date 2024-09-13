import sqlite3

# Initialize the database and create the table
conn = sqlite3.connect('npc.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS npcs
               (name TEXT, tier INTEGER, role TEXT, description TEXT, tactics TEXT)''')

conn.commit()
conn.close()

print("Database initialized successfully.")

