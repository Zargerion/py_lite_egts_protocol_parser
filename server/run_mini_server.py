import argparse
import logging

from config.config import from_yaml
from server.server import Server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Configuration file')
    args = parser.parse_args()

    if not args.c:
        logging.fatal('Configuration file path not specified')

    try:
        cfg = from_yaml(args.c)
    except Exception as e:
        logging.fatal(f'Error parsing configuration file: {e}')

    logging.basicConfig(level=cfg.get_log_level())

    srv: Server = Server.New(cfg.get_listen_address(), cfg.get_empty_conn_ttl())
    srv.run()

if __name__ == '__main__':
    main()