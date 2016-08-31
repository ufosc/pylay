import socket
from threading import Thread

from server.user import User
from server.error import NoUserError
from common.command import Command
from common.reply import Reply

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

	def start(self, ip, port, callback):
		"""
		Begin listening for client connections at the given address.

		@param ip The IP address to listen on.
		@param port The port to listen on. Should be 6660-6669 or 7000.
		@param callback The function to call when a thread receives a message
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

			Thread(target = usr.listen, args = (callback,)).start()

	def get_user(self, n):
		try:
			return next(u for u in self._users if u.hostmask.nickname == n)
		except StopIteration:
			raise NoUserError from None

	def remove_user(self, usr):
		self._users.remove(usr)
		usr.die()

	@property
	def users(self):
		return self._users

	@property
	def hostname(self):
		return self._hostname
