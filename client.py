#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

import ed25519
signing_key, verifying_key = ed25519.create_keypair()
vkey_hex = verifying_key.to_ascii(encoding="hex")

verifying_key_external = "empty"
name = input("Name: ")


def receive():
    """Handles receiving of messages."""

    global verifying_key_external

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")

            if (name + ":") in msg:
                print("already have my msg")

            else:
                if "~" in msg:
                    print(verifying_key_external.to_ascii(encoding="hex"))
                    message, signature = msg.split("~")
                    print(signature)
                    verifying_key_external.verify(signature.encode(), message.encode(), encoding="hex")
                    msg_list.insert(tkinter.END, message)
                elif "Greetings from the cave!" in msg:
                    msg_list.insert(tkinter.END, msg)
                    client_socket.send(bytes(name, "utf8"))
                elif "has joined the chat!" in msg:
                    msg_list.insert(tkinter.END, msg)
                    sendSignatureKey()
        except ed25519.BadSignatureError:  # Possibly client has left the chat.
            print("signature is bad!")
            break


def checkForSignature():
    f = open("verifyingKey.txt", "r")


def getSignatureKey(msg):
    global verifying_key_external
    someString, vk_hex = msg.split("{")
    verifying_key_external = ed25519.VerifyingKey(vk_hex.encode(), encoding="hex")
    print("got signature " + vk_hex)


def sendSignatureKey():
    message = "Key {" + vkey_hex.decode()
    f = open("verifyingKey.txt", "w")
    f.write(message)
    f.close()
    print("sent signature " + vkey_hex.decode())


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    msg_list.insert(tkinter.END, msg)
    signature = signing_key.sign(msg.encode(), encoding="hex")
    print(signature)
    msg1 = msg + "~" + signature.decode()
    client_socket.send(bytes(msg1, "utf8"))
    if "/" in msg:
        send_file(msg)
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def send_file(path):
    file = open(path, "r")
    msg = file.readline()
    while msg:
        signature = signing_key.sign(msg.encode(), encoding="hex")
        msg = msg + "~" + signature.decode()
        client_socket.send(bytes(msg, "utf8"))
        msg = file.readline()
    file.close()


def receive_file(msg):
    file = open("new.txt", "w")
    file.write(msg)
    file.close()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.