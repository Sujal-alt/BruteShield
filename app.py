from flask import Flask, render_template, request
import hashlib
import re

app = Flask(__name__)

def check_strength(password):
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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    hashed = ''
    decoded = ''
    strength = 0

    if request.method == "POST":
        if "clear" in request.form:
            return render_template("index.html", hashed='', decoded='', strength=0)

        password = request.form["password"]
        strength = check_strength(password)
        hashed = hash_password(password)
        decoded = password

        # Store only strong passwords (>= 70)
        if strength >= 70:
            with open("passwords.txt", "a") as file:
                file.write(f"Decoded: {decoded} \n Encoded: {hashed} ") 

    return render_template("index.html", hashed=hashed, decoded=decoded, strength=strength)

if __name__ == "__main__":
    app.run(debug=True)
