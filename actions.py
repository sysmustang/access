#coding: utf-8

import os
import subprocess
from crypto import Encryption

class Base(Encryption):

    def __init__(self, config):
        self.encryptionKey = config.password
        self.storagePath = config.storage

        Encryption.__init__(self)

    def readDB(self):
        with open(self.storagePath, 'rb') as storage:
            encrypted = storage.read()

        data = self.decrypt(encrypted)
        return data

    def writeDB(self, data):
        with open(self.storagePath, 'wb') as storage:
            encrypted = self.encrypt(data)
            storage.write(encrypted)

    def existsDB(self):
        if not os.path.exists(self.storagePath):
            raise Exception('Сначала засетапь БД!')


class Show(Base):

    def run(self):
        self.existsDB()
        data = self.readDB().strip()
        print(data)

class Edit(Base):

    def run(self):
        self.existsDB()
        data = self.readDB()

        tpath = subprocess.check_output(['/bin/mktemp']).strip()
        os.chmod(tpath, 600)

        with open(tpath, 'wb') as tempStorage:
            tempStorage.write(data)

        subprocess.call(['vi ' + tpath], shell=True)

        selection = raw_input('База данных будет обновлена, продолжить? (y/n): ')
        while selection != 'y' and selection != 'n':
            selection = raw_input('База данных будет обновлена, продолжить? (y/n): ')

        if selection == 'n':
            return

        with open(tpath, 'rb') as tempStorage:
            editData = tempStorage.read()

        os.unlink(tpath)
        self.writeDB(editData)


class Setup(Base):

    def run(self):
        if os.path.exists(self.storagePath):
            selection = raw_input('Текущая база данных будет удалена, продолжить? (y/n): ')
            while selection != 'y' and selection != 'n':
                selection = raw_input('Текущая база данных будет удалена, продолжить? (y/n): ')

            if selection == 'n':
                return

            os.unlink(self.storagePath)

        os.chmod(self.storagePath, 600)
        self.writeDB('Здесь храним креды и прочую важную инфу\n')

        print('[OK] База данных успешно создана')
