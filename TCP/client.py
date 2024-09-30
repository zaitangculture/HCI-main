import socket

def start_client(host='192.168.2.16', port=777):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return

        while True:
            message = input("Enter message to send: ")
            if not message:
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print('Received from server:', data.decode())

if __name__ == "__main__":
    start_client()
