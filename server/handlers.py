from server.server import *
from server.user import *
from common.message import *
from common.reply import *
from common.command import *

class Handlers:

	@staticmethod
	def quit(serv, usr):
		serv.remove_user(usr)

	@staticmethod
	def nick(serv, usr, n):
		if len(n) > 9:
			usr.send(Message(serv.hostname, Reply.ERR.ERRONEUSNICKNAME, [
				n, 'erroneous nickname'
			]))
			return

		try:
			serv.get_user(n)
			usr.send(Message(serv.hostname, Reply.ERR.NICKNAMEINUSE, [
				n, 'nickname is already in use'
			]))
		except ValueError:
			pass

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
		try:
			target = serv.get_user(n)
			target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
		except ValueError:
			usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nickname'
			]))
