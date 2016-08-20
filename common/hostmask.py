import re

class hostmask:


	def __init__(self, raw):
		"""
		Get information about a source.
		This information is usually the first part of a message from a server,
		and contains the nick, user, and host names.

		:param raw: The string to parse.
		:return: None
		"""

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
