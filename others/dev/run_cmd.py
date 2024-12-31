# coding=utf-8
"""
DATE:   2022/4/25
AUTHOR: TesterCC
"""

import os

cmd = r"androbugs -f D:\ChromeDownload\app2.apk -o C:\Users\Yilan\Reports\test"
r = os.popen(cmd)

print(r.read())