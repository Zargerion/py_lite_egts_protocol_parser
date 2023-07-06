from time import sleep
import argparse

import socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--host", help="Adress of server to work with EGTS", default='127.0.0.2', type=str)
    parser.add_argument("-p", "--port", help="Port to work with EGTS", default=6000, type=int)
    parser.add_argument("file", help="Text file with packages", type=str)
    
    args = parser.parse_args()

    TEST_ADDR = (args.host, args.port)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(TEST_ADDR)

    BUFF = 2048

    with open(args.file) as f:
        for rec in f.readlines():
            print("send: {}".format(rec))
            package = bytes.fromhex(rec[:-1])            
            client.send(package)

            rec_package = client.recv(BUFF)
            print("received: {}".format(rec_package.hex()))
            sleep(1)

    client.close()
