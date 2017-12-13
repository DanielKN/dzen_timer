# Echo client program
import socket
import sys

HOST = 'localhost'    # The remote host
PORT = 2222              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(sys.argv[1].encode('utf-8')))
    s.close()
