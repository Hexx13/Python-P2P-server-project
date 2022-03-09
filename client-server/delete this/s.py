import socket
import threading
import os
import hashlib

from time import gmtime, strftime
import time
listOfSongs = list()

HOST = '127.0.0.1'        
PORT = 50006
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
    
# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""   

# custom say hello command

def sayHello():
    print ("----> The hello function was called")

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.

def parseInput(data, con):
    print("parsing...")
    print(str(data))
    
    # Checking for commands
    if "<filesize" in str(data):
        path = 'chunk0.mp3'
        size = os.path.getsize(path)
        print(size)

    if "<getservertime>" in data:
        print("command in data..")
        formatted= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        con.send(str(formatted).encode())

    elif "<addsong" in str(data):
        print("adding song....")
        items = data.split('-')
        print(items[0])
        print(items[1])
        print(items[2])

        f = open('c0.mp3', 'wb')

        filedata = con.recv(1000)
        while filedata:
            print(filedata)
            f.write(filedata)
            filedata = con.recv(1000)

        f.close()
        listOfSongs.append(items[1])

    elif "<ip" in str(data):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")

    elif "<get" in str(data):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print("getting file")
        parts = str(data).split('-')
        fileName = parts[1]
        print("filename: " + str(fileName))
        print("sending the file")
        cleanedName = fileName[0:-3]
        print(cleanedName)

        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")

        f = open(cleanedName, 'rb')
        content = f.read()
        con.sendall(content)
        f.close()
        print("send the file")

    elif "<search" in str(data):
        files = os.listdir(path="../../..")
        newList = list()

        for oneFile in files:
            if ".mp3" in oneFile:
                print(oneFile)

        con.send(str(newList).encode())

    elif "<hash" in str(data):
        m = hashlib.sha256()
        # read in the file
        file = open('chunk0.mp3', 'rb')
        content = file.read()
        # get the hash
        m.update(content)
        res = m.digest()
        print(res)
        con.send(str(res).encode())

# we make a new thread is started from an incoming connection
# the manageConnection function is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)
    
    parseInput(str(data), conn)# Calling the parser, passing the connection
    
    print("rec:" + str(data))
    buffer += str(data)
    
    #conn.send(str(buffer))
        
    conn.close()

while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    


