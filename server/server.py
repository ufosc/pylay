import socket
from threading import Thread

from server.user import User
from server.error import NoUserError
from common.command import Command
from common.reply import Reply

class Server:
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

			# The user will manage its own connection info
			usr = User(conn, ip)
			# Users are autonomous, but store in a list for nickname lookup
			self._users.append(usr)

			# Let the user start listening on its own thread
			Thread(target = usr.listen, args = (callback,)).start()

	def get_user(self, n):
		"""
		Get the user with the given nickname.
		A user will always be returned, else an exception is raised.

		@param n The nickname to search for.
		@return The retrieved user.
		"""

		try:
			return next(u for u in self._users if u.hostmask.nickname == n)
		except StopIteration:
			raise NoUserError from None

	def remove_user(self, usr):
		"""
		Remove a user from the server, and signal it to stop listening on its
		connection and shut down.

		@param usr The user to remove
		"""

		# The server needs to remove the user instead of just calling die to
		# make sure a dead user does not remain in the user list
		self._users.remove(usr)
		# Will stop the listen loop and close the connection, ending the thread
		usr.die()

	@property
	def users(self):
		return self._users

	@property
	def hostname(self):
		return self._hostname
