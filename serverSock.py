import socket
import logging

class Server:
   """
   A simple socket server to listen for controls
   """

   def __init__(self, sock=None):
      if sock is None:
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      else:
         self.sock = sock
      self.HOST = '127.0.0.1'
      self.PORT = '8888'
      self.HOST_PORT = (self.HOST, self.PORT)

   def get_data(self):
      """Retrieves data from a socket connection"""
      data_recvd = b''
      with self.sock as s:
         s.bind(self.HOST_PORT)
         s.listen()
         conn, addr = s.accept()
         with conn:
            logging.info('Connection from:' + addr)
            while True:
               data = conn.recv(1024)
               if not data:
                  return data_recvd.decode('UTF-8')
               data_recvd += data