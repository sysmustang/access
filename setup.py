#!/usr/bin/python
#coding: utf-8

import os
from subprocess import Popen, PIPE

def isSetup():
    if not os.path.islink('/usr/bin/access'):
        return False

    if not os.path.exists('/usr/share/access'):
        return False

    return True

def install():
    if os.getuid() != 0:
        raise Exception('Похоже нехватает прав.. Are you root?')

    access_dir = os.path.dirname(__file__)
    copy = Popen(['/bin/cp', '-r', access_dir, '/usr/share/access'], stderr=PIPE)
    copy.wait()

    if not os.path.isdir('/usr/share/access'):
        raise Exception('Ошибка копирования в /usr/share!')

    os.symlink('/usr/share/access/access.py', '/usr/bin/access')

    if not os.path.islink('/usr/bin/access'):
        raise Exception('Ошибка создания симлинка /usr/bin/access')

if __name__ == '__main__':
    if isSetup():
        print('Access установлен!')
        exit()

    try:
        install()
        print('Access установлен!')
    except Exception as e:
        print('ERROR: \033[1m{}\033[0m'.format(e))


