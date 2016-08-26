import socket
from threading import Thread

from user import *
from handlers import *
from common.command import *
from common.reply import *

class Server(object):
	"""
	An instance of an IRC server.
	Manages users and channels, and handles received messages.
	"""

	def __init__(self):
		"""
		Create a new IRC server.
		"""

		self._users = []
		self._hostname = None

	def start(self, ip, port):
		"""
		Begin listening for client connections at the given address.

		@param ip The IP address to listen on.
		@param port The port to listen on. Should be 6660-6669 or 7000.
		"""

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

		self._hostname = ip
		sock.bind((ip, port))

		while True:
			# Listen with no queued connections - will block
			sock.listen(0)
			# A connection has been acquired - get its info
			(conn, (ip, _)) = sock.accept()

			usr = User(conn, ip)
			self._users.append(usr)

			Thread(target = usr.listen, args = (self.handle_message,)).start()

	def handle_message(self, usr, data):
		"""
		Perform an action based on the message received.
		Handle passing messages, managing users/channels, etc.

		@param usr The User the data was received from.
		@param data The raw data received from the client.
		@return False, if the connection should end, True otherwise.
		"""

		res = None

		msg = Command(data)
		if msg.command == Command.QUIT:
			self._users.remove(usr)
			return False

		elif msg.command == Command.NICK:
			res = Handlers.nick(self, usr, *msg.arguments)
		elif msg.command == Command.USER:
			res = Handlers.user(self, usr, *msg.arguments)
		elif msg.command == Command.PRIVMSG:
			res = Handlers.privmsg(self, usr, *msg.arguments)

		else:
			res = Message(self._hostname, Reply.ERR.UNKNOWNCOMMAND, [
				msg.command, 'unknown command'
			])

		if res is not None:
			usr._connection.sendall(format(res))

		# A command may have caused a user to become registered
		if not usr.is_registered() and usr.can_register():
			self.register_user(usr)

		# Most normal commands do not end with finishing the connection
		return True

	def find_user(self, n):
		return next((u for u in self._users if u.hostmask.nickname == n), None)

	def register_user(self, usr):
		assert not usr.is_registered() and usr.can_register()

		usr.register()
		usr._connection.sendall(format(Message(self._hostname, Reply.RPL.WELCOME, [
			'welcome to pylay IRC ' + format(usr.hostmask)
		])))

	@property
	def users(self):
		return self._users

	@property
	def hostname(self):
		return self._hostname
