import socket

def start_server(host='192.168.2.9', port=54321):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server listening on {host}:{port}')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('Received from client:', data.decode())
                conn.sendall(data)  # Echo back the received data

if __name__ == "__main__":
    start_server()
