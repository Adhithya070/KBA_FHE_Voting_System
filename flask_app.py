from flask import Flask, request, jsonify
import jwt
import bcrypt
import pickle
from datetime import datetime, timedelta
from encryption import setup_fhe, encrypt_vote, decrypt_vote, add_encrypted_votes

app = Flask(__name__)

# Secret key for JWT
JWT_SECRET = "cd33ae4d226e5db1deadb7253ce18f2093b71fac206fdba26fd6e3238ca5b0f8"
JWT_ALGORITHM = "HS256"

# File paths
VOTES_FILE = "votes.pkl"
ADMIN_FILE = "admin.pkl"

import atexit

# Clear user data on shutdown
def clear_user_data():
    print("Clearing user data from votes.pkl...")
    try:
        storage = load_storage()
        storage["users"] = {}  # Clear user credentials
        storage["votes"] = []  # Clear votes
        save_storage(storage)
        print("User data cleared successfully.")
    except Exception as e:
        print(f"Error while clearing user data: {e}")

# Register the shutdown handler

# Load or initialize storage
def load_storage():
    try:
        with open(VOTES_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {"users": {}, "votes": []}

def save_storage(storage):
    with open(VOTES_FILE, "wb") as f:
        pickle.dump(storage, f)

def load_admin():
    try:
        with open(ADMIN_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def save_admin(admin_credentials):
    with open(ADMIN_FILE, "wb") as f:
        pickle.dump(admin_credentials, f)

# Initialize FHE context
context = setup_fhe()

# Routes
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    storage = load_storage()
    if username in storage["users"]:
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    storage["users"][username] = hashed_pw
    save_storage(storage)
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    admin_credentials = load_admin()
    storage = load_storage()
    if admin_credentials and username == admin_credentials["username"]:
        if not admin_credentials or not bcrypt.checkpw(password.encode(), admin_credentials["password"]):
            return jsonify({"error": "Invalid admin password"}), 401
    else:
        hashed_pw = storage["users"].get(username)
        if not hashed_pw or not bcrypt.checkpw(password.encode(), hashed_pw.encode()):
            return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.utcnow() + timedelta(hours=1)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return jsonify({"message": "Login successful", "token": token})

@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    token = data.get("token")
    vote = data.get("vote")

    if not token or vote not in [0, 1]:
        return jsonify({"error": "Token and valid vote (0 or 1) are required"}), 400

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    storage = load_storage()
    encrypted_vote = encrypt_vote(vote, context)
    storage["votes"].append(encrypted_vote)
    save_storage(storage)
    return jsonify({"message": "Vote cast successfully"})

@app.route("/results", methods=["POST"])
def results():
    data = request.json
    token = data.get("token")
    admin_password = data.get("admin_password")

    if not token or not admin_password:
        return jsonify({"error": "Token and admin password are required"}), 400

    # Validate admin password
    admin_credentials = load_admin()
    if not admin_credentials or not bcrypt.checkpw(admin_password.encode(), admin_credentials["password"]):
        return jsonify({"error": "Invalid admin password"}), 401

    # Validate token
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    storage = load_storage()
    if not storage["votes"]:
        return jsonify({"message": "No votes have been cast yet"}), 200

    encrypted_votes = storage["votes"]
    encrypted_tally = add_encrypted_votes(encrypted_votes, context)
    total_votes = decrypt_vote(encrypted_tally, context)
    return jsonify({
        "result": {
            "votes_for_1": total_votes,
            "votes_for_0": len(encrypted_votes) - total_votes
        }
    })


atexit.register(clear_user_data)

if __name__ == "__main__":
    app.run(debug=True)
