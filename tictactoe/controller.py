import socket
import threading
from config import HOST, BROKER_PORT, CONTROLLER_PORT

def handle_client(client_sock, broker_sock):
    try:
        while True:
            data = client_sock.recv(1024).decode()
            if not data:
                break
            broker_sock.sendall(data.encode())
            reply = broker_sock.recv(1024).decode()
            client_sock.sendall(reply.encode())
    except:
        pass
    finally:
        client_sock.close()

def start_controller():
    broker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_sock.connect((HOST, BROKER_PORT))
    print("[CONTROLLER] Connected to broker")

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', CONTROLLER_PORT))
    server_sock.listen()
    print(f"[CONTROLLER] Listening for clients on port {CONTROLLER_PORT}")

    while True:
        client_sock, addr = server_sock.accept()
        print(f"[CONTROLLER] Client connected: {addr}")
        threading.Thread(target=handle_client, args=(client_sock, broker_sock), daemon=True).start()

if __name__ == "__main__":
    start_controller()

