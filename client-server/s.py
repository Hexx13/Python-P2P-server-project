import hashlib
import os
import socket
import threading
from pydub import AudioSegment
from pydub.utils import make_chunks
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

cmdArr = ["servertime", "hello", "help", "addsong-(songName)", "removesong-(songname)", "getsong-(songname)",
          "hash-(songname)", "search", "slice-(songname)", "playsong"]
songs = list()


def hash(data, con):
    hasher = hashlib.sha256()
    name = process(data);

    # open file
    file = open(name, 'rb')
    content = file.read()

    # hash
    hasher.update(content)
    result = hasher.digest()

    con.send(str(result).encode())

# splits commands and returns the command extension
def process(data):
    arr = data.split('-')

    process1 = arr[1].translate({ord(':'): None})
    return process1.translate({ord("'"): None})

# lists songs on server
def search(con):
    files = os.listdir(path=os.getcwd())

    mp3s = list()

    for oneFile in files:
        if ".mp3" in oneFile:
            print(oneFile)
            mp3s.append(oneFile)

    con.send(str(mp3s).encode())

# custom command, deletes a song
def removeSong(data, con):
    print("song being removed......")

    if ".mp3" in str(data):
        os.remove(process(data))
        con.send("Song deleted".encode())

    else:
        con.send("Invalid file type".encode())

# server send song to client
def getSong(data, con):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("get file......")

    fileName = process(data)

    print("filename: " + str(fileName))
    print(f"sending file to {hostname}  {ip_address} ..................")

    f = open(fileName, 'rb')
    content = f.read()
    con.sendall(content)
    f.close()
    print("file recieved by client")

# client send song to server
def addSong(data, con):
    print("sond being added......")
    name = process(data)
    filename = name + '.mp3'
    print(filename)
    f = open(filename, 'wb')

    filedata = con.recv(1000)
    while filedata:
        print(filedata)
        f.write(filedata)
        filedata = con.recv(1000)

    f.close()
    songs.append(name)

# custom say hello command
def sayHello(con):
    print("----> The hello function was called")
    con.send("Hello from the server".encode())

# custom command list command
# Sends the list of commands to the client
def cmdList(con):
    messg = "Commands list: "
    for x in cmdArr:
        messg += x + ";    "
    con.send(messg.encode())

def getServTime(con):
    print("command in data..")
    con.send(str(strftime("%a, %d %b %Y %H:%M:%S", gmtime())).encode())

def createLog():
    logName = "Session " + str(strftime("%a %d %b %Y %H.%M.%S", gmtime())) + " HostName " + socket.gethostname() + ".txt"
    log = open(logName, 'w')
    log.close()
    return logName

def slice(data, con):
    print("get file......")
    fileName = process(data)
    print("slicing file......")
    myAudio = AudioSegment.from_file(fileName, "mp3")
    chunk_length_ms = 1000 * 30  # pydub calculates in millisec
    chunks = make_chunks(myAudio, chunk_length_ms)  # Make chunks of 30 seconds

    # Export all of the individual chunks as mp3 files

    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.mp3".format(i)
        chunk.export(chunk_name, format="mp3")

    con.sendall("Slicing finished".encode())

def parseInput(data, con):
    print("parsing...")
    print(str(data))

    # Checking for commands
    if "<getservertime" in data:
        getServTime(con)
    elif "<help" in data:
        cmdList(con)
    elif "<hello" in data:
        sayHello(con)
    elif "<addsong" in data:
        addSong(data, con)
    elif "<removesong" in data:
        removeSong(data, con)
    elif "<search" in data:
        search(con)
    elif "<getsong" in data:
        getSong(data, con)
    elif "<hash" in data:
        hash(data, con)
    elif "<slice" in data:
        slice(data, con)

def manageConnection(conn, addr):

    print('Connected by', addr)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    #creates log file
    logName = createLog()
    #open log file
    log = open(logName, 'w')
    #log ip and hostname
    log.write("Host connected: " + hostname + "Ip address: " + ip_address+"\r\n")

    data = conn.recv(1024)

    parseInput(str(data).lower(), conn)  # Calling the parser, passing the connection
    inpt = "rec:" + str(data)
    #log input
    log.write(inpt+"\r\n")
    print(inpt)

    log.close()
    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # Threading was implemented on the server-side to not interrupt the listening function for further connections.
    # This way the server can operate normally while clients are able to connect.
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
