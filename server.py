from flask import Flask, request, jsonify
import sqlite3

app = Flask(
    __name__,
    static_folder=".",
    static_url_path=""
)

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
    return app.send_static_file("index.html")


@app.route("/reserve", methods=["POST"])
def reserve():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    username = request.form.get("username", "").strip().lower()

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
