from server import *
from user import *
from common.reply import *
from common.command import *

class Handlers:

	@staticmethod
	def quit(serv, usr):
		return False

	@staticmethod
	def nick(serv, usr, n):
		if (len(n) > 9):
			usr.send(Message(serv.hostname, Reply.ERR.ERRONEUSNICKNAME, [
				n, 'erroneous nickname'
			]))
			return True

		if serv.find_user(n) is not None:
			usr.send(Message(serv.hostname, Reply.ERR.NICKNAMEINUSE, [
				n, 'nickname is already in use'
			]))
			return True

		usr.update(nickname = n)
		return True

	@staticmethod
	def user(serv, usr, n, h, s, r):
		if usr.is_registered() or usr.hostmask.username is not None:
			usr.send(Message(serv.hostname, Reply.ERR.ALREADYREGISTERED, [
				'unauthorized command (already registered)'
			]))
			return True

		usr.update(username = n)
		return True

	@staticmethod
	def privmsg(serv, usr, n, m):
		target = serv.find_user(n)
		if target is None:
			usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nickname'
			]))
			return True

		target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
		return True
