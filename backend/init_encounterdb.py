import sqlite3

# Connect to the SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('encounters.db')
cursor = conn.cursor()

# Create a table named 'encounters'
cursor.execute('''CREATE TABLE encounters
                  (name TEXT, difficulty TEXT, details TEXT)''')



# Insert some sample data into the 'encounters' table
cursor.execute("INSERT INTO encounters VALUES ('Bandit Ambush', 'Medium', 'A group of bandits attack')")
cursor.execute("INSERT INTO encounters VALUES ('Alien Ruins', 'Hard', 'The party discovers ancient alien ruins')")


# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print("Database initialized successfully.")
