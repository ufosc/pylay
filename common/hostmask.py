import re

class Hostmask:


	def __init__(self, raw):
		"""
		Get information about a source.
		This information is usually the first part of a message from a server,
		and contains the nick, user, and host names.

		:param raw: The string to parse.
		:return: None
		"""

		# Breakdown for parsing a hostmask:
		# - ".{1,9}": get the nickname, which is at most 9 characters
		# - "[^@]":   parse up to the host separator for the username
		# - "(.+)":   parse to the end of the string for the hostname
		result = re.search("^(.{1,9})!([^@]+)@(.+)$", raw)

		if result is None:
			raise ValueError('bad hostmask format')
		else:
			self._nick = result.group(1)
			self._user = result.group(2)
			self._host = result.group(3)

	@property
	def nick(self):
		return self._nick

	@property
	def user(self):
		return self._user

	@property
	def host(self):
		return self._host
