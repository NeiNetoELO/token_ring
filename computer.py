#!bin/bash/python
# -*- coding: utf-8 -*-

import socket
from typing import Tuple
from collections import deque


class Computer(object):
    """xd"""

    def __init__(self, ny_nickname: str, my_socket_address: Tuple[str, int] = ('localhost', 5000),
                 next_computer_address: Tuple[str, int] = ('localhost', 6000), tokenizer: bool=False):
        """
        It gets a tuple to set where to host the server,
        another tuple to set where to send his packets
        and a boolean to set whether it is the first computer on a network (defaults to false because this will only be used once)
        """
        self.ny_nickname = ny_nickname
        self.my_socket_address = my_socket_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.my_socket_address)
        
        self.next_computer_address = next_computer_address
        self.packet_queue = deque()
        if tokenizer:
            self.create_token()

    def start(self):

        while True:
            packet = Packet(*str(self.wait_connection()).split(';'))  # get packets from socket, cast to str, split(';')
            if not Packet.is_token():
                if self.ny_nickname == packet.dest_nick:  # if I am the destination device of this packet
                    packet.read()  # mark packet as read "OK"
                    self.connect(packet.to_bytes())  # send packet to next computer on the network
                elif self.ny_nickname == packet.origin_nick:
                    # it means the packet I had sent to some computer on the network got back to me
                    if packet.has_been_read:
                        # It's fine, discard packet or something
                        # pass token
                    else:
                        #  SOMETHING WENT WRONG
            elif Packet.is_token():
                if len(self.packet_queue) > 0:  # if I want to send messages
                    self.connect(self.packet_queue.popleft().to_bytes())
                    # wait for packet to come back
                    continue
                else:
                   # pass token

        pass

    def connect(self, text=b"teste"):
        self.sock.sendto(text, self.next_computer_address)

    def wait_connection(self):
        incoming = self.sock.recv(1024)
        return incoming

    def create_token(self):
        return Packet(1234, '', '', '')


def read_file(file_path: str) -> list:
    '''
    <ip_destino_token>
    <apelido>
    <tempo_token>
    '''
    with open(file_path) as setup_file:
        return list(setup_file)


class Packet(object):
    """Datagram: 2345;naocopiado:Bob:Alice:Oi Mundo!"""
    """Datagram: iden;statuscopy;origin;destination;msg"""
    """          0   ;1         ;2     ;3          ;4"""

    def __init__(self, packet_type: int, origin_nick: str, dest_nick: str, text: str):
        self.packet_type = packet_type
        self.origin_nick = origin_nick
        self.dest_nick = dest_nick
        self.text = text
        self.has_been_read = False

    def is_token(self):
        if self.packet_type == 1234:
            return True
        elif self.packet_type == 2345:
            return False

    def read(self):
        self.has_been_read = True

    def to_bytes(self):
        return bytes(str(self), 'utf-8')

    def _pprint(self):
        return "{}\n{}\n{}\n{}\n{}".format(self.packet_type, self.read, self.dest_nick, self.dest_nick, self.text)

    def __str__(self) -> str:
        return "{}\n{}\n{}\n{}\n{}".format(
            self.packet_type, self.has_been_read, self.dest_nick, self.dest_nick, self.text)
        
"""
To run on a single machine,
openopen two ipython sessions and copypaste this
(must cd token_ring first)

from computer import Computer
pc1 = Computer(('localhost', 5000), ('localhost', 6000))
print(pc1.wait_connection())

from computer import Computer
pc2 = Computer(('localhost', 6000), ('localhost', 5000))
pc2.connect(b"teste")

"""
if __name__ == "__main__":
    pc3 = Computer(('localhost', 7000))
    # setup = read_file("")
