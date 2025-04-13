from flask import Flask, request, jsonify
import bcrypt
from db import get_db_connection
from dotenv import load_dotenv
import os
from crypto_utils import encrypt
from crypto_utils import decrypt

load_dotenv(dotenv_path='../config/settings.env')

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Lockbase 🔐"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, master_password_hash) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except MySQLdb.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT master_password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/credentials/create', methods=['POST'])
def create_credential():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    service = data.get("service_name")
    user_id = data.get("user_id")

    if not all([username, password, service, user_id]):
        return jsonify({"error": "Missing fields"}), 400

    encrypted_user = encrypt(username)
    encrypted_pass = encrypt(password)
    salt = os.urandom(16).hex()

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO credentials (user_id, service_name, encrypted_username, encrypted_password, salt)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, service, encrypted_user, encrypted_pass, salt))
        conn.commit()
        return jsonify({"message": "Credential saved"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/credentials/get', methods=['POST'])
def get_credentials():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT service_name, encrypted_username, encrypted_password
            FROM credentials WHERE user_id = %s
        """, (user_id,))
        rows = cursor.fetchall()

        results = []
        for service, enc_user, enc_pass in rows:
            results.append({
                "service": service,
                "username": decrypt(enc_user),
                "password": decrypt(enc_pass)
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/credentials/update', methods=['PUT'])
def update_credential():
    data = request.get_json()
    credential_id = data.get('id')
    new_username = data.get('username')
    new_password = data.get('password')

    if not credential_id or not new_password:
        return jsonify({"error": "Missing credential ID or new password"}), 400

    conn = cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        from crypto_utils import encrypt
        encrypted_username, encrypted_password, salt = encrypt(new_username, new_password)

        cursor.execute("""
            UPDATE credentials
            SET encrypted_username = %s,
                encrypted_password = %s,
                salt = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (encrypted_username, encrypted_password, salt, credential_id))

        conn.commit()
        return jsonify({"message": "Credential updated"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@app.route('/credentials/delete', methods=['DELETE'])
def delete_credential():
    data = request.get_json()
    credential_id = data.get('id')

    if not credential_id:
        return jsonify({"error": "Missing credential ID"}), 400

    conn = cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM credentials WHERE id = %s", (credential_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Credential not found"}), 404

        return jsonify({"message": "Credential deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == '__main__':
    app.run(debug=True)
