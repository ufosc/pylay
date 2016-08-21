import socket
from threading import Thread
from SocketServer import ThreadingMixIn

def handle_message(user, raw):
	m = Command(raw)

	quit = False
	if m.command == Command.NICK:
		print('NICK')
	if m.command == Command.USER:
		print('USER')
	if m.command == Command.QUIT:
		print('QUIT')

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
