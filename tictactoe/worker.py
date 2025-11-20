# worker.py

import socket
import os
from config import BROKER_HOST, BROKER_PORT
from utils import check_winner

def start_worker():
    # Determine worker name
    if hasattr(os, "uname"):
        hostname = os.uname().nodename
    else:
        hostname = os.getenv("COMPUTERNAME", "worker")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((BROKER_HOST, BROKER_PORT))
    s.sendall(f"WORKER|{hostname}\n".encode())

    print(f"[WORKER {hostname}] Connected to broker.")

    while True:
        data = s.recv(1024).decode()

        if not data:
            print("[WORKER] Broker disconnected.")
            break

        # Expected format: symbol|move|board_csv
        symbol, move, board_raw = data.split("|")
        board = board_raw.split(",")

        move = int(move)
        valid = board[move] == " "

        if valid:
            board[move] = symbol

        winner = check_winner(board)

        result = f"{valid}|{','.join(board)}|{winner if winner else ''}"

        print(f"[WORKER {hostname}] Move {move} by {symbol} -> valid={valid}")

        s.sendall(result.encode())

if __name__ == "__main__":
    start_worker()
