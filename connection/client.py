import socket
import serverManagment

def main():
    server = serverManagment.getServerInfo()

    port = server["port"]
    hostname = server["hostname"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, port))
        print(f"Connected! hostname: {hostname}, port: {port}")

        while True:
            sock.sendall(input("> ").encode())

if __name__ == "__main__":
    main()
