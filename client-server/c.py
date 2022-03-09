
# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connecting to server.....")

try:
    print("Type help if you want the command list")
    print("type input:")

    text = input()


    # when we send data to the server, we are using a colon
    # at the end of a sentence to mark the end of the current sentence
    # later when the input comes back, we will then be breaking the input
    # into individual parts using the colon : to separate the lines
    s.sendall(("<" + text + ">" + ":").encode())

    if "addsong" in text:
        "Loading file send...."

        fileChunk = open('c0part.mp3', 'rb')
        theStuff = fileChunk.read()
        s.sendall(theStuff)
        fileChunk.close()


    data = s.recv(80000)


    print("Response:" + str(data))
finally:
    print("closing connection.....")
    s.close()
