import base64, os

key = base64.b64encode(os.urandom(32)).decode()
print("Paste this into your .env file:\n")
print(f"ENCRYPTION_KEY={key}")
