#!/usr/bin/python

# https://pymotw.com/2/socket/tcp.html

import socket
import sys


def start(port, q):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('localhost', port)
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(64)
                if data != '':
                  q.put(data)
                if not(data):
                    break
        finally:
            # Clean up the connection
            connection.close()
