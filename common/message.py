from hostmask import *

class message:

	def __init__(self, raw):
		"""
		Parse a complete IRC message into its constituents.
		Break a message into its source, command, and arguments (if any).

		:param raw: The string to parse.
		:return: None
		"""

		# Each portion of a message is delimited by a space
		# Except for the escaped last argument, which is dealt with later
		parts = raw.split()

		# The source is optional - if it exists, it is prepended with a ":"
		if parts[0].startswith(':'):
			# hostmask will parse the information from the source
			self._source = hostmask(parts[0][1:])
			del parts[0]
		else:
			self._source = None

		# All IRC messages must contain a command
		if len(parts) == 0:
			raise ValueError('message contains no command')

		self._command = parts.pop(0)

		# The remaining parts are the arguments
		self._arguments = []
		while parts:
			# An argument starting with ":" means the remaining portion of the
			# message is intended to be parsed as a single argument
			if parts[0].startswith(':'):
				break
			else:
				self._arguments.append(parts.pop(0))

		# The previous while loop must have invoked "break"
		# This means there is an escaped argument in this message
		if parts:
			# Recreate the original format of the argument
			escaped = ' '.join(parts)
			# Add it to the list, ignoring its escape character ":"
			self._arguments.append(escaped[1:])

	@property
	def source(self):
		return self._source

	@property
	def command(self):
		return self._command

	@property
	def arguments(self):
		return self._arguments
