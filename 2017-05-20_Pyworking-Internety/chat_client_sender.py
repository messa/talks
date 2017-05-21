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
    while True:
        msg = input('zadej zpravu: ')
        if not msg:
            continue
        to_send = msg.encode() + b'\n'
        s.sendall(to_send)


if __name__ == '__main__':
    main()
