import socket  # Import socket module
import nacl.secret
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, Box, PublicKey

sk = PrivateKey.generate()
pk = sk.public_key
pkencoded = pk.encode(HexEncoder)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
f = open('torecv.txt','wb')
s.listen(1)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print("Got connection from", addr)
    c.send(pkencoded)
    pk_external = c.recv(1024)
    loaded_public_key = PublicKey(pk_external, encoder=HexEncoder)
    boxAsymmetric = Box(sk, loaded_public_key)
    message = c.recv(1024)
    plain_text = boxAsymmetric.decrypt(message)
    box = nacl.secret.SecretBox(plain_text)

    print("Receiving...")
    l = box.decrypt(c.recv(1024))
    while (l):
        print("Receiving...")
        f.write(l)
        l = box.decrypt(c.recv(1024))
    f.close()
    print("Done Receiving")
    c.send(box.encrypt(b"Thank you for connection"))
    c.close()                # Close the connection