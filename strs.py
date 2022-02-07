# -*- coding: utf-8 -*-

def colorize(code, origin):
	if code <= 0 or code >= 256:
		return origin
	return '\033[38;5;' + str(code) + 'm' + origin + '\033[0m'
