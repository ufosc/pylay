from server.user import User
from server.error import NoUserError
from common.message import Message
from common.reply import Reply
from common.command import Command
from common.error import NicknameError

def check_state(serv, usr, state):
	if state == True and not usr.is_registered():
		usr.send(Message(serv.hostname, Reply.ERR.NOTREGISTERED, [
			'you have not registered'
		]))
		return False

	elif state == False and usr.is_registered():
		usr.send(Message(serv.hostname, Reply.ERR.ALREADYREGISTERED, [
			'unauthorized command (already registered)'
		]))
		return False

	else:
		return True

def quit(serv, usr):
	serv.remove_user(usr)

def nick(serv, usr, n):
	try:
		serv.get_user(n)
		usr.send(Message(serv.hostname, Reply.ERR.NICKNAMEINUSE, [
			n, 'nickname is already in use'
		]))
	except NoUserError:
		try:
			usr.update(nickname = n)
			if usr.can_register():
				usr.register()
				usr.send(Message(serv.hostname, Reply.RPL.WELCOME, [
					'welcome to pylay IRC ' + format(usr.hostmask)
				]))
		except NicknameError:
			usr.send(Message(serv.hostname, Reply.ERR.ERRONEUSNICKNAME, [
				n, 'erroneous nickname'
			]))

def user(serv, usr, n, h, s, r):
	usr.update(username = n)
	if usr.can_register():
		usr.register()
		usr.send(Message(serv.hostname, Reply.RPL.WELCOME, [
			'welcome to pylay IRC ' + format(usr.hostmask)
		]))

def privmsg(serv, usr, n, m):
	try:
		target = serv.get_user(n)
		target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
	except NoUserError:
		usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
			n, 'no such nickname'
		]))

handler_map = {
	Command.QUIT:    (None,  quit),
	Command.NICK:    (None,  nick),
	Command.USER:    (False, user),
	Command.PRIVMSG: (True,  privmsg)
}

def unknown_handler(serv, usr, state):
	usr.send(Message(serv.hostname, Reply.ERR.UNKNOWNCOMMAND, [
		msg.command, 'unknown command'
	]))
