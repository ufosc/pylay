import socket
from threading import Thread
from SocketServer import ThreadingMixIn

from user import *

class Server:

	class Listener(Thread):

		def __init__(self, conn):
			Thread.__init__(self)

			self._connection = conn

		def run(self):
			while True:
				data = self._connection.recv(512)
				if not data:
					break

				# handle the message

	def start(self, ip, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

		sock.bind((ip, port))
		while True:
			sock.listen(0)
			(conn, addr) = sock.accept()

			# create requesting user
			Listener(conn).start()
