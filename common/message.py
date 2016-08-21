class Message(object):
	"""
	A generic IRC message from a client or server.
	"""

	@staticmethod
	def has_prefix(raw):
		"""
		Check if a message contains a prefixed server/client source.
		The message prefix is optional, and usually present only for replies.

		:param raw: The message in string form.
		:return: A boolean representing whether or not a prefix exists.
		"""

		return raw.startswith(':')

	@staticmethod
	def parse_arguments(arg):
		"""
		Split a single argument string into individual arguments.

		:param arg: The arguments as a single string.
		:return: A list of arguments.
		"""

		args = []

		parts = arg.split()
		while parts:
			# An argument starting with ":" means the remaining portion of the
			# message is intended to be parsed as a single argument
			if parts[0].startswith(':'):
				break
			else:
				args.append(parts.pop(0))

		# The previous while loop must have invoked "break"
		# This means there is an escaped argument in this message
		if parts:
			# Recreate the original format of the argument
			escaped = ' '.join(parts)
			# Add it to the list, ignoring its escape character ":"
			args.append(escaped[1:])

		return args

	def __init__(self, pre, cmd, args):
		"""
		Create a new message with the given parts

		:param pre: The prefix of the message, or None.
		:param cmd: The main command (an all-caps name or a code).
		:param arg: The arguments.
		:return: None
		"""

		self._prefix = pre
		self._command = cmd
		self._arguments = args

	def __format__(self, spec):
		"""
		Format a message as it would be sent to a client or server.

		:param spec: The character encoding. Unused.
		:return: The message formatted as a string.
		"""

		# Accumlate the individual parts of the message
		result = ""

		# The prefix is optional
		if self._prefix is not None:
			src = format(self._prefix)
			# When the source exists, it is always prepended by a ':'
			result += ":{} ".format(src)

		# The command always exists
		result += "{} ".format(self._command)
		# Concat all arguments but the last (may need escaping)
		if len(self._arguments[:-1]) > 0:
			result += "{} ".format(' '.join(self._arguments[:-1]))

		# If the last argument has a space, it must be escaped with ':'
		if ' ' in self._arguments[-1]:
			result += ":{}".format(self._arguments[-1])
		else:
			result += "{}".format(self._arguments[-1])

		return (result + '\r\n')

	@property
	def prefix(self):
		return self._prefix

	@property
	def command(self):
		return self._command

	@property
	def arguments(self):
		return self._arguments
