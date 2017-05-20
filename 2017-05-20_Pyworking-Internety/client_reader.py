#!/usr/bin/env python3

import argparse
import socket


def main():
    p = argparse.ArgumentParser()
    p.add_argument('host')
    p.add_argument('port')
    args = p.parse_args()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, int(args.port)))
    buf = b''
    while True:
        data = s.recv(1024)
        if not data:
            print('konec')
        buf += data
        while b'\n' in buf:
            line, rest = buf.split(b'\n', 1)
            buf = rest
            print('> ' + line.decode().rstrip())


if __name__ == '__main__':
    main()
