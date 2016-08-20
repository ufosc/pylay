import sys

from common.message import *

line = sys.stdin.readline()

msg = message(line)

print(msg.command)
for arg in msg.arguments:
	print(arg)
