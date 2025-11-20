# worker.py

import socket
from config import BROKER_HOST, BROKER_PORT

def start_worker():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((BROKER_HOST, BROKER_PORT))
        print("[WORKER] Connected to broker")
    except Exception as e:
        print("[WORKER] Could not connect:", e)
        return

    try:
        while True:
            # In your actual project, the worker would process tasks
            pass
    except KeyboardInterrupt:
        print("[WORKER] Exiting...")
    finally:
        s.close()

if __name__ == "__main__":
    start_worker()
