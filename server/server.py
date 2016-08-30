import socket
from threading import Thread

from server.user import User
from server.handlers import Handlers
from server.error import NoUserError
from common.command import Command
from common.reply import Reply

class Server(object):
	"""
	An instance of an IRC server.
	Manages users and channels, and handles received messages.
	"""

	_callbacks = {
		Command.QUIT:    (None,  Handlers.quit),
		Command.NICK:    (None,  Handlers.nick),
		Command.USER:    (False, Handlers.user),
		Command.PRIVMSG: (True,  Handlers.privmsg)
	}

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
		"""

		try:
			msg = Command(data)
			(reg, cb) = Server._callbacks[msg.command]

			if reg == True and not usr.is_registered():
				usr.send(Message(self._hostname, Reply.ERR.NOTREGISTERED, [
					'you have not registered'
				]))
			elif reg == False and usr.is_registered():
				usr.send(Message(self._hostname, Reply.ERR.ALREADYREGISTERED, [
					'unauthorized command (already registered)'
				]))

			else:
				cb(self, usr, *msg.arguments)

		except KeyError:
			usr.send(Message(self._hostname, Reply.ERR.UNKNOWNCOMMAND, [
				msg.command, 'unknown command'
			]))

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
