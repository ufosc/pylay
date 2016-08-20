import sys

from common.message import *

line = sys.stdin.readline()

msg = Message(line)

print(msg.command)
for arg in msg.arguments:
	print(arg)
