# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""
基于UDP的活跃主机发现技术
UDP没有三次握手，目标不会回应任何UDP数据包
当向目标发送一个UDP数据包之后：
- 如果目标主机处于活跃状态，但目标端口关闭，会返回一个ICMP数据包，数据包的含义为unreachable
- 如果目标主机处于未活跃状态，则收不到任何回应

基于UDP的主机发现(nmap)

Usage:
python UDP主机发现扫描武器.py --ip 10.0.4.148
python UDP主机发现扫描武器.py --ip 10.0.4.140-149
"""

from optparse import OptionParser
import nmap

ret = dict()
ret['status'] = None
ret['info'] = list()


def Scan(ip):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments=' -PU')

        for host in nm.all_hosts():
            ret['info'].append(host)
            ret['status'] = 'success'

    except Exception as err:
        ret['status'] = 'fail'
        ret['info'] = str(err)


def main():
    usage = "Usage: %prog -i <ip address>"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")  # 获取网段地址
    options, args = parse.parse_args()
    if '-' in options.targetIP:
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):
            Scan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' +
                 options.targetIP.split('.')[2] + '.' + str(i))
    else:
        Scan(options.targetIP)
    print(ret)


if __name__ == '__main__':
    main()
