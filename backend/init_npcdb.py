import sqlite3

conn = sqlite3.connect('npc.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE npcs
               (name TEXT, tier INTEGER, role TEXT, description TEXT, tactics TEXT)''')

conn.commit()
conn.close()

print("Database initialized successfully.")
