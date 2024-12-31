# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""
import json

"""
基于nmap的主机发现

Usage:
python 主机发现武器.py --ip 10.0.4.148
python 主机发现武器.py --ip 10.0.4.145-151
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
        # -sn:使用ping进行扫描  只是测试该主机状态
        # -PE:使用ICMP的 echo请求包(-PP:使用timestamp请求包 -PM:netmask请求包)
        result = nm.scan(hosts=ip, arguments='-sn -PE')

        # 对结果进行切片，提取主机状态信息
        state = result['scan'][ip]['status']['state']
        # print("[+] {} is {}".format(ip, state))
        if state == "up":
            ret['info'].append(ip)
            ret['status'] = 'success'

    except:
        # import traceback;traceback.print_exc()
        pass


def main():
    usage = "Usage: %prog -i <ip address>"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")  # 获取网段地址
    options, args = parse.parse_args()

    try:
        if '-' in options.targetIP:
            for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):
                Scan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' +
                     options.targetIP.split('.')[2] + '.' + str(i))
        else:
            Scan(options.targetIP)
    except Exception as err:
        ret['status'] = 'fail'
        ret['info'] = str(err)

    print(json.dumps(ret))


if __name__ == '__main__':
    main()
