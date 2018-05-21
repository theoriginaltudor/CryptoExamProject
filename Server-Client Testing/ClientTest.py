import socket               # Import socket module
import nacl.secret
import nacl.utils
from nacl.public import SealedBox, PublicKey
from nacl.encoding import HexEncoder

key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))

pk = s.recv(64)
loaded_public_key = PublicKey(pk, encoder=HexEncoder)
sealing_box = SealedBox(loaded_public_key)
print(key)
message = sealing_box.encrypt(key)
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
print(s.recv(1024))
s.close()     # Close the socket when done