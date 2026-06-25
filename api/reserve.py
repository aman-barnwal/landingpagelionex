from flask import Flask, request, jsonify
from supabase import create_client
import resend
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SUPABASE = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SECRET_KEY")
)

# -----------------------------
# Resend Configuration
# -----------------------------

resend.api_key = os.getenv("RESEND_API_KEY")

# -----------------------------
# Flask
# -----------------------------

app = Flask(
    __name__,
    static_folder=".",
    static_url_path=""
)

#--------------------------
# Email
# -----------------------------

def send_confirmation_email(name, email, username):

    template = Path(
        "templates/welcome_email.html"
    )

    if not template.exists():
        raise FileNotFoundError(
            "templates/welcome_email.html not found."
        )

    html = template.read_text(encoding="utf-8")

    html = html.replace("{{NAME}}", name)
    html = html.replace("{{USERNAME}}", username)

    resend.Emails.send({

        "from": "Lionex <onboarding@resend.dev>",

        "to": [email],

        "subject": "🎉 Welcome to Lionex — You're In!",

        "html": html

    })

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.route("/api/reserve", methods=["POST"])
def reserve():

    name = request.form.get("name", "").strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    username = request.form.get(
        "username",
        ""
    ).strip().lower()

    if not name or not email or not username:

        return jsonify({
            "success": False,
            "message": "Please fill all fields."
        })

    reserved = {

        "admin",
        "lionex",
        "official",
        "support",
        "system",
        "root",
        "myai",
        "atlas",
        "nova",
        "rogue",
        "twinkle",
        "solace"

    }

    if username in reserved:

        return jsonify({
            "success": False,
            "message": "This username is reserved."
        })

    try:

        SUPABASE.table(
            "waitlist"
        ).insert({

            "name": name,

            "email": email,

            "username": username

        }).execute()

    except Exception as e:

        error = str(e).lower()

        if (
            "duplicate" in error
            or "unique" in error
            or "23505" in error
        ):

            return jsonify({

                "success": False,

                "message":
                "Email or username already exists."

            })

        print("Database Error:", e)

        return jsonify({

            "success": False,

            "message":
            "Unable to reserve username."

        })

    try:

        if resend.api_key:

            send_confirmation_email(

                name,

                email,

                username

            )

    except Exception as e:

        print("Email Error:", e)

    return jsonify({

        "success": True,

        "message":
        "You're officially on the Lionex waitlist."

    })
# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8000,

        debug=True

    )
