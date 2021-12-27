# -*- coding: utf-8 -*-
# @Time    : 2021/12/23
# @Author  : SecCodeCat

from optparse import OptionParser

import re
import requests

from requests import session

ss = session()
ss.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


# cd ~/vulhub/zabbix/CVE-2016-10134/
def login(target_url, pwd, token):
    # todo
    '''尝试登陆'''
    data = {'pma_username': user,
            'pma_password': pwd,
            'server': 1,
            'target': 'index.php',
            'token': token}
    r = ss.post(url=target_url, data=data)
    return r.text


def main():
    usage = "Usage: %prog --ip <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="ip", help="server ip, e.g. 10.0.0.1")
    parse.add_option("-u", '--user', type="string", dest="username", default="guest", help="login user name")
    parse.add_option("-p", '--pw', type="string", dest="password", default="", help="login password")


if __name__ == '__main__':
    main()
