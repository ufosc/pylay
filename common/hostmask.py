import re

class hostmask:

	def __init__(self, raw):
		result = re.search("^(.{1,9})!([^@]+)@(.+)$", raw)
		assert result is not None

		self._nick = regex.group(1)
		self._user = regex.group(2)
		self._host = regex.group(3)

	@property
	def nick(self):
		return self._nick

	@property
	def user(self):
		return self._user

	@property
	def host(self):
		return self._host
