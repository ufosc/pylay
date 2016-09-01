import socket
from threading import Thread

from server.user import User
from server.error import NoUserError, NoChannelError, NotInChannelError
from common.command import Command
from common.reply import Reply
from common.channel import Channel

class Server:
	"""
	An instance of an IRC server.
	Manages users and channels, and handles received messages.
	"""

	def __init__(self):
		"""
		Create a new IRC server.
		"""

		self._users    = {}
		self._channels = {}

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
			# Users are autonomous, but store them as a key to keep track of
			# the channels they belong to
			self._users[usr] = []

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
			us = self._users.keys()
			return next(u for u in us if u.hostmask.nickname == n)
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
		self._users.pop(usr)
		# Will stop the listen loop and close the connection, ending the thread
		usr.die()

	def get_channel(self, n, create = False):
		"""
		Get the channel with the given (fully-qualified) name.

		@param n The name of the channel to search for.
		@param create Specify whether the channel should be created if it
		              does not exist. Otherwise, raise NoChannelError.
		@return The retrieved channel.
		"""

		try:
			cs = self._channels.keys()
			# The name includes the prefix, so format each channel to match
			return next(c for c in cs if format(c) == n)

		except StopIteration:
			# When no channel is found, it is automatically created (maybe)
			# Always try to create it, to raise BadChannelError
			c = Channel.from_raw(n)
			if create == False:
				raise NoChannelError from None

			# The channel starts out with no users
			self._channels[c] = []
			return c

	def get_channel_users(self, chan):
		"""
		Return a list of users that are currently in a channel.

		@param chan The channel object to get users from.
		@return A list of joined users.
		"""

		try:
			return self._channels[chan]
		except KeyError:
			raise NoChannelError from None

	def join_channel(self, chan, usr):
		"""
		Add to the list of joined users for a channel.

		@param chan The target channel.
		@param usr The user trying to join.
		"""

		if chan not in self._channels:
			self._channels[chan] = []
		if usr in self._channels[chan]:
			return

		self._channels[chan].append(usr)
		self._users[usr].append(chan)

	def part_channel(self, chan, usr):
		"""
		Remove a user from the list of users of a channel.

		@param chan The target channel.
		@param usr The user trying to part.
		"""

		if chan not in self._channels:
			raise NoChannelError
		if chan not in self._users[usr]:
			raise NotInChannelError

		self._channels[chan].remove(usr)
		self._users[usr].remove(chan)

	@property
	def hostname(self):
		return self._hostname
