from server.server import Server
from common.command import Command
from sys import argv

from server.handlers import handler_map, check_state
from server.handlers import unknown_handler, invalid_handler

def handle_message(serv, usr, data):
	try:
		msg = Command(data)
		(state, handler) = handler_map[msg.command]
		if check_state(serv, usr, state):
			handler(serv, usr, *msg.arguments)

	except ValueError:
		pass

	except KeyError:
		unknown_handler(serv, usr, msg.command)

	except TypeError:
		invalid_handler(serv, usr, msg.command)

argc = len(argv)
ip   = '127.0.0.1' if (argc < 2) else argv[1]
port = 7000 if (argc < 3) else int(argv[2])

serv = Server()
serv.start(ip, port, lambda usr, data:
	handle_message(serv, usr, data)
)
