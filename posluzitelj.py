# kod za sockete je napravljen po https://www.youtube.com/watch?v=g1Jyi0qLuoU
from socket import *
from threading import *
import time
from cryptography.fernet import Fernet
import konfiguracijska_datoteka
from konfiguracijska_datoteka import fernet_kljuc_klijent as fernet_decrypt
from konfiguracijska_datoteka import fernet_kljuc_posluzitelj as fernet_encrypt
from konfiguracijska_datoteka import aad, nonce, data, ct

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
                msg =  fernet_decrypt.decrypt(msg)
                print("Klijent: " + msg.decode('utf-8'))


server = socket(AF_INET, SOCK_STREAM) # AF family net , slanje podataka
server.bind(('127.0.0.1', 5050)) # prva adresa, lokalno, 5050 port
server.listen(2)                # dva klijenta
conn, addr = server.accept()

print("Autentifikacija u tijeku")
konfiguracijska_datoteka.AuthRSAServer()
time.sleep(1)
print("Razmjena kljuceva...")
konfiguracijska_datoteka.KeyExchangeX25519()
time.sleep(1)
print("Generiranje fernet kljuceva...")
time.sleep(1)

sender = ChatThread(conn)
sender.setName('Sender')
receiver=ChatThread(conn)
receiver.setName('Receiver')

sender.start()
receiver.start()