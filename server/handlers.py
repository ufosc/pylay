from server import *
from user import *
from common.reply import *

class Handlers:

	@staticmethod
	def nick(serv, usr, n):
		if (len(n) > 9):
			return Message(serv.hostname, Reply.ERR.ERRONEUSNICKNAME, [
				n, 'erroneous nickname'
			])

		if serv.find_user(n) is not None:
			return Message(serv.hostname, Reply.ERR.NICKNAMEINUSE, [
				n, 'nickname is already in use'
			])

		usr.nickname = n
		return None

	@staticmethod
	def user(serv, usr, n, h, s, r):
		if usr.is_registered() or usr.username is not None:
			return Message(serv.hostname, Reply.ERR.ALREADYREGISTERED, [
				'unauthorized command (already registered)'
			])

		usr.username = n
		return None
