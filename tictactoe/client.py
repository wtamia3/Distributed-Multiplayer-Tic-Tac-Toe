# client.py

import socket
from config import CONTROLLER_HOST, CONTROLLER_PORT

def start_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((CONTROLLER_HOST, CONTROLLER_PORT))
        print("[CLIENT] Connected to controller")
    except Exception as e:
        print("[CLIENT] Could not connect:", e)
        return

    try:
        while True:
            move = input("Enter move (0-8): ")
            symbol = input("Enter symbol (X/O): ")
            msg = f"{symbol}|{move}"
            s.sendall(msg.encode())
            reply = s.recv(1024).decode()
            print("[CLIENT] Broker reply:", reply)
    except KeyboardInterrupt:
        print("[CLIENT] Exiting...")
    finally:
        s.close()

if __name__ == "__main__":
    start_client()
