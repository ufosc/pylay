from server import *
from user import *
from common.reply import *
from common.command import *

class Handlers:

	@staticmethod
	def quit(serv, usr):
		serv.remove_user(usr)

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
			usr.register()
			usr.send(Message(serv.hostname, Reply.RPL.WELCOME, [
				'welcome to pylay IRC ' + format(usr.hostmask)
			]))

	@staticmethod
	def user(serv, usr, n, h, s, r):
		usr.update(username = n)
		if usr.can_register():
			usr.register()
			usr.send(Message(serv.hostname, Reply.RPL.WELCOME, [
				'welcome to pylay IRC ' + format(usr.hostmask)
			]))

	@staticmethod
	def privmsg(serv, usr, n, m):
		target = serv.find_user(n)
		if target is None:
			usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nickname'
			]))
			return

		target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
