import sys

from common.message import *

line = sys.stdin.readline()

msg = Message(line)
print(format(msg))
