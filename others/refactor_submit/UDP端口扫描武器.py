# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json

"""
基于UDP的端口扫描(nmap)

Usage:
python UDP端口扫描武器.py --ip 10.0.4.148
python UDP端口扫描武器.py --ip 10.0.4.147-149
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
            # print(nm[host])
            ret['info'].append({host:list(nm[host].get('tcp').keys())})
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
