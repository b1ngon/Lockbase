# 🔐 Lockbase – Encrypted Credential Manager

Lockbase is a secure Flask-based API for storing and retrieving user credentials with end-to-end encryption using AES-256. It supports user registration, login, and full CRUD operations for credential management.

---

## 📚 Table of Contents

- [Features](#features)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [API Usage](#api-usage)  
- [Environment Variables](#environment-variables)  
- [Author](#author)  

---

## ✨ Features

- Register & authenticate users with hashed passwords (`bcrypt`)
- Encrypt credentials using AES (CBC mode) and a secure base64 key
- Store encrypted username/password per service (Gmail, GitHub, etc.)
- RESTful API endpoints (POST, GET, PUT, DELETE)
- Easily testable via Postman or cURL
- MySQL-backed persistent storage
- Environment-configured via `.env`

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
lockbase/
├── backend/
│   ├── main.py                 # Flask app with route handlers
│   ├── db.py                   # MySQL database connection
│   ├── crypto_utils.py         # AES encryption/decryption logic
│   ├── generate_key.py         # One-time script to generate base64 key
├── config/
│   └── settings.env            # Environment configuration (not tracked)
├── frontend/
│   └── index.html              # Placeholder for future UI
├── logs/
│   └── .keep                   # Keeps logs directory in version control
├── tests/                      # Folder for test scripts (optional)
├── .gitignore                  # Ignore virtualenv, .env, etc.
├── requirements.txt           # All project dependencies
└── README.md                   # This file
```

</details>

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/bingonx/lockbase.git
cd lockbase
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Unix
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate encryption key
```bash
python backend/generate_key.py
```

### 5. Start the Flask server
```bash
python backend/main.py
```

---

## 🔌 API Usage

### ✅ Register a User
```bash
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "barry", "password": "strongpass"}'
```

### ✅ Store Credentials
```bash
curl -X POST http://127.0.0.1:5000/credentials/create \
-H "Content-Type: application/json" \
-d '{"username": "barry@gmail.com", "password": "secure123", "service_name": "Gmail", "user_id": 1}'
```

---

## 📄 Environment Variables

To get started, copy the example environment file and configure your own secrets.

⚠️ **Never commit your real `.env` file. Add `config/settings.env` to `.gitignore`.**

### Create a `.env` file at `config/settings.env`:
```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=lockbase
ENCRYPTION_KEY=your_32_byte_base64_key
```

You can generate a secure encryption key using:
```bash
python backend/generate_key.py
```

---

## 🧾 Supported API Endpoints

| Method | Endpoint              | Description             |
|--------|-----------------------|-------------------------|
| POST   | `/register`           | Register a new user     |
| POST   | `/credentials/create` | Save new credentials    |
| POST   | `/credentials/get`    | Retrieve stored creds   |
| PUT    | `/credentials/update` | Update stored creds     |
| DELETE | `/credentials/delete` | Delete stored creds     |

---

## 👤 Author

Developed by **Barry Ngon**  
Full-stack Developer • Security Enthusiast  
[GitHub](https://github.com/bingonx) • [LinkedIn](https://linkedin.com/in/barryngon/)
