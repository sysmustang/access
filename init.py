#!/usr/bin/python
#coding: utf-8


import argparse
import subprocess


class Config:
    storage = '/etc/access_data'

    def __init__(self, **kwargs):
        for atname in kwargs.keys():
            setattr(self, atname, kwargs[atname])

class Init:
    password = False
    action = ''


    def __init__(self):
        parser = argparse.ArgumentParser(description='''Хранилище доступов и прочей важной инфы.
        Запуск без аргументов - просмотр БД. It's coded by Mustang''')
        parser.add_argument('-e', '--edit', action='store_true', help='Редактирование БД')
        parser.add_argument('-s', '--setup', action='store_true', help='Установка БД')
        self.arguments = parser.parse_args()

        uid = int(subprocess.check_output(['/usr/bin/id', '-u']))
        if uid != 0:
            raise Exception('Похоже нехватает прав.. Are you root?')

        self._getAction()
        self._getPassword()

    def _getAction(self):
        args = vars(self.arguments)

        for action in args.keys():
            if args[action]:
                self.action = action[0].upper() + action[1:]
                return

        self.action = 'Show'

    def _getPassword(self):
        subprocess.call(["echo -n 'Password: '"], shell=True)
        try:
            password = subprocess.check_output(["bash -c 'read -s password;echo $password'"], shell=True).strip()
        except KeyboardInterrupt:
            subprocess.call('reset')
            exit()
        # Перенос строки
        print('')

        if password:
            self.password = password
        else:
            exit()


    def getConfig(self):
        thisConfiguration = Config(password=self.password, action=self.action)
        return thisConfiguration
