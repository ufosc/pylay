from common.message import Message

class Reply(Message):
	"""
	An IRC reply sent by a server.
	"""

	class RPL:
		"""
		Constants for all RPL_* IRC message codes.
		"""

		WELCOME  = 1
		YOURHOST = 2
		CREATED  = 3
		MYINFO   = 4

	class ERR:
		"""
		Constants for all ERR_* IRC message codes.
		"""

		UNKNOWNCOMMAND = 421
		NEEDMOREPARAMS = 461

		NOSUCHNICK       = 401
		NONICKNAMEGIVEN  = 431
		ERRONEUSNICKNAME = 432
		NICKNAMEINUSE    = 433
		NICKCOLLISION    = 436

		NOTREGISTERED     = 451
		ALREADYREGISTERED = 462

		NOSUCHCHANNEL = 403
		NOTONCHANNEL  = 442

	def __init__(self, raw):
		"""
		Create a command representation by parsing a raw received message.
		Similar to Command, but prefix is a string, and command is an int.

		@param raw The full message in string form.
		"""

		# Ignoret the CRLF
		parts = raw[:-2].split()

		pre = None
		if Message.has_prefix(raw):
			# A reply source is just the server name
			pre = parts[0][1:]
			del parts[0]

		if len(parts) == 0:
			raise ValueError('message has no command')

		# A reply command is just a 3-digit code
		cmd = int(parts[0])
		arg = ' '.join(parts[1:])

		Message.__init__(self, pre, cmd, Message.parse_arguments(arg))
