import os

def ssh_exe(host, cmd, user = ''):
	if len(user) != 0:
		user += '@'
	cmd_line = 'ssh -o "StrictHostKeyChecking=no" -o "BatchMode=yes" "' + user + host + '" ' + cmd + ' </dev/null'
	os.system(cmd_line)
