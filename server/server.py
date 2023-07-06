import socket
import logging

class Server:
    def __init__(self, addr: str, ttl: int):
        self.addr = addr
        self.ttl = ttl
        self.listener = None
        
    
    def run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.listener:
                self.listener.bind((self.addr, 6000))
                logging.info("Server is running...", self.addr)
                
                while True:
                    try: 
                        conn, clint_addr = self.listener.accept()
                        logging.info("A connection is established to client %s", clint_addr)
                        # Ваш код для обработки соединения клиента
                        
                    except Exception as e:
                        logging.error(f"Cannot make connection: {e}")
                
        except Exception as e:
            logging.error(f"Cannot run server: {e}")

    def stop(self) -> None:
        if self.listener is not None:
            self.listener.close()