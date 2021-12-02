# coding=utf-8
"""
DATE:   2021/12/1
AUTHOR: TesterCC
"""

# 生成字典工具
import itertools
words = "1234568790abcdefghijklmnopqrstuvwxyz"
temp =itertools.permutations(words,2)  # 位数越多，生成时间越长
passwords = open("dic.txt","a")
for i in temp:
   passwords.write("".join(i))
   passwords.write("".join("\n"))
passwords.close()

