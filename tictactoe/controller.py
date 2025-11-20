# controller.py

import socket
from config import BROKER_HOST, BROKER_PORT

def start_controller():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((BROKER_HOST, BROKER_PORT))
    s.sendall("CONTROLLER\n".encode())
    print("[CONTROLLER] Connected to broker.")

    response = s.recv(1024).decode()
    print("[BROKER REPLY]", response)

    while True:
        move = input("Enter move (0–8): ")
        symbol = input("Enter symbol (X/O): ")

        msg = f"{symbol}|{move}"
        s.sendall(msg.encode())

        reply = s.recv(1024).decode()
        valid, board, winner = reply.split("|")

        print("Valid?", valid)
        print("Board:", board)
        print("Winner:", winner)

if __name__ == "__main__":
    start_controller()
