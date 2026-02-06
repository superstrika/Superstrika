import socket
import serverManagment

class Client:
    def __init__(self):
        server = serverManagment.getServerInfo(False)

        port = server["port"]
        hostname = server["hostname"]

        print(port)
        print(hostname)

        self._sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._sock.connect((hostname, port))

        print(f"Connected! hostname: {hostname}, port: {port}")
    
    def sendMessage(self, cmd: int, params: list[float]):
        msg = str(cmd)

        for param in params:
            msg += "#" + str(param)
        
        print(f"Sending: {msg}")

        self._sock.sendall(msg.encode())

    def __del__(self):
        self._sock.close()

if __name__ == "__main__":
    c = Client()
    c.sendMessage(1, [0.0, 100, 0, 250, 0, 0, 0])
