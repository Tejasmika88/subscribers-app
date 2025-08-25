from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/app/data/items.db"   # PVC-mounted path

def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/api/items", methods=["GET"])
def get_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    items = [{"id": r[0], "name": r[1]} for r in rows]
    return jsonify(items)

@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added successfully"}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
