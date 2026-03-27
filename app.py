from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def connect_db():
    return sqlite3.connect("database.db")

# Create table
@app.route('/init')
def init():
    conn = connect_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            status TEXT,
            notes TEXT
        )
    ''')
    conn.close()
    return "Database initialized"

# Add application
@app.route('/add', methods=['POST'])
def add():
    data = request.json
    conn = connect_db()
    conn.execute("INSERT INTO applications (company, status, notes) VALUES (?, ?, ?)",
                 (data['company'], data['status'], data['notes']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Added successfully"})

# Get all
@app.route('/all', methods=['GET'])
def get_all():
    conn = connect_db()
    data = conn.execute("SELECT * FROM applications").fetchall()
    conn.close()
    return jsonify(data)

# Update
@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.json
    conn = connect_db()
    conn.execute("UPDATE applications SET status=? WHERE id=?", (data['status'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Updated"})

# Delete
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = connect_db()
    conn.execute("DELETE FROM applications WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(debug=True)