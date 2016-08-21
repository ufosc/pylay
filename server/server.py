import socket
from threading import Thread
from SocketServer import ThreadingMixIn

from user import *
from common.command import *
from common.reply import *

class Server(object):
	"""
	An instance of an IRC server.
	Manages users and channels, and handles received messages.
	"""

	class Listener(Thread):
		"""
		A single, threaded, connection to a client.
		Waits for data to be sent from the client, and passes it to the server
		for processing.
		"""

		def __init__(self, serv, addr, conn):
			"""
			Initialize the client listener and its thread.

			:param serv: The server this listener was spawned from.
			:param addr: The addres the connection was opened on.
			:param conn: The socket connection itself.
			:return: None
			"""

			Thread.__init__(self)
			self._connection = conn
			self._address = addr

			self._server = serv

		def run(self):
			"""
			Begin the messaging loop waiting for data from the client.

			:return: None
			"""

			while True:
				# IRC messages can be a maximum of 512 characters
				data = self._connection.recv(512)
				if not data:
					break

				# The server method will return True when the client quits
				done = self._server.handle_message(self, data)
				if done:
					break

			# Explicitly finish the connection - any remaining data will be sent
			self._connection.close()

		def send(self, data):
			"""
			Send some data back to the client.
			Guaranteed to send all data.

			:param data: The data to send.
			:return: None
			"""

			self._connection.sendall(data)

		@property
		def address(self):
			return self._address

	def __init__(self):
		"""
		Create a new IRC server.

		:return: None
		"""

		self._users = {}
		self._hostname = None

	def start(self, ip, port):
		"""
		Begin listening for client connections at the given address.

		:param ip: The IP address to listen on.
		:param port: The port to listen on. Should be 6660-6669 or 7000.
		:return: None
		"""

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

		self._hostname = ip
		sock.bind((ip, port))

		while True:
			# Listen with no queued connections - will block
			sock.listen(0)
			# A connection has been acquired - get its info
			(conn, addr) = sock.accept()

			(ip, _) = addr
			# All users are pending until the nick and host info is sent
			self._users[ip] = PendingUser(ip)

			# Begin waiting for data from this client
			Server.Listener(self, addr, conn).start()

	def handle_message(self, source, data):
		"""
		Perform an action based on the message received.
		Handle passing messages, managing users/channels, etc.

		:param source: The Listener the data was received on.
		:param data: The raw data received from the client.
		:return: True, if the connection should now close; False otherwise.
		"""

		(ip, _) = source.address
		usr = self._users[ip]
		res = None

		msg = Command(data)
		if msg.command == Command.QUIT:
			return True

		elif msg.command == Command.NICK:
			res = self.set_nickname(usr, *msg.arguments)

		else:
			res = Message(self._hostname, Reply.ERR.UNKNOWNCOMMAND, [
				msg.command, 'unknown command'
			])

		if res is not None:
			source.send(format(res))

		# Most normal commands do not end with finishing the connection
		return False

	def set_nickname(self, usr, nick):
		return None

	@property
	def users(self):
		return self._users
