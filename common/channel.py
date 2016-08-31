import re

from common.error import BadChannelError

class Channel:
	"""
	Manages the state and information pertaining to an IRC channel.
	"""

	# This channel can be accessed across servers
	GLOBAL = '#'
	# This channel can only be accessed by users on the server it was created on
	LOCAL  = '&'

	@staticmethod
	def from_raw(raw):
		"""
		Parse channel information from a string.
		Will only succeed if the channel type is one defined above.

		@param raw The complete channel identifier in string form.
		@return A newly created Channel object.
		"""

		# Breakdown for parsing a channel:
		# - "[#&]":         get the channel type, a single character
		# - "[^ ,]{1,199}": get the channel name, up to 199 characters (a
		#                   complete IRC channel can be up to 200), which
		#                   should not include spaces or commas
		result = re.search("^([#&])([^ ,]{1,199})$", raw)

		if result is None:
			raise BadChannelError

		return Channel(result.group(2), result.group(1))

	def __init__(self, n, t):
		"""
		Create a new Channel object with the given attributes.

		@param n The name of the channel, a string.
		@param t The type of the channel, a single character that matches one
		         of the constants above.
		"""

		self._name = n
		self._type = t

	def __format__(self, spec):
		"""
		Convert the channel into an identifier as it would appear in a message.
		Consists of the type followed by the name.

		@param spec The character encoding. Unused.
		@return The channel formatted as a string.
		"""

		return self._type + self._name

	@property
	def name(self):
		return self._name

	@property
	def type(self):
		return self._type
