import hostmask

class message:

	def __init__(self, raw):
		parts = raw.split()

		if parts[0].startswith(':'):
			self._source = hostmask(parts[0][1:])
			del parts[0]
		else
			self._source = None

		if len(parts) == 0:
			raise ValueError('message contains no command')

		self._command = parts.pop(0)

		self._parameters = []
		while parts:
			if param.startswith(':'):
				break
			else:
				self._parameters.append(parts.pop())

		if parts:
			escaped = ''.join(parts)
			self._parameters.append(escaped[1:])

	@property
	def source(self):
		return self._source
