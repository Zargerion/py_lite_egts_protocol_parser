import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(128)
    
    print(f"Сервер запущен на {host}:{port}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Установлено соединение с клиентом {addr[0]}:{addr[1]}")
        
        data = conn.recv(1024)
        if data:
            print(f"Получены данные от клиента: {data.decode()}")
        
        conn.close()

# Пример использования
host = '127.0.0.1'
port = 6000
start_server(host, port)

# python -u "c:\Code\py_protocol_parser\s.py"