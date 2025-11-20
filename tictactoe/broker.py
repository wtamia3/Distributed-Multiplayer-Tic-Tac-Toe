import socket
import threading
from queue import Queue
from config import BROKER_HOST, BROKER_PORT

controller_conn = None
workers = []
task_queue = Queue()
lock = threading.Lock()
print(f"[BROKER] Binding to {BROKER_HOST}:{BROKER_PORT}")

def handle_worker(conn, addr):
    print(f"[WORKER CONNECTED] {addr}")

    with lock:
        workers.append(conn)

    try:
        while True:
            symbol, move, board = task_queue.get()
            payload = f"{symbol}|{move}|{','.join(board)}"
            conn.sendall(payload.encode())

            result = conn.recv(1024).decode()
            controller_conn.sendall(result.encode())
    except:
        print(f"[WORKER DISCONNECTED] {addr}")
    finally:
        with lock:
            if conn in workers:
                workers.remove(conn)
        conn.close()

def handle_controller(conn):
    global controller_conn
    controller_conn = conn
    print("[BROKER] Controller connected.")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        symbol, move, board_raw = data.split("|")
        board = board_raw.split(",")

        task_queue.put((symbol, int(move), board))

def start_broker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((BROKER_HOST, BROKER_PORT))
    s.listen(5)

    print(f"[BROKER] Listening on {BROKER_HOST}:{BROKER_PORT}")

    while True:
        conn, addr = s.accept()
        first = conn.recv(32).decode()

        if first.startswith("CONTROLLER"):
            threading.Thread(target=handle_controller, args=(conn,)).start()
        else:
            threading.Thread(target=handle_worker, args=(conn, addr)).start()

if __name__ == "__main__":
    start_broker()
