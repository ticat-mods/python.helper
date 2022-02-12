# -*- coding: utf-8 -*-

def colorize(code, origin):
	if code <= 0 or code >= 256:
		return origin
	return '\033[38;5;' + str(code) + 'm' + origin + '\033[0m'

def to_true(s):
	return s.lower() in ['true', 't', 'yes', 'y', 'on', '1']

def to_false(s):
	return s.lower() in ['false', 'f', 'no', 'n', 'off', '0']
