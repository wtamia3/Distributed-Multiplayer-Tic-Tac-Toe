import socket
import sys
from config import CONTROLLER_HOST, CONTROLLER_PORT

def start_client():
    host = CONTROLLER_HOST

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, CONTROLLER_PORT))
    print("Connected to controller.\n")

    while True:
        msg = s.recv(1024).decode()
        if not msg:
            break
        print(msg, end="")
        if "Your move" in msg:
            move = input("> ")
            s.sendall(move.encode())

if __name__ == "__main__":
    start_client()
