# -*- coding: utf-8 -*-

import sys
import os
from copy import deepcopy

class Env:
	def __init__(self, parse_from_env_file = True):
		self._pairs = {}
		self._keys = []
		self._prefix_for_get = ''
		self._deleted_keys = []
		self._modified_keys = set()
		if not parse_from_env_file:
			return
		self._parse_from_env_file()

	def _parse_from_env_file(self):
		if len(sys.argv) <= 1:
			raise Exception('no env file path in sys.argv')
		path = os.path.join(sys.argv[1], 'env')
		file = open(path)
		self._parse_from(file)
		file.close()

	def _parse_from(self, reader):
		while True:
			line = reader.readline()
			if not line:
				break
			if len(line) == 0:
				continue
			line = line[:-1]
			if len(line) == 0:
				continue
			i = line.find('=')
			if i < 0:
				raise Exception('bad ticat env line: ' + line)
			k = line[:i]
			v = line[i+1:]
			self._keys.append(k)
			self._pairs[k] = v

	def write_to_env_file(*envs):
		modified = False
		for env in envs:
			if env.modified():
				modified = True
				break
		if not modified:
			return
		path = os.path.join(sys.argv[1], 'env')
		file = open(path, 'a')
		for env in envs:
			env._write_to(file)
		file.close()

	def _write_to(self, writer):
		for k in self._deleted_keys:
			writer.write(k + '=--\n')
		for k in self._modified_keys:
			writer.write(k + '=' + self._pairs[k] + '\n')

	def dump(self):
		for k in self._keys:
			print(k[len(self._prefix_for_get):] + ' (' + k + ') = ' + self._pairs[k])

	def keys(self):
		res = []
		for k in self._keys:
			res.append(k[len(self._prefix_for_get):])
		return res

	def get_ex(self, key, default):
		key = self._prefix_for_get + key
		if key not in self._pairs:
			return default
		return self._pairs[key]

	def get(self, key):
		return self._pairs[self._prefix_for_get + key]

	def has(self, key):
		return (self._prefix_for_get + key) in self._pairs

	def detach_prefix(self, prefix):
		prefix = self._prefix_for_get + prefix
		self._keys, keys = [], self._keys
		env = Env(False)
		env._deleted_keys = deepcopy(self._deleted_keys)
		env._modified_keys = deepcopy(self._modified_keys)
		env._prefix_for_get = prefix
		for k in keys:
			if not k.startswith(prefix):
				self._keys.append(k)
			else:
				env._keys.append(k)
				env._pairs[k] = self._pairs[k]
				del self._pairs[k]
		return env

	def with_prefix(self, prefix):
		prefix = self._prefix_for_get + prefix
		env = Env(False)
		env._deleted_keys = deepcopy(self._deleted_keys)
		env._modified_keys = deepcopy(self._modified_keys)
		env._prefix_for_get = prefix
		for k in self._keys:
			if not k.startswith(prefix):
				continue
			env._keys.append(k)
			env._pairs[k] = self._pairs[k]
		return env

	# TODO: this is slow, use r-index?
	def delete(self, key):
		deleted = False
		origin = key
		key = self._prefix_for_get + key
		self._keys, keys = [], self._keys
		for k in keys:
			if k != key:
				self._keys.append(k)
			else:
				self._deleted_keys.append(k)
				del self._pairs[k]
				deleted = True
		if not deleted:
			raise Exception('key ' + origin + ' (' + key + ') not found')

	def delete_all(self):
		self._deleted_keys += self.keys
		self._keys = []

	def set(self, key, val):
		key = self._prefix_for_get + key
		self._pairs[key] = val
		self._modified_keys.add(key)

	def modified(self):
		return len(self._modified_keys) + len(self._deleted_keys) > 0

