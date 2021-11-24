# coding=utf-8
'''
DATE: 2020/09/09
AUTHOR: Yanxi Li
'''
import json

"""
扫描原理：
1.参数接收
    参数值为要扫描的目标机器IP和端口
2.发送和收取相应包
3.包内容判断

本例，自己来构建SYN包来进行发包和收包并判断
其实也可以直接用socket模块进行构造，不过socket模块构造TCP包比较复杂

pip install scapy

Usage:
python tcp_syn_port_scan_scapy.py --ip 10.0.4.148 --port 22,25,80,443,8080,8000

SYN扫描：
使用SYN扫描的不同点就在于客户端收到SYN/ACK包响应后，客户端不返回ACK包响应，而是直接返回RST包响应请求端口连接，这样三次握手就没有完成。
我们通过前两个包已经确定了端口是否开放了，这就完成了端口的扫描，又不会在目标系统日志中记录日志。

备注：python本身就有nmap的第三方库
"""
from optparse import OptionParser
# import sys
from scapy.all import *
from scapy.layers.inet import IP, TCP

from scapy.utils import ContextManagerCaptureOutput

# initialization
ret = dict()
ret['status'] = None
ret['info'] = list()


def scan(ip, port):
    # print("Server %s, Port: %s is scaning" % (ip, port))

    try:
        # debug with pdb
        # import pdb;pdb.set_trace()

        port = int(port)

        src_port = RandShort()  # return random port， 0 to 2**16 (65536)
        # 获取一个响应包， flags S 代表SYN类型, res即是响包结果       # verbose=0，屏蔽console打印
        res = sr1(IP(dst=ip) / TCP(sport=src_port, dport=port, flags="S"), timeout=3, verbose=0)
        # 判断相应包里是否有TCP层
        if res.haslayer(TCP):
            if res.getlayer(TCP).flags == "SA":  # 判断是否是SYN_ACK
                sr(IP(dst=ip) / TCP(sport=src_port, dport=port, flags="AR"), timeout=3, verbose=0)
                # print("Result: OPEN")
                ret['info'].append(port)
                ret['status'] = 'success'
            elif res.getlayer(TCP).flags == "RA":  # 判断是否是RST_ACK
                # print("Result: CLOSE")
                pass
    except:
        # print("Scan error!")
        pass


def main():
    usage = "Usage: %prog -i <ip address>"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="TargetIP", help="specify the IP address")
    parse.add_option("-p", '--port', type="string", dest="TargetPort", help="specify the port,80 or 21,443,80")
    options, args = parse.parse_args()

    ip = options.TargetIP
    port = options.TargetPort.split(',')

    if ip and port:
        for _port in port:
            scan(ip, _port)
    else:
        ret['status'] = "fail"
        ret['info'] = "lack args, ip or port"

    print(json.dumps(ret))


if __name__ == '__main__':
    # ip = sys.argv[1]
    # port = sys.argv[2]
    # scan(ip, port)
    main()
