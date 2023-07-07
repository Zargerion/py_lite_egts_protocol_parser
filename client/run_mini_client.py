from time import sleep
import argparse

import socket

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--host", help="Adress of server to work with EGTS", default='127.0.0.1', type=str)
    parser.add_argument("-p", "--port", help="Port to work with EGTS", default=3000, type=int)
    parser.add_argument("file", help="Text file with packages", type=str)
    
    args = parser.parse_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(args.host, args.port)
    client.connect((args.host, args.port))

    BUFF = 1024

    with open(args.file) as f:
        for rec in f.readlines():
            print("send: {}".format(rec))
            package = bytes.fromhex(rec[:-1])            
            client.send(package)

            data = client.recv(BUFF)
            if data:
                print(f"Answer from server: {data.decode()}")

    client.close()

                                    ### TO RUN ###

    ### python -u ".\client\run_mini_client.py" ".\client\to_test_egts_packages.csv" ###
