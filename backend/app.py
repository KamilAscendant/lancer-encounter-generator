from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # This will allow requests from any origin

def connect_db():
    conn = sqlite3.connect('encounters.db')
    return conn

@app.route('/api/encounter', methods=['GET'])
def get_encounter():
#    conn = connect_db()
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM encounters ORDER BY RANDOM() LIMIT 1")
#    encounter = cursor.fetchone()
#    return jsonify({"name": encounter[0], "difficulty": encounter[1], "details": encounter[2]})

    return jsonify({
        "message": "Test Encounter Generated",
        "name": "Test NPC",
        "difficulty": "Easy",
        "details": "This is a test encounter for debugging purposes."
    })

if __name__ == '__main__':
    app.run(debug=True)
