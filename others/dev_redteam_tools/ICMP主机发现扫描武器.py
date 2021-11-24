# coding=utf-8
"""
DATE:   2021/8/13
AUTHOR: TesterCC
"""

"""
基于ICMP的主机发现

1.用scapy 发送ping请求 和 接收目标主机的应答数据， random用于产生随意字段，optparse用于处理命令行参数
2.对用户输入的参数进行接收和批量处理，并将处理后的IP地址传入Scan函数

缺点：
当网络设备，例如：路由器、防火墙等对ICMP采取了屏蔽策略时，就会导致扫描结果不准确。

Usage:

python ICMP主机发现武器.py --ip 10.0.4.140-149
"""

from random import randint
from optparse import OptionParser

from scapy.all import *
# scapy库里有一个all.py文件，这一句就是把all.py文件里面所有函数和变量导入当前环境
from scapy.layers.inet import IP, ICMP  # 这些指定协议在新版本scapy中都是通过all.py来加载了

import threading

# initialization
ret = dict()
ret['status'] = None
ret['info'] = list()

def Scan(ip):
    # ICMP扫描逻辑核心
    ip_id = randint(1, 65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet = IP(dst=ip, ttl=64, id=ip_id) / ICMP(id=icmp_id, seq=icmp_seq) / b'scc'
    result = sr1(packet, timeout=1, verbose=False)
    if result:
        for rcv in result:
            scan_ip = rcv[IP].src
            # print(scan_ip + '--->' 'Host is up')  # Debug
            ret['status'] = 'success'
            # ret['info'][scan_ip] = True
            ret['info'].append(scan_ip)
    else:
        # print(ip + '--->' 'host is down')
        pass


# 多线程，效率也不高，CPython GIL的问题，只比单线程快几秒
def main():
    parser = OptionParser("Usage:%prog --ip <target host> ")  # 输出帮助信息  是optparse定义的格式化字符串符号，表示本程序的文件名。比如你的文件为xxx.py
    parser.add_option('--ip', type='string', dest='IP',
                      help='specify target host, e.g. 10.0.0.1 or 10.0.0.1-20')  # 获取ip地址参数
    options, args = parser.parse_args()
    # print(type(options)) # 'optparse.Values'
    # print(options) # {'IP': '10.0.4.1-20'}
    # print("Scan report for " + options.IP + "\n")
    # 判断是单台主机还是多台主机
    # ip中存在-,说明是要扫描多台主机
    if '-' in options.IP:
        # 代码意思举例：192.168.1.1-120
        # 通过'-'进行分割，把192.168.1.1和120进行分离
        # 把192.168.1.1通过','进行分割,取最后一个数作为range函数的start,然后把120+1作为range函数的stop
        # 这样循环遍历出需要扫描的IP地址
        for i in range(int(options.IP.split('-')[0].split('.')[3]), int(options.IP.split('-')[1]) + 1):
            tip = options.IP.split('.')[0] + '.' + options.IP.split('.')[1] + '.' + options.IP.split('.')[
                2] + '.' + str(i)
            # multi thread
            threads = []
            t = threading.Thread(target=Scan, args=(tip,))
            threads.append(t)
            t.start()
            t.join()

    else:
        Scan(options.IP)

    print(json.dumps(ret))
    # print("[+]Scan finished!....\n")


if __name__ == "__main__":

    try:
        # st = time.time()
        main()
        # print(f"[+] cost time: {time.time() - st}")   # 39.4721
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")

