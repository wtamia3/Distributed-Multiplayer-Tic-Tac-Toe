import socket
from config import BROKER_HOST, BROKER_PORT
from utils import check_winner

def start_worker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((BROKER_HOST, BROKER_PORT))
    print("[WORKER] Connected to broker.")

    while True:
        data = s.recv(1024).decode()
        symbol, move, board_raw = data.split("|")
        board = board_raw.split(",")

        move = int(move)
        valid = board[move] == " "

        if valid:
            board[move] = symbol

        winner = check_winner(board)

        result = f"{valid}|{','.join(board)}|{winner if winner else ''}"
        print(f"[WORKER TASK] Move {move} by {symbol} -> valid={valid}")

        s.sendall(result.encode())

if __name__ == "__main__":
    start_worker()
