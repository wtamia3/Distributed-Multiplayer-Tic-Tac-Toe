import socket
import threading
from config import HOST, CONTROLLER_PORT

def listen_to_controller(sock):
    while True:
        try:
            data = sock.recv(4096).decode()
            if not data:
                break
            try:
                board, turn, winner = data.split("|")
            except:
                print(data)
                continue

            print("\n" + board)
            print(turn)
            print("Winner:", winner)
            print("\n")
        except:
            break

def start_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, CONTROLLER_PORT))
    print("[CLIENT] Connected to controller")

    threading.Thread(target=listen_to_controller, args=(s,), daemon=True).start()

    while True:
        move = input("Enter move (0-8): ").strip()
        symbol = input("Enter symbol (X/O): ").strip().upper()
        s.sendall(f"{symbol}|{move}".encode())

if __name__ == "__main__":
    start_client()
