#coding: utf-8

from Crypto.Cipher import AES

class Encryption:

    def __init__(self):
        passLenght = len(self.encryptionKey)
        if passLenght < 16:
            symbols = ['!' for _ in xrange(16 - passLenght)]
            self.encryptionKey += ''.join(symbols)

    def _getChiper(self):
        return AES.new(self.encryptionKey, AES.MODE_CFB, '_+UlD:IQ*8[;}jzp')

    def encrypt(self, data):
        chiper = self._getChiper()
        return chiper.encrypt(data)

    def decrypt(self, data):
        chiper = self._getChiper()
        db = chiper.decrypt(data)

        try:
            db.decode('utf-8')
        except:
            raise Exception('Неверный пароль!')

        return db


