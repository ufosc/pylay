import socket
from threading import Thread
from SocketServer import ThreadingMixIn

from common.command import *
from user import *

def handle_message(u, raw):
	m = Command(raw)

	quit = False
	if m.command == Command.NICK:
		u.nickname = m.arguments[0]
	if m.command == Command.USER:
		u.username = m.arguments[0]
	if m.command == Command.QUIT:
		quit = True

	hm = u.make_hostmask()
	if hm is not None:
		output = "{} is now registered!".format(format(hm))
		print(output)

	return quit

class ClientListener(Thread):

	def __init__(self, usr, conn):
		Thread.__init__(self)

		self._user = usr
		self._connection = conn

	def run(self):
		while True:
			data = self._connection.recv(512)
			if not data:
				break

			quit = handle_message(self._user, data)
			if quit:
				break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

sock.bind(('127.0.0.1', 7000))
while True:
	sock.listen(0)
	(conn, addr) = sock.accept()

	user = User(addr)
	listener = ClientListener(user, conn)
	listener.start()
