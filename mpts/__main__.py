import argparse

from mpts.client import main as client_main
from mpts.server import main as server_main


def main():
    parser = argparse.ArgumentParser(description='MPTS')
    parser.add_argument('--server', action='store_true', help='Run as server')
    parser.add_argument('--client', action='store_true', help='Run as client')
    args = parser.parse_args()

    if args.server:
        server_main()
    elif args.client:
        client_main()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
