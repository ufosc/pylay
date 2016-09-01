from server.user import User
from server.error import NoUserError, NoChannelError, NotInChannelError
from common.message import Message
from common.reply import Reply
from common.command import Command
from common.error import BadNicknameError, BadChannelError

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
		except BadNicknameError:
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

def join(serv, usr, n):
	try:
		chan = serv.get_channel(n, True)
		serv.join_channel(chan, usr)
	except BadChannelError:
		usr.send(Message(serv.hostname, Reply.ERR.NOSUCHCHANNEL, [
			n, 'no such channel'
		]))

def privmsg(serv, usr, n, m):
	try:
		chan = serv.get_channel(n)
		us = serv.get_channel_users(chan)
		targets = [u for u in us if u != usr]

		for t in targets:
			t.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))

	except BadChannelError:
		try:
			target = serv.get_user(n)
			target.send(Message(usr.hostmask, Command.PRIVMSG, [n, m]))
		except NoUserError:
			usr.send(Message(serv.hostname, Reply.ERR.NOSUCHNICK, [
				n, 'no such nick'
			]))

	except NoChannelError:
		usr.send(Message(serv.hostname, Reply.ERR.NOSUCHCHANNEL, [
			n, 'no such channel'
		]))

def part(serv, usr, n):
	try:
		chan = serv.get_channel(n)
		serv.part_channel(chan, usr)

		targets = serv.get_channel_users(chan)
		for t in targets:
			t.send(Message(usr.hostmask, Command.PART, [n]))

	except (BadChannelError, NoChannelError):
		usr.send(Message(serv.hostname, Reply.ERR.NOSUCHCHANNEL, [
			n, 'no such channel'
		]))

	except NotInChannelError:
		usr.send(Message(serv.hostname, Reply.ERR.NOTONCHANNEL, [
			n, 'you\'re not on that channel'
		]))

handler_map = {
	Command.QUIT:    (None,  quit),
	Command.NICK:    (None,  nick),
	Command.USER:    (False, user),
	Command.JOIN:    (True,  join),
	Command.PRIVMSG: (True,  privmsg),
	Command.PART:    (True,  part),
}

def unknown_handler(serv, usr, cmd):
	usr.send(Message(serv.hostname, Reply.ERR.UNKNOWNCOMMAND, [
		cmd, 'unknown command'
	]))
