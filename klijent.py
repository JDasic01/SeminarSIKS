# kod za sockete je napravljen po https://www.youtube.com/watch?v=g1Jyi0qLuoU
import base64
from socket import *
from threading import *
from cryptography.fernet import Fernet
import time
import konfiguracijska_datoteka
from konfiguracijska_datoteka import fernet_kljuc_posluzitelj as fernet_decrypt
from konfiguracijska_datoteka import fernet_kljuc_klijent as fernet_encrypt

class ChatThread(Thread):
    def __init__(self,con):
        Thread.__init__(self)
        self.con=con
    def run(self):
        name=current_thread().getName()
        while True:
            if name=='Sender':
                msg = bytes(input(), 'utf-8')
                self.con.send(fernet_encrypt.encrypt(msg))
            elif name=='Receiver':
                msg = self.con.recv(1024)
                msg = fernet_decrypt.decrypt(msg) # dekripciju
                print("Posluzitelj: " +  msg.decode('utf-8')) # dekodiranje

client = socket()
client.connect(('127.0.0.1', 5050))

print("Autentifikacija u tijeku")
konfiguracijska_datoteka.AuthRSAServer()
time.sleep(1)
print("Razmjena kljuceva...")
konfiguracijska_datoteka.KeyExchangeX25519()
time.sleep(1)
print("Generiranje fernet kljuceva...")
time.sleep(1)
sender = ChatThread(client)
sender.setName('Sender')
receiver=ChatThread(client)
receiver.setName('Receiver')

sender.start()
receiver.start()