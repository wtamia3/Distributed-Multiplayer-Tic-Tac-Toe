# client.py

import socket

HOST = "127.0.0.1"
PORT = 5555

def start_client():
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))

    try:
        while True:
            msg = c.recv(2048)
            if not msg:
                break
            msg = msg.decode()
            print(msg, end="")
            if "Your move" in msg:
                move = input("> ")
                c.sendall(move.encode())
    except:
        pass
    finally:
        print("\nClient closed.")
        c.close()


if __name__ == "__main__":
    start_client()
