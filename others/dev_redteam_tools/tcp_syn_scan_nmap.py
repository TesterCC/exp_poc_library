# coding=utf-8
"""
DATE:   2021/11/22
AUTHOR: TesterCC
"""

"""
TCP SYN扫描(nmap)
包含端口和应用信息

Usage:
python tcp_syn_port_scan_scapy.py --ip 10.0.4.148
python tcp_syn_port_scan_scapy.py --ip 10.0.4.140-149
"""

from optparse import OptionParser
import nmap


def Scan(ip):
    try:
        lport = None
        nm = nmap.PortScanner()
        nm.scan(ip)  # 将与目标端口进行三次握手，尝试建立连接，如果连接成功，则端口开放，速度慢，会被目录主机记录

        for host in nm.all_hosts():
            print('HOST: {0} ({1})'.format(host, nm[host].hostname()))
            print('State: {0}'.format(nm[host].state()))

            for proto in nm[host].all_protocols():
                print('Protocol: {0}'.format(proto))
                lport = list(nm[host][proto].keys())

        lport.sort()
        for port in lport:
            print("port: {0}\tstate: {1}".format(port, nm[host][proto][port]))

            # ret['info'].append(host)
            # ret['status'] = 'success'

    except Exception as err:
        pass
        # ret['status'] = 'fail'
        # ret['info'] = str(err)


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


if __name__ == '__main__':
    main()
