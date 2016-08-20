class Reply:
	"""
	An IRC reply sent by a server.
	"""

	def __init__(self, raw):
		"""
		Create a command representation by parsing a raw received message.
		Similar to Command, but prefix is a string, and command is an int.

		:param raw: The full message in string form.
		:return: None
		"""

		parts = raw.split()

		pre = None
		if Message.has_prefix(raw):
			# A reply source is just the server name
			pre = parts[0][1:]
			del parts[0]

		if len(parts) == 0:
			raise ValueError('message has no command')

		# A reply command is just a 3-digit code
		cmd  = int(parts[0])
		args = Message.parse_arguments(parts[1:])

		Message.__init__(self, pre, cmd, args)
