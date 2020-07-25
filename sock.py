import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s_addr = ('localhost', 5005)
sock.connect(s_addr)

try:
   message = b'message'
   sock.sendall(message)
finally:
   sock.close()