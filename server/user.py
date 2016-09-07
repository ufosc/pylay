from common.hostmask import *

class User:
	"""
	Manages the state of a user, starting from the time of connection.
	"""

	def __init__(self, conn, host):
		"""
		Create a new user that has connected from the given hostname.
		The user starts in an unregistered state.

		@param conn The socket connection for this user.
		@param host The hostname of the user.
		"""

		# A user can be registered once it has a fully complete hostmask
		self._registered = False
		# A thread can continue the listen loop until it is no longer alive
		self._alive = True

		self._connection = conn
		self._hostmask = Hostmask(None, None, host)

	def update(self, nickname = None, username = None):
		"""
		Update the username/nickname of a user after a USER or NICK command.
		Any argument that is not None will be updated with the given value.
		Note that the username can only be updated before the user registers.

		@param nickname The nickname to update to.
		@param username The username to update to.
		"""

		if username is not None:
			# A username can only be set in the "waiting to register" state
			assert not self._registered
			# Hostmask user/host is immutable, so create an updated copy
			newh = Hostmask.update(self._hostmask, username = username)
			self._hostmask = newh

		if nickname is not None:
			self._hostmask.nickname = nickname

	def listen(self, callback):
		"""
		Begin listening for messages on the user connection.

		@param callback The callback function to pass the received data to.
		"""

		while self._alive:
			# 512 is the maximum IRC message size, and always is encoded ASCII
			try:
				data = self._connection.recv(512).decode('ascii')
				assert data

				callback(self, data)

			except (UnicodeDecodeError, AssertionError):
				self.die()

		# Once dead, close the connection and finish off this user
		self._connection.close()

	def send(self, msg):
		"""
		Send a message to this user.
		The send is guaranteed to complete.

		@param msg A message object to send.
		"""

		try:
			data = format(msg)
			self._connection.sendall(bytes(data, 'ascii'))
		except UnicodeDecodeError:
			self.die()

	def is_registered(self):
		"""
		Check if a user has been registered.
		"""

		return self._registered

	def can_register(self):
		"""
		Check if a user can register in its current state.

		@return True if the user can register, False otherwise.
		"""

		if self._registered:
			return False
		# A user can register once all components of its hostmask are present
		if self._hostmask.nickname is None:
			return False
		if self._hostmask.username is None:
			return False

		return True

	def register(self):
		"""
		Set a user as registered.
		A user must have a nickname and a username at this point.
		"""

		# Always call can_register before attempting to call register
		assert not self._registered
		assert self.can_register()

		self._registered = True

	def die(self):
		"""
		Signal this user to stop listening on its connection and shut down.
		"""

		# The thread will actually die the next time the listen loop runs
		self._alive = False

	@property
	def alive(self):
		return self._alive

	@property
	def hostmask(self):
		return self._hostmask
