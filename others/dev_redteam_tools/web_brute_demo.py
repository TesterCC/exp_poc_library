# -*- coding: utf-8 -*-
# @Time    : 2021/12/3
# @Author  : SecCodeCat

import requests

url = "http://192.168.157.160/pikachu/vul/burteforce/bf_form.php"
username = "admin"
password = "111111"
data = {
    "username": username.strip(),
    "password": password.strip(),
    "submit": "Login"
}
print('-' * 20)
print('用户名：', username.strip())
print('密码：', password.strip())
resp = requests.post(url, data=data)
print("The status_code is %d" % (resp.status_code))

