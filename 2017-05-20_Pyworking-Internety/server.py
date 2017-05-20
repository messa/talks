import argparse
import select
import socket


def main():
    p = argparse.ArgumentParser()
    p.add_argument('port')
    args = p.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', int(args.port)))
    server.listen(16)

    clients = []

    while True:
        inputs = [server] + [client.socket for client in clients]
        outputs = [client.socket for client in clients if client.want_write()]
        print('select({}, {}, ...)'.format(inputs, outputs))
        readable, writable, exceptional = select.select(inputs, outputs, [])
        print('select: {}, {}, {}'.format(readable, writable, exceptional))
        if server in readable:
            client_socket, client_address = server.accept()
            print('Accepted connection from {}'.format(client_address))
            client = Client(client_socket, client_address, clients)
            clients.append(client)
        for client in clients:
            if client.socket in writable:
                client.process_write()
            if client.socket in readable:
                client.process_read()


class Client:

    def __init__(self, socket, address, client_list):
        self.socket = socket
        self.address = address
        self.client_list = client_list
        self.read_buffer = b''
        self.to_send = b''

    def want_write(self):
        return self.to_send

    def process_read(self):
        s = self.socket.recv(1024)
        print('Client {} received: {!r}'.format(self.address, s))
        if not s:
            self.socket.close()
            self.client_list.remove(self)
            return
        self.read_buffer += s
        while b'\n' in self.read_buffer:
            line, rest = self.read_buffer.split(b'\n', 1)
            self.read_buffer = rest
            self.process_line(line)

    def process_line(self, line):
        line = line.rstrip()
        print('Client {} processing line {}'.format(self.address, line))
        for client in self.client_list:
            client.to_send += '{}: '.format(self.address).encode() + line + b'\n'

    def process_write(self):
        n = self.socket.send(self.to_send)
        self.to_send = self.to_send[n:]


if __name__ == '__main__':
    main()
