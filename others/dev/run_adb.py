# coding=utf-8
"""
DATE:   2022/4/25
AUTHOR: TesterCC
"""

import os

cmd = r"adb version"

r = os.popen(cmd)
print(r.read())
