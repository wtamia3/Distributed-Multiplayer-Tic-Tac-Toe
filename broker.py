import socket
import threading
import queue
from config import BROKER_HOST, BROKER_PORT

task_queue = queue.Queue()
worker_sockets = []
lock = threading.Lock()

def handle_worker(conn, addr):
    with lock:
        worker_sockets.append(conn)
    print(f"[WORKER CONNECTED] {addr}")

    try:
        while True:
            # Wait for a task from controller
            symbol, move, board = task_queue.get()
            message = f"{symbol}|{move}|{','.join(board)}"
            conn.sendall(message.encode())

            result = conn.recv(1024).decode()
            conn.sendall(result.encode())
    except:
        print("[WORKER DISCONNECTED]", addr)
    finally:
        with lock:
            worker_sockets.remove(conn)
        conn.close()

def start_broker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((BROKER_HOST, BROKER_PORT))
    s.listen(5)
    print(f"[BROKER] Running at {BROKER_HOST}:{BROKER_PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_worker, args=(conn, addr)).start()

if __name__ == "__main__":
    start_broker()
