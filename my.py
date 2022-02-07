import os

# Use os executing to avoid the dependency of mysql.connector
def my_exe(host, port, user, db, query, fmt):
	if len(fmt) == 0:
		fmt = '--table'
	else:
		fmt = {
			'v': '--vertical',
			'tab': '--batch',
			't': '--table',
		}[fmt]
	query = ' '.join(query.split())
	cmd_line='mysql -h "%s" -P "%s" -u "%s" --database="%s" --comments %s -e "%s"' % (host, port, user, db, fmt, query)

	lines = os.popen(cmd_line).readlines()
	if len(lines) > 0:
		lines = lines[1:]

	result = []
	for line in lines:
		if len(line) != 0:
			line = line[:-1]
		result.append(line.split('\t'))
	return result
