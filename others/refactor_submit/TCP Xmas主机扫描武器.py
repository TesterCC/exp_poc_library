# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""
Usage:
python "TCP Xmas主机扫描武器.py" --ip 10.0.4.148
python "TCP Xmas主机扫描武器.py" --ip 10.0.4.147-151
"""

from optparse import OptionParser
import nmap

ret = dict()
ret['status'] = None
ret['info'] = list()


def Scan(ip):
    try:
        nm = nmap.PortScanner()
        # TCP Xmas
        nm.scan(ip, arguments=' -sX')

        for host in nm.all_hosts():
            ret['info'].append({host: nm[host].get('addresses').get('mac')})
            ret['status'] = 'success'

    except:
        pass


def main():
    usage = "Usage: %prog --ip <ip address>"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")
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
