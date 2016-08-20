import sys

from common.hostmask import *

line = sys.stdin.readline()

hs = hostmask(line)
if hs is None:
	print("invalid hostname {}".format(line))
else:
	print("nick: {}".format(hs.nick))
	print("user: {}".format(hs.user))
	print("hostt: {}".format(hs.host))
