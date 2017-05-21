#!/usr/bin/env python3

import argparse
import logging
import select
import socket


logger = logging.getLogger(__name__)

default_bind_host = ''
default_bind_port = 5555

log_format = '%(asctime)s %(levelname)5s: %(message)s'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--log', help='path to log file')
    p.add_argument('--verbose', '-v', action='store_true')
    p.add_argument('--host', help='host to bind to, default: {}'.format(default_bind_host or 'all'))
    p.add_argument('--port', help='TCP port to bind to, default: {}'.format(default_bind_port))
    args = p.parse_args()

    setup_logging(args.log, args.verbose)

    bind_host = args.host or default_bind_host
    bind_port = int(args.port or default_bind_port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((bind_host, bind_port))
    server.listen(16)
    logger.info('Listening on %s:%s', bind_host, bind_port)

    clients = []

    while True:
        # https://docs.python.org/3/library/select.html#select.select
        inputs = [server] + [client.socket for client in clients]
        outputs = [client.socket for client in clients if client.want_write()]
        logger.debug('select(%r, %r, ...)', [x.fileno() for x in inputs], [x.fileno() for x in outputs])
        readable, writable, exceptional = select.select(inputs, outputs, [])
        logger.debug('select result: readable %r writable %r', [x.fileno() for x in readable], [x.fileno() for x in writable])
        if server in readable:
            client_socket, client_address = server.accept()
            logger.info('Accepted connection %s from %r', client_socket.fileno(), client_address)
            client = Client(client_socket, client_address, clients)
            clients.append(client)
        for client in clients:
            if client.socket in writable:
                client.process_write()
            if client.socket in readable:
                client.process_read()


def setup_logging(log_file, verbose):
    from logging import INFO, DEBUG, StreamHandler, Formatter
    from logging.handlers import WatchedFileHandler
    root = logging.getLogger('')
    root.setLevel(DEBUG)

    h = StreamHandler()
    h.setFormatter(Formatter(log_format))
    h.setLevel(DEBUG if verbose else INFO)
    root.addHandler(h)

    if log_file:
        h = WatchedFileHandler(log_file)
        h.setFormatter(Formatter(log_format))
        h.setLevel(DEBUG)
        root.addHandler(h)


class Client:

    def __init__(self, socket, address, client_list):
        self.socket = socket
        self.address = address
        self.client_list = client_list
        self.read_buffer = b''
        self.to_send = b''

    def want_write(self):
        return self.to_send

    def _name(self):
        ''' pro účely logování '''
        try:
            fd = self.socket.fileno()
        except Exception as e:
            fd = '-'
        return '{} {}'.format(fd, self.address)

    def process_read(self):
        try:
            s = self.socket.recv(1024)
            logger.debug('Client %s: received %r', self._name(), s)
        except ConnectionResetError as e:
            logger.exception('Client %s: recv failed: %r', self._name(), e)
            s = None
        if not s:
            self.socket.close()
            self.client_list.remove(self)
        else:
            self.read_buffer += s
            while b'\n' in self.read_buffer:
                line, rest = self.read_buffer.split(b'\n', 1)
                self.read_buffer = rest
                self.process_line(line)

    def process_line(self, line):
        line = line.rstrip()
        logger.debug('Client %s: processing line %r', self._name(), line)
        for client in self.client_list:
            client.to_send += '{}: '.format(self.address).encode() + line + b'\n'

    def process_write(self):
        # Schválně budeme posílat po malých kouscích (5 bajtů), abychom donutili
        # chat klienty čekat na zbytek dat (tj. bufferovat příchozí data).
        try:
            n = self.socket.send(self.to_send[:5])
        except Exception as e:
            logger.exception('Client %s: send failed: %r', self._name(), e)
            return
        logger.debug('Client %s: Sent %s bytes', self._name(), n)
        self.to_send = self.to_send[n:]


if __name__ == '__main__':
    main()
