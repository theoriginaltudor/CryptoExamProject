import socket               # Import socket module
import nacl.secret
import nacl.utils
from nacl.public import Box, PublicKey, PrivateKey
from nacl.encoding import HexEncoder

sk = PrivateKey.generate()
print("Client's secret key : ", sk)
pk = sk.public_key
print("Client's public key: ", pk)
pkencoded = pk.encode(HexEncoder)
key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                 # Reserve a port for your service.

s.connect((host, port))

pk_external = s.recv(64)
print("Public key received from server: ", pk_external)
s.send(pkencoded)
loaded_public_key = PublicKey(pk_external, encoder=HexEncoder)
boxAsymmetric = Box(sk, loaded_public_key)
print("This box contains client secret key and Server's public key : ", boxAsymmetric)

message = boxAsymmetric.encrypt(key)  # Encrypt secret key of Client
s.send(message)                       # Sending secret key encrypted
box = nacl.secret.SecretBox(key)      # creating a secret box for the message

f = open('file.txt', 'rb')
print('Sending...')
l = box.encrypt(f.read(1024))  # Encryption of message
print("This is the encrypted message: ", l)
while (l):
    print('Sending...')
    s.send(l)
    l = box.encrypt(f.read(1024))
f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024))
s.close()     # Close the socket when done
