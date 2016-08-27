from server import *
from user import *
from common.reply import *
from common.command import *

class Handlers:

	@staticmethod
	def quit(serv, usr):
		pass

	@staticmethod
	def nick(serv, usr, n):
		if (len(n) > 9):
			usr.send(Message(serv.hostname, Reply.ERR.ERRONEUSNICKNAME, [
				n, 'erroneous nickname'
			]))
			return

		if serv.find_user(n) is not None:
			usr.send(Message(serv.hostname, Reply.ERR.NICKNAMEINUSE, [
				n, 'nickname is already in use'
			]))
			return

		usr.update(nickname = n)
		if usr.can_register():
			serv.register_user(usr)

	@staticmethod
	def user(serv, usr, n, h, s, r):
		usr.update(username = n)
		if usr.can_register():
			serv.register_user(usr)

	@staticmethod
	def privmsg(serv, usr, n, m):
		target = serv.find_user(n)
		if target is None:
			usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nickname'
			]))
			return

		target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
