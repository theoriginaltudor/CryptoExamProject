import socket               # Import socket module
import nacl.secret
import nacl.utils
from nacl.public import Box, PublicKey, PrivateKey
from nacl.encoding import HexEncoder

sk = PrivateKey.generate()
pk = sk.public_key
pkencoded = pk.encode(HexEncoder)
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))

pk_external = s.recv(64)
s.send(pkencoded)
loaded_public_key = PublicKey(pk_external, encoder=HexEncoder)
boxAsymmetric = Box(sk, loaded_public_key)
message = boxAsymmetric.encrypt(key)
s.send(message)
box = nacl.secret.SecretBox(key)

f = open('file.txt','rb')
print('Sending...')
l = box.encrypt(f.read(1024))
while (l):
    print('Sending...')
    s.send(l)
    l = box.encrypt(f.read(1024))
f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)
print(box.decrypt(s.recv(1024)))
s.close()     # Close the socket when done