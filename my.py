import subprocess
import sys

# Use os executing to avoid the dependency of mysql.connector
def my_exe(host, port, user, pp, db, query, fmt):
	if len(fmt) == 0:
		fmt = '--table'
	else:
		fmt = {
			'v': '--vertical',
			'tab': '--batch',
			't': '--table',
		}[fmt]
	query = ' '.join(query.split())

	args = ['mysql', '-h', host, '-P', port, '-u', user, '--database=%s' % db, '--comments', fmt, '-e', query]

	if sys.version_info.major == 2:
		cmd = subprocess.Popen(args, stdout=subprocess.PIPE, env={'MYSQL_PWD': pp})
	else:
		cmd = subprocess.Popen(args, stdout=subprocess.PIPE, env={'MYSQL_PWD': pp}, encoding='utf8')
	cmd.wait()
	if cmd.returncode != 0:
		sys.stderr.write('***\n')
		sys.stderr.write(query)
		sys.stderr.write('\n***\n')
		sys.stderr.write(cmd.stdout.read())
		raise Exception('os.wait: exit status != 0')

	lines = cmd.stdout.readlines()
	if len(lines) > 0:
		lines = lines[1:]

	result = []
	for line in lines:
		if len(line) != 0:
			line = line[:-1]
		if sys.version_info.major == 2:
			line = line.encode('utf8')
		cols = line.split('\t')
		if len(cols) == 1:
			result.append(cols[0])
		else:
			result.append(cols)
	return result
