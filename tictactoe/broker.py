import socket
import threading
from config import HOST, BROKER_PORT

# Game state
board = [" "] * 9
current_turn = "X"
clients = []
lock = threading.Lock()

def print_board():
    b = board
    return f"""
 {b[0]} | {b[1]} | {b[2]}
-----------
 {b[3]} | {b[4]} | {b[5]}
-----------
 {b[6]} | {b[7]} | {b[8]}
"""

def check_winner():
    combos = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for x,y,z in combos:
        if board[x] == board[y] == board[z] != " ":
            return board[x]
    if " " not in board:
        return "Draw"
    return None

def broadcast():
    msg = f"{print_board()}|Next: {current_turn}|Winner: {check_winner() or 'None'}"
    for c in clients:
        try:
            c.sendall(msg.encode())
        except:
            clients.remove(c)

def handle_controller(conn):
    global current_turn
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            try:
                symbol, move = data.split("|")
                move = int(move)
            except:
                conn.sendall("Invalid input".encode())
                continue

            with lock:
                if board[move] == " " and symbol == current_turn:
                    board[move] = symbol
                    current_turn = "O" if current_turn == "X" else "X"
                    broadcast()
                else:
                    conn.sendall("Invalid move".encode())
    finally:
        clients.remove(conn)
        conn.close()

def start_broker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, BROKER_PORT))
    s.listen()
    print(f"[BROKER] Listening on {HOST}:{BROKER_PORT}")
    while True:
        conn, addr = s.accept()
        print(f"[BROKER] Controller connected: {addr}")
        threading.Thread(target=handle_controller, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_broker()
