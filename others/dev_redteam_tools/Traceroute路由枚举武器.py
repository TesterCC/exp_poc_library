# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""

traceroute是诊断网络问题时常用的工具。它可以定位从源主机到目标主机之间经过了哪些路由器，以及到达各个路由器的耗时。

Traceroute路由枚举(scapy)

Usage:
python Traceroute路由枚举武器.py --dst 10.0.4.148
python Traceroute路由枚举武器.py --dst cn.bing.com

ref:
https://stackoverflow.com/questions/1151771/how-can-i-perform-a-ping-or-traceroute-using-native-python/7018928
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


def route_scan(dst):
    ans, unans = sr(IP(dst=dst, ttl=(4, 25), id=RandShort()) / TCP(flags=0x2), timeout=45, verbose=False)
    if ans:
        for snd, rcv in ans:
            # print(snd.ttl, rcv.src, isinstance(rcv.payload, TCP))
            ret['status'] = "success"
            ret['info'].append({snd.ttl: rcv.src})


def route_scan_v2(dst):
    result, unans = traceroute(dst, maxttl=32, verbose=False)
    if result:
        for snd, rcv in result:
            # print(snd.ttl, rcv.src, isinstance(rcv.payload, TCP))
            ret['status'] = "success"
            # 返回路由表信息
            ret['info'].append((snd.ttl, rcv.src, isinstance(rcv.payload, TCP)))


def main():
    usage = "Usage: %prog --dst <ip address / domain>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--dst', type="string", dest="Destination", help="specify the IP address or domain")
    options, args = parse.parse_args()

    dst = options.Destination
    # print(">>>", dst)
    try:
        # route_scan(dst)

        dst = dst.split(",")
        route_scan_v2(dst)
    except Exception as err:
        import traceback;
        traceback.print_exc()
        ret['status'] = "fail"
        ret['info'] = "unknown error"

    print(json.dumps(ret))


if __name__ == '__main__':
    main()
