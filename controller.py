import socket
import threading
from config import CONTROLLER_HOST, CONTROLLER_PORT, BROKER_HOST, BROKER_PORT
import queue

task_queue = queue.Queue()
result_queue = queue.Queue()

clients = []
board = [" "] * 9
turn = "X"
lock = threading.Lock()

def listen_to_broker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((BROKER_HOST, BROKER_PORT))
    print("[CONTROLLER] Connected to BROKER")

    while True:
        # Receive via broker
        result = s.recv(1024).decode()
        valid, new_board, winner = result.split("|")
        valid = valid == "True"
        new_board = new_board.split(",")
        result_queue.put((valid, new_board, winner))
        
def handle_client(conn, symbol):
    global turn, board

    conn.sendall(f"Welcome Player {symbol}!\n".encode())

    while True:
        if turn == symbol:
            conn.sendall("Your move (0-8): ".encode())
            move = conn.recv(1024).decode().strip()

            if not move.isdigit() or int(move) not in range(9):
                conn.sendall("Invalid input.\n".encode())
                continue

            with lock:
                # Send job to broker
                task_queue.put((symbol, int(move), board))

                valid, new_board, winner = result_queue.get()
                if valid:
                    board = new_board
                    broadcast_board()
                    if winner:
                        broadcast(f"Game over! Winner: {winner}\n")
                        return
                    turn = "O" if turn == "X" else "X"
                else:
                    conn.sendall("Invalid move.\n".encode())

def broadcast(message):
    for c in clients:
        try:
            c.sendall(message.encode())
        except:
            pass

def broadcast_board():
    text = (
        "\nBoard:\n" +
        f"{board[0]} | {board[1]} | {board[2]}\n" +
        "---------\n" +
        f"{board[3]} | {board[4]} | {board[5]}\n" +
        "---------\n" +
        f"{board[6]} | {board[7]} | {board[8]}\n\n"
    )
    broadcast(text)

def start_controller():
    broker_thread = threading.Thread(target=listen_to_broker)
    broker_thread.start()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((CONTROLLER_HOST, CONTROLLER_PORT))
    s.listen(2)
    print(f"[CONTROLLER] Running on {CONTROLLER_HOST}:{CONTROLLER_PORT}")

    symbols = ["X", "O"]

    for symbol in symbols:
        conn, addr = s.accept()
        clients.append(conn)
        print(f"[CLIENT CONNECTED] {symbol} from {addr}")
        threading.Thread(target=handle_client, args=(conn, symbol)).start()

if __name__ == "__main__":
    start_controller()
