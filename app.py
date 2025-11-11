from flask import Flask, render_template, request
import hashlib
import re
from datetime import datetime
import os

app = Flask(__name__)

def check_strength(password: str) -> int:
    length = len(password)
    score = 0
    if length >= 8:
        score += 25
    if re.search(r"[a-z]", password):
        score += 15
    if re.search(r"[A-Z]", password):
        score += 20
    if re.search(r"\d", password):
        score += 20
    if re.search(r"\W", password):
        score += 20
    return min(score, 100)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

PASSWORD_FILE = os.path.join(os.path.dirname(__file__), "passwords.txt")

@app.route("/", methods=["GET", "POST"])
def index():
    hashed = ''
    decoded = ''
    strength = 0

    if request.method == "POST":
        # If clear button pressed, just render blank form
        if "clear" in request.form:
            return render_template("index.html", hashed='', decoded='', strength=0)

        password = request.form.get("password", "")
        if password:
            strength = check_strength(password)
            hashed = hash_password(password)
            decoded = password  # used only to show on the page (NOT stored)

            # Store only strong passwords (>= 70) — store hashed + timestamp only
            if strength >= 70:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(PASSWORD_FILE, "a", encoding="utf-8") as f:
                    f.write(f"{timestamp}  Hashed: {hashed}\n")
    return render_template("index.html", hashed=hashed, decoded=decoded, strength=strength)

if __name__ == "__main__":
    # debug=True is fine for development, remove in production
    app.run(debug=True)
