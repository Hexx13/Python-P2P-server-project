import socket
import threading

from time import gmtime, strftime
import time

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""
cmdArr = ["servertime", "hello", "help"]
songs = list()

#todo make this be able handle other files apart from c0.mp3
def addSong(data, con):
    print("sond being added......")
    arr = data.split('-')
    for x in arr:
        print(x)

    f = open('c0.mp3', 'wb')

    filedata = con.recv(1000)
    while filedata:
        print(filedata)
        f.write(filedata)
        filedata = con.recv(1000)

    f.close()
    songs.append(arr[1])

# custom say hello command
def sayHello(con):
    print("----> The hello function was called")
    con.send("Hello from the server".encode())


# custom command list command
# S ends the list of commands to the client
def cmdList(con):
    messg = "Commands list: "
    for x in cmdArr:
        messg += x + ";    "
    con.send(messg.encode())


def getServTime(con):
    print("command in data..")
    formatted = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    con.send(str(formatted).encode())


# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    print("parsing...")
    print(str(data))

    # Checking for commands
    if "<getservertime>" in data:
        getServTime(con)
    elif "<help>" in data:
        cmdList(con)
    elif "<hello>" in data:
        sayHello(con)


# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)

    parseInput(str(data), conn)  # Calling the parser, passing the connection

    print("rec:" + str(data))
    buffer += str(data)

    # conn.send(str(buffer))

    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
