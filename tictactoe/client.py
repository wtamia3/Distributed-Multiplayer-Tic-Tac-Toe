# client.py

import socket
import sys
from config import CONTROLLER_HOST, CONTROLLER_PORT

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((CONTROLLER_HOST, CONTROLLER_PORT))
    except Exception as e:
        print("Could not connect to controller:", e)
        sys.exit(1)

    print("Connected to controller.\n")

    while True:
        msg = s.recv(1024).decode()

        if not msg:
            print("Controller disconnected.")
            break

        print(msg, end="")

        if "Your move" in msg:
            move = input("> ")
            s.sendall(move.encode())

if __name__ == "__main__":
    start_client()
