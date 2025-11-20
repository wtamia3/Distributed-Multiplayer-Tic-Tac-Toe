# controller.py

import socket
from config import BROKER_HOST, BROKER_PORT, CONTROLLER_PORT

def handle_client(client_sock, broker_sock):
    try:
        while True:
            data = client_sock.recv(1024).decode()
            if not data:
                break
            # Forward to broker
            broker_sock.sendall(data.encode())
            # Get broker response
            reply = broker_sock.recv(1024).decode()
            client_sock.sendall(reply.encode())
    except:
        print("[CONTROLLER] Client disconnected")
    finally:
        client_sock.close()

def start_controller():
    # Connect to broker
    try:
        broker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broker_sock.connect((BROKER_HOST, BROKER_PORT))
        broker_sock.sendall("CONTROLLER\n".encode())
        print("[CONTROLLER] Connected to broker")
    except Exception as e:
        print("[CONTROLLER] Failed to connect to broker:", e)
        return

    # Listen for clients
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(('', CONTROLLER_PORT))
        server_sock.listen()
        print(f"[CONTROLLER] Listening for clients on port {CONTROLLER_PORT}")
    except Exception as e:
        print("[CONTROLLER] Failed to start server socket:", e)
        return

    while True:
        client_sock, addr = server_sock.accept()
        print(f"[CONTROLLER] Client connected from {addr}")
        handle_client(client_sock, broker_sock)

if __name__ == "__main__":
    start_controller()
