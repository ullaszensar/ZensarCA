import os
import sys
import base64
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    cipher = Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = cipher.encrypt(file_data)

    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as enc_file:
        enc_file.write(encrypted_data)

    print(f"File '{file_path}' has been encrypted and saved as '{encrypted_file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 encrypt_java.py <file_path> <encryption_key>")
        sys.exit(1)

    file_path = sys.argv[1]
    key = sys.argv[2]

    if not os.path.exists(file_path):
        print("Error: The specified file does not exist.")
        sys.exit(1)

    try:
        key = base64.urlsafe_b64encode(key.encode().ljust(32)[:32])  # Ensure 32 bytes
        Fernet(key)  # Validate the key
    except Exception:
        print("Invalid key. Ensure it is a 32-byte Base64 encoded key.")
        sys.exit(1)

    encrypt_file(file_path, key)