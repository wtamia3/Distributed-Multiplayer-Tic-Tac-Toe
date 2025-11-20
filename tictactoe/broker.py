# broker.py

import socket
from config import BROKER_HOST, BROKER_PORT
import threading

clients = []

def handle_controller(conn):
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("[BROKER] Received from controller:", data)
            # Echo back for testing
            conn.sendall(f"Processed:{data}".encode())
    except:
        print("[BROKER] Controller disconnected")
    finally:
        conn.close()

def start_broker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((BROKER_HOST, BROKER_PORT))
    s.listen()
    print(f"[BROKER] Listening on {BROKER_HOST}:{BROKER_PORT}")

    while True:
        conn, addr = s.accept()
        print(f"[BROKER] Connected: {addr}")
        threading.Thread(target=handle_controller, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_broker()
