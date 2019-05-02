
#######################################################################

import re
import time
import t_webtool
import t_stocklib

#######################################################################

def loader_main():
    t_stocklib.start_collect(t_webtool.mkd(db=r'stocklib', user=r'root', passwd=r'admin'))

#######################################################################

def loader_phone(phones):
    # loader_phone(t_webtool.fget(r'e:/phone.txt').decode(r'gbk').split('\r\n'))
    provs = r''
    citys = r''

    number = 1
    for phone in phones:
        print(r'%s : %s' % (number, phone))
        bs = t_webtool.bs4get(r'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile' % phone)
        position = re.findall(r'卡号归属地(.*)卡 类 型', bs.text, re.DOTALL | re.MULTILINE)[0]
        position = re.findall(r'\w+', position)

        prov = position[0]
        city = prov

        if len(position) > 1:
            city = position[1]

        city = city.replace(r'市', r'')

        provs += prov
        provs += '\r\n'

        citys += city
        citys += '\r\n'

        number += 1
        time.sleep(0.1)

    print(r'省信息:')
    print(provs)

    print(r'市信息:')
    print(citys)

#######################################################################

if __name__ == "__main__":
    loader_main()
    print('bye...')

#######################################################################
