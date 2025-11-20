# controller.py

import socket
import threading
from multiprocessing import Process, Queue
from worker import worker_loop
from utils import format_board

HOST = "127.0.0.1"
PORT = 5555

clients = []
symbols = ["X", "O"]
board = [" "] * 9
turn = "X"

# REAL shared multiprocessing queues
task_queue = Queue()
result_queue = Queue()

# Sync lock to prevent race conditions
turn_lock = threading.Lock()


def safe_send(conn, msg):
    try:
        conn.sendall(msg.encode())
        return True
    except Exception as e:
        print("[SEND ERROR]", e)
        return False


def broadcast(msg):
    dead = []
    for c in clients:
        if not safe_send(c, msg):
            dead.append(c)

    for c in dead:
        clients.remove(c)


def wrap_handler(conn, symbol):
    """Show all exceptions instead of silently exiting"""
    try:
        handle_client(conn, symbol)
    except Exception as e:
        print(f"[THREAD ERROR] Player {symbol} crashed:", e)


def handle_client(conn, symbol):
    global board, turn

    safe_send(conn, f"Welcome Player {symbol}!\n")

    while True:
        with turn_lock:

            if turn != symbol:
                continue

            safe_send(conn, "Your move (0-8): ")

            try:
                data = conn.recv(1024)
            except Exception as e:
                print(f"[RECV ERROR] Player {symbol}:", e)
                return

            if not data:
                print(f"[DISCONNECT] Player {symbol} closed connection")
                return

            move = data.decode().strip()

            if not move.isdigit() or int(move) not in range(9):
                safe_send(conn, "Invalid input.\n")
                continue

            move = int(move)

            # Send to worker
            task_queue.put((symbol, move, board))
            valid, new_board, winner = result_queue.get()

            if not valid:
                safe_send(conn, "Invalid move.\n")
                continue

            board[:] = new_board

            broadcast(f"Board:\n{format_board(board)}\n")

            if winner:
                broadcast(f"GAME OVER — {winner} wins!\n")
                return

            turn = "O" if turn == "X" else "X"


def start_server():
    # spawn worker process
    worker = Process(target=worker_loop, args=(task_queue, result_queue))
    worker.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print("\nServer running on port 5555...\n")

    while len(clients) < 2:
        conn, addr = server.accept()
        symbol = symbols[len(clients)]
        print(f"Player {symbol} connected from {addr}")

        clients.append(conn)
        thread = threading.Thread(target=wrap_handler, args=(conn, symbol))
        thread.start()


if __name__ == "__main__":
    start_server()
