import socket
import time

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('superstrika-2.local', 8081))

        while True:
            sock.sendall(input("> ").encode())

if __name__ == "__main__":
    main()
