import re

from common.error import NicknameError

class Hostmask(object):
	"""
	A unique identifier for a client.
	This information is usually the first part of a message from a server, and
	contains the nick, user, and host names.
	"""

	@staticmethod
	def from_raw(raw):
		"""
		Parse a hostmask as it is received from a message.

		@param raw The hostmask, as a string.
		@return The constructed Hostmask, or None if invalid.
		"""

		# Breakdown for parsing a hostmask:
		# - ".{1,9}": get the nickname, which is at most 9 characters
		# - "[^@]":   parse up to the host separator for the username
		# - "(.+)":   parse to the end of the string for the hostname
		result = re.search("^(.{1,9})!([^@]+)@(.+)$", raw)

		if result is None:
			return None
		else:
			return Hostmask(result.group(1), result.group(2), result.group(3))

	@staticmethod
	def update(old, username = None, hostname = None):
		"""
		Create a new hostmask, based off of another.
		Will update any passed optional argument.

		@param username The new username to replace old.username.
		@param hostname The new hostname to replace old.hostname.
		@return The newly constructed hostname.
		"""

		n = old.nickname
		u = username if username is not None else old.username
		h = hostname if hostname is not None else old.hostname

		return Hostmask(n, u, h)

	def __init__(self, nick, user, host):
		"""
		Create a new hostmask with the given parts.

		@param nick The nickname.
		@param user The username.
		@param host The hostname.
		"""

		self._nickname = nick
		self._username = user
		self._hostname = host

	def __format__(self, spec):
		"""
		Format a hostmask as how it will be seen in a message.
		The parts of a hostmask are separated by '!' and '@'.

		@param spec The character encoding. Unused.
		@return The hostmask formatted as a string.
		"""

		if not self.is_valid():
			raise RuntimeError('cannot format an incomplete hostmask')

		return "{}!{}@{}".format(self._nickname, self._username, self._hostname)

	def is_valid(self):
		"""
		Check if all components of a hostmask are present.

		@return True, if the hostmask is valid, False otherwise.
		"""

		return None not in (self._nickname, self._username, self._hostname)

	@property
	def nickname(self):
		return self._nickname

	@nickname.setter
	def nickname(self, nick):
		chars = len(nick)
		if chars < 1 or chars > 9:
			raise NicknameError

		self._nickname = nick

	@property
	def username(self):
		return self._username

	@property
	def hostname(self):
		return self._hostname
