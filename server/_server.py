import socket
import logging
from struct import unpack
import time

from egtc.package import Package

class Server:
    def __init__(self):
        self.addr = None
        self.ttl = None
        self.listener = None
        
    def New(self, addr: str, ttl: int):
        """Gets 'adress:port' and time of life connection"""
        self.addr = addr
        self.ttl = ttl

    def __handleConn(self, conn: socket.socket) -> None:
        """Handling of connection"""
        headerLen = 10
        try:
            headerBuf = conn.recv(headerLen)

            # if the packet is not in EGTS format, close the connection
            if headerBuf[0] != 0x01:
                raise Exception(f"Packet does not match EGTS format. Connection closed. Client IP: {conn.getpeername()[0]}")

            # calculate the length of the packet, equal to the length of the header (HL) + body length (FDL) + CRC packet 2 bytes if there is FDL from order of Mintrans No. 285
            bodyLen = unpack('<H', headerBuf[5:7])[0]
            pkgLen = headerBuf[3]
            if bodyLen > 0:
                pkgLen += bodyLen + 2

            # get the end of the EGTS packet
            buf = conn.recv(pkgLen-headerLen)
            if not buf:
                raise Exception(f"Error receiving packet body. Client IP: {conn.getpeername()[0]}")

            # form a complete packet
            recvPacket = headerBuf + buf

            pkg = Package()
            pkg.decode(recvPacket)
            pkg.print_packet_values()


            response_text = 'Authorized!'
            conn.send(response_text.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error of connection: {e}", exc_info=True)
        finally:
            conn.close()
    
    def run(self) -> None:
        """Runs server..."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.listener:
                # it split this "{host}:{port}"
                host, port = self.addr.split(':')
                self.listener.bind((host, int(port)))
                self.listener.listen(128)
                logging.info("Server is running...", self.listener.getsockname())
                
                while True:
                    try: 
                        conn, clint_addr = self.listener.accept()
                        logging.info("A connection is established to client %s", clint_addr, exc_info=True)
                        
                        self.__handleConn(conn)
                
                    except Exception as e:
                        logging.info(f"conn, clint_addr = self.listener.accept() fail {e}", exc_info=True) 

        except Exception as e:
            logging.error(f"Cannot run server: {e}", exc_info=True)
        finally:
            self.listener.close()

    def stop(self) -> None:
        """Close socket"""
        if self.listener is not None:
            self.listener.close()