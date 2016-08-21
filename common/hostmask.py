import re

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

		:param raw: The hostmask, as a string.
		:return: The constructed Hostmask, or None if invalid.
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

	def __init__(self, nick, user, host):
		"""
		Create a new hostmask with the given parts.

		:param nick: The nickname.
		:param user: The username.
		:param host: The hostname.
		:return: None
		"""

		self._nickname = nick
		self._username = user
		self._hostname = host

	def __format__(self, spec):
		"""
		Format a hostmask as how it will be seen in a message.
		The parts of a hostmask are separated by '!' and '@'.

		:param spec: The character encoding. Unused.
		:return: The hostmask formatted as a string.
		"""

		return "{}!{}@{}".format(self._nickname, self._username, self._hostname)

	@property
	def nickname(self):
		return self._nickname

	@nickname.setter
	def nickname(self, nick):
		self._nickname = nick

	@property
	def username(self):
		return self._username

	@property
	def hostname(self):
		return self._hostname
