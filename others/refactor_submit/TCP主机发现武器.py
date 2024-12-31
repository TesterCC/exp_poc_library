# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""
基于TCP的主机发现(nmap)

Usage:
python TCP主机发现武器.py --ip 10.0.4.148
python TCP主机发现武器.py --ip 10.0.4.147-151
"""
import json
from optparse import OptionParser
import nmap

ret = dict()
ret['status'] = None
ret['info'] = list()


def Scan(ip):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, arguments=' -sT')   # 将与目标端口进行三次握手，尝试建立连接，如果连接成功，则端口开放，速度慢，会被目录主机记录

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
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
