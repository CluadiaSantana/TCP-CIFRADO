import socket
import os
import nacl.utils
from Crypto.Cipher import AES
from base64 import b64encode

class randomPynacl():
    def __init__(self, bytes):
        self._bytes = bytes
        self._buf= nacl.utils.random(self._bytes)
    
    def changeBits(self,bytes):
        self._bytes = bytes
    
    def Random(self):
        self._buf= nacl.utils.random(self._bytes)

    def PrintRandom(self):
        for number in self._buf:
            print(f'{hex(number)[2:]}',end = " ")
    
    def strRandom(self):
        random=''
        for number in self._buf:
            if len(hex(number)[2:])==1:
                random+="0"
            random+= hex(number)[2:]
            random+= ""
        return random

# se crea el socket para el servidor
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#se pone el host de mi localhost y el port 5500 (es el que tengo configurado) tambien se pone que archivo se enviara
host="127.0.0.1"
port=5500
FILE = "Hola.txt"
#se crea el random que se utilizara
random=randomPynacl(16)
random=random.strRandom()
#se asgignan los valores que se utilizan en el AES
key = random.encode()
cipher = AES.new(key, AES.MODE_EAX)
d_cipher=AES.new(key, AES.MODE_EAX, cipher.nonce)
#el archivo se abre y se guarda la data en original
with open(FILE, 'rb') as file:
    original = file.read()
#se encripta el data del archivo
cipherfile = cipher.encrypt(original)
#se sobre-escribe el archivo con el data encriptado
with open(FILE, 'wb') as encrypted_file:
    encrypted_file.write(cipherfile)
#se le asigna al servidor el host y el puerto
serversocket.bind((host,port))
#se configura para que empiece a escuchar
serversocket.listen(3)
print(f'El servidor esta escuchando en {host} puerto {port}')
while True: #siempre se estara escuchando
    # se aceptan conexiones del exterior
    (clientsocket, address) = serversocket.accept()
    print(f'Se ha conectado con el cliente {address}')
    with clientsocket:
        #se manda el archivo
        with open(FILE, 'rb') as f:
            clientsocket.sendfile(f)
            print("El archivo se ha enviado")
    #se desencripta para checar que este correcta la encriptacion esto se poede comentar para checar que los dos archivos coinciden cuando estan encriptados
    decrypted = d_cipher.decrypt(cipherfile)
    with open(FILE, 'wb') as dec_file:
        dec_file.write(decrypted)

