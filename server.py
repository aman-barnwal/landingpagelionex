from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "users.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS waitlist(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/reserve", methods=["POST"])
def reserve():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    username = request.form.get("username", "").strip().lower()

    reserved = [
        "admin",
        "lionex",
        "support",
        "official",
        "system",
        "myai",
        "atlas",
        "nova",
        "rogue",
        "twinkle",
        "solace"
    ]

    if username in reserved:
        return jsonify({
            "success": False,
            "message": "Reserved username"
        })

    try:

        conn = sqlite3.connect(DB_FILE)

        conn.execute("""
            INSERT INTO waitlist
            (name,email,username)
            VALUES (?,?,?)
        """, (name, email, username))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "You're officially on the Lionex waitlist."
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "Email or username already exists."
        })


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )
