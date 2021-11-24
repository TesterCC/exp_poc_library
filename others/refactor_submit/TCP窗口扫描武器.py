# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json

"""
TCP窗口扫描(nmap)

原理：
客户端发送 ACK 数据包
服务端返回 RST 数据包，则该端口没有被过滤，
接着检查 RST 数据包中的窗口大小，如窗口大小值非零，则说明端口开放，为 0 则说明端口关闭

Usage:
python TCP窗口扫描武器.py --ip 10.0.4.148
python TCP窗口扫描武器.py --ip 10.0.4.147-151
"""

from optparse import OptionParser
import nmap

ret = dict()
ret['status'] = None
ret['info'] = list()


def Scan(ip):
    try:
        nm = nmap.PortScanner()
        # TCP Window Scan
        nm.scan(ip, arguments=' -sW')

        for host in nm.all_hosts():
            print({host: nm[host].get('addresses').get('mac')})
            ret['info'].append({host: nm[host].get('addresses').get('mac')})
            ret['status'] = 'success'
    except:
        pass


def main():
    usage = "Usage: %prog --ip <ip address>"
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
