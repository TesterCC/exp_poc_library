# coding=utf-8
"""
DATE:   2021/8/13
AUTHOR: TesterCC
"""
import json

"""
基于ICMP的主机发现

Usage:
python ICMP主机发现武器.py --ip 10.0.4.148
python ICMP主机发现武器.py --ip 10.0.4.140-149
"""

from random import randint
from optparse import OptionParser

from scapy.all import *
from scapy.layers.inet import IP, ICMP

import threading

ret = dict()
ret['status'] = None
ret['info'] = list()

def Scan(ip):

    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet = IP(dst=ip, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'scc'
    result = sr1(packet, timeout=1, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src

            ret['status'] = 'success'

            ret['info'].append(scan_ip)


def main():
    parser = OptionParser("Usage:%prog --ip <target host> ")
    parser.add_option('--ip', type='string', dest='IP',
                      help='specify target host, e.g. 10.0.0.1 or 10.0.0.1-20')
    options, args = parser.parse_args()

    if '-' in options.IP:
        for i in range(int(options.IP.split('-')[0].split('.')[3]), int(options.IP.split('-')[1]) + 1):
            tip = options.IP.split('.')[0] + '.' + options.IP.split('.')[1] + '.' + options.IP.split('.')[
                2] + '.' + str(i)

            threads = []
            t = threading.Thread(target=Scan, args=(tip,))
            threads.append(t)
            t.start()
            t.join()

    else:
        Scan(options.IP)

    print(json.dumps(ret))


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")

