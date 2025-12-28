import socket
import time
import serverManagment
import commandManager

def main():
    server = serverManagment.getServerInfo(True) #same hostname
    port = server["port"]
    hostname = server["hostname"]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((hostname, port))

        print(f"Listening... Port: {port}, Hostname: {hostname}")
        sock.listen(1)

        conn, addr = sock.accept()
        print(f"Connection by: {addr}")

        sock.setblocking(False)
        print("Socket is non-blocking. Attempting to receive data...")

        while True:
            try:
                data = conn.recv(1024)

                if data:
                    print(data.decode())
                    commandManager.runCommand(data.decode())

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