import socket  # Import socket module
import nacl.secret
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey, SealedBox

sk = PrivateKey.generate()
pk = sk.public_key
print(pk)
pkencoded = pk.encode(HexEncoder)
print(pkencoded)
unsealing_box = SealedBox(sk)

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
f = open('torecv.txt','wb')
s.listen(2)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print("Got connection from", addr)
    c.send(pkencoded)
    message = c.recv(1024)
    plain_text = unsealing_box.decrypt(message)
    print("Symmetric key: ", plain_text)
    box = nacl.secret.SecretBox(plain_text)

    print("Receiving...")
    l = box.decrypt(c.recv(1024))
    while (l):
        print("Receiving...")
        f.write(l)
        l = box.decrypt(c.recv(1024))
    f.close()
    print("Done Receiving")
    c.send(b"Thank you for connection")
    c.close()                # Close the connection