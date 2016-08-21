from message import *
from hostmask import *

class Command(Message):
	"""
	An IRC command sent by a client.
	"""

	NICK    = "NICK"
	USER    = "USER"
	JOIN    = "JOIN"
	PRIVMSG = "PRIVMSG"
	PART    = "PART"
	QUIT    = "QUIT"

	def __init__(self, raw):
		"""
		Create a command representation by parsing a raw received message.
		Use functionality from Message, then create a Hostmask from the prefix.

		:param raw: The full message in string form.
		:return: None
		"""

		parts = raw.split()

		pre = None
		if Message.has_prefix(raw):
			# Create a hostmask from the prefix, ignoring the ':' at the start
			pre = Hostmask.from_raw(parts[0][1:])
			del parts[0]

		if len(parts) == 0:
			raise ValueError('message has no command')

		cmd = parts[0]
		# Every 'part' after the command is an argument
		arg = ' '.join(parts[1:])

		Message.__init__(self, pre, cmd, Message.parse_arguments(arg))
