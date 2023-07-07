import argparse
import logging
import os

from .config.config import from_yaml, Settings
from ._server import Server

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Configuration file')
    args = parser.parse_args()

    if not args.c:
        logging.fatal('Configuration file path not specified')

    cfg = from_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), args.c))
    try:
        cfg = from_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), args.c))
    except Exception as e:
        logging.fatal(f'Error parsing configuration file: {e}')

    logging.basicConfig(level=cfg.get_log_level())

    srv = Server()
    srv.New(cfg.get_listen_address(), cfg.get_empty_conn_ttl())
    srv.run()

if __name__ == '__main__':
    main()

                        ### TO RUN ###

### python -u -m server.run_mini_server -c ".\config\conf.yaml" ###