import socket
import time

def main():
    port = 50100
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', 8082))
        print("Listening...")
        sock.listen(1)
        conn, addr = sock.accept()
        print(f"Connection by: {addr}")
        # print(conn.recv(1024).decode())
        sock.setblocking(False)
        print("Socket is non-blocking. Attempting to receive data...")

        while True:
            try:
                data = conn.recv(1024)

                if data:
                    print(data.decode())
                else:
                    print("Connection closed by slave")
                    break

            except BlockingIOError:
                print("No data yet, waiting...")
                time.sleep(0.1)
                continue

            except Exception as e:
                print(f"ERROR: {e}")
                break

if __name__ == "__main__":
    main()
