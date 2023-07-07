import socket

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"Успешно подключено к серверу {host}:{port}")
        
        message = "Привет, сервер!"
        client_socket.send(message.encode())
        
    except ConnectionRefusedError:
        print(f"Не удалось подключиться к серверу {host}:{port}")
        
    finally:
        client_socket.close()

# Пример использования
host = '127.0.0.1'
port = 6000
connect_to_server(host, port)

# python -u "c:\Code\py_protocol_parser\с.py"
