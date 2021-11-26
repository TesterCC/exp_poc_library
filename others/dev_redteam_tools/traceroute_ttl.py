# coding=utf-8
"""
DATE:   2021/11/26
AUTHOR: TesterCC
"""
"""
ref:
https://www.cnblogs.com/LyShark/p/12411435.html#_label0
"""

from scapy.all import *
from scapy.layers.inet import IP, ICMP
from random import randint
import time,ipaddress,threading
from optparse import OptionParser

def ICMP_Ping(addr):
    RandomID=randint(1,65534)
    packet = IP(dst=addr, ttl=64, id=RandomID) / ICMP(id=RandomID, seq=RandomID) / "testercc"
    respon = sr1(packet,timeout=3,verbose=0)
    if respon:
        print("[+] --> {}".format(str(respon[IP].src)))

def TraceRouteTTL(addr):
    for item in range(1,128):
        RandomID=randint(1,65534)
        packet = IP(dst=addr, ttl=item, id=RandomID) / ICMP(id=RandomID, seq=RandomID)
        respon = sr1(packet,timeout=3,verbose=0)
        if respon != None:
            ip_src = str(respon[IP].src)
            if ip_src != addr:
                print("[+] --> {}".format(str(respon[IP].src)))
            else:
                print("[+] --> {}".format(str(respon[IP].src)))
                return 1
        else:
            print("[-] --> TimeOut")
        time.sleep(1)

if __name__== "__main__":
    parser = OptionParser()
    parser.add_option("--mode",dest="mode",help="选择使用的工具模式<ping/trace>")
    parser.add_option("-a","--addr",dest="addr",help="指定一个IP地址或范围")
    (options,args) = parser.parse_args()
    # 使用方式: main.py --mode=ping -a 192.168.1.0/24
    if options.mode == "ping":
        net = ipaddress.ip_network(str(options.addr))
        for item in net:
            t = threading.Thread(target=ICMP_Ping,args=(str(item),))
            t.start()
    # 使用方式: main.py --mode=trace -a 61.135.169.121
    elif options.mode == "trace":
        TraceRouteTTL(str(options.addr))
    else:
        parser.print_help()