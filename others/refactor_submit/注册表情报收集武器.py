# coding=utf-8
"""
DATE:   2021/12/7
AUTHOR: TesterCC
"""
import json
import platform
import sys

system_version = platform.system()

ret = dict()
ret['status'] = None
ret['info'] = None

if system_version == 'Windows':
    from winreg import *
else:
    ret['status'] = 'fail'
    ret['info'] = "non windows platform"
    print(json.dumps(ret))
    sys.exit()

def get_userinfo():
    ret['info'] = list()
    # 连接注册表根键 以HKEY_LOCAL_MACHINE为例
    regRoot = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    subDir = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList'

    # 获取指定目录下所有键的控制
    keyHandle = OpenKey(regRoot, subDir)

    # 获取该目录下所有键的个数(0-下属键个数 1-当前键值个数)
    count = QueryInfoKey(keyHandle)[0]
    for i in range(count):
        # 穷举键获取键名
        subKeyName = EnumKey(keyHandle, i)
        subDir_2 = r'%s\%s' % (subDir, subKeyName)

        # 根据获取的键名拼接之前的路径作为参数 获取当前键下所属键的控制
        keyHandle_2 = OpenKey(regRoot, subDir_2)
        num = QueryInfoKey(keyHandle_2)[1]
        for j in range(num):
            name, value, type_ = EnumValue(keyHandle_2, j)
            if ('ProfileImagePath' in name and 'Users' in value):
                # print(value)
                ret['status'] = 'success'
                ret['info'].append(value)
        # 读写操作结束后关闭键
        CloseKey(keyHandle_2)

    # 关闭键值
    CloseKey(keyHandle)
    CloseKey(regRoot)


if __name__ == '__main__':
    try:

        get_userinfo()

    except:
        pass

    print(json.dumps(ret))