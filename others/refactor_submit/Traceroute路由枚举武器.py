# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""
traceroute是诊断网络问题时常用的工具。它可以定位从源主机到目标主机之间经过了哪些路由器，以及到达各个路由器的耗时。


Usage:
python Traceroute路由枚举武器.py --dst 10.0.4.148
python Traceroute路由枚举武器.py --dst cn.bing.com
"""

import json

from optparse import OptionParser
from scapy.all import *
from scapy.layers.inet import IP, TCP, traceroute

from optparse import OptionParser
import nmap

# initialization
ret = dict()
ret['status'] = None
ret['info'] = list()

def route_scan_v2(dst):
    result, unans = traceroute(dst, maxttl=32, verbose=False)
    if result:
        for snd, rcv in result:
            ret['status'] = "success"
            # 返回路由表信息
            ret['info'].append((snd.ttl, rcv.src, isinstance(rcv.payload, TCP)))


def main():
    usage = "Usage: %prog --dst <ip address / domain>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--dst', type="string", dest="Destination", help="specify the IP address or domain")
    options, args = parse.parse_args()

    dst = options.Destination

    try:
        dst = dst.split(",")
        route_scan_v2(dst)
    except Exception as err:
        ret['status'] = "fail"
        ret['info'] = str(err)

    print(json.dumps(ret))


if __name__ == '__main__':
    main()
