import socket
from threading import Thread
from SocketServer import ThreadingMixIn

from user import *

class Server:

	class Listener(Thread):

		def __init__(self, serv, addr, conn):
			Thread.__init__(self)
			self._connection = conn
			self._address = addr

			self._server = serv

		def run(self):
			while True:
				data = self._connection.recv(512)
				if not data:
					break

				# handle the message

	def __init__(self):
		self._users = []

	def start(self, ip, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

		sock.bind((ip, port))
		while True:
			sock.listen(0)
			(conn, addr) = sock.accept()

			(ip, _) = addr
			self._users.append(PendingUser(ip))

			Listener(self, addr, conn).start()

	@property
	def users(self):
		return self._users
