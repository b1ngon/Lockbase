from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

from dotenv import load_dotenv
from pathlib import Path

# Load the .env key
env_path = Path(__file__).resolve().parent.parent / "config" / "settings.env"
load_dotenv(dotenv_path=env_path)

KEY = base64.b64decode(os.getenv("ENCRYPTION_KEY"))

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt(username, password):
    def _encrypt_one(plain_text):
        iv = get_random_bytes(16)
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        padded_text = pad(plain_text).encode()
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(iv + encrypted).decode()

    encrypted_username = _encrypt_one(username)
    encrypted_password = _encrypt_one(password)
    salt = base64.b64encode(get_random_bytes(16)).decode()

    return encrypted_username, encrypted_password, salt

def decrypt(enc_text):
    enc = base64.b64decode(enc_text)
    iv = enc[:16]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(enc[16:])
    return unpad(decrypted.decode())
