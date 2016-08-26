from server import *
from user import *
from common.reply import *
from common.command import *

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

		usr.update(nickname = n)
		return None

	@staticmethod
	def user(serv, usr, n, h, s, r):
		if usr.is_registered() or usr.hostmask.username is not None:
			return Message(serv.hostname, Reply.ERR.ALREADYREGISTERED, [
				'unauthorized command (already registered)'
			])

		usr.update(username = n)
		return None

	@staticmethod
	def privmsg(serv, usr, n, m):
		target = serv.find_user(n)
		if target is None:
			return Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nickname'
			])

		msg = Message(usr.hostmask, Command.PRIVMSG, [n, m])
		target[1].send(format(msg))
		return None
