# Echo client program
import socket

HOST = '127.0.0.1'  # The remote host
PORT = 50007  # The same port as used by the server



exit = 0

def playSong():
    print("Please type which file you would like to play")
    import webbrowser
    webbrowser.open(input())


def addSong(filename):
    print("Loading file send....")

    # read chunk
    fileChunk = open(filename, 'rb')
    # store chunk
    theStuff = fileChunk.read()
    # send to server
    s.sendall(theStuff)
    # close chunk
    fileChunk.close()

#client side recieving song from server
def getSong():
    # stuff = str(data).split("'")
    print("Please choose a name for the downloading file")

    filename = input() + '.mp3'
    print(f"Downloading: {filename} ..............")
    f = open(filename, 'wb')
    data = s.recv(1000)

    while data:
        print(data)
        f.write(data)
        data = s.recv(1000)

    f.close()


cmdArr = ["servertime", "hello", "search", "addsong", "removesong", "getsong",
          "hash", "slice", "playsong"]


def buildMenu():
    print("Input a number corresponding to the commands below")
    # Array of commands

    numbr = 0;
    # Prints the array of commands
    for i in cmdArr:
        numbr += 1
        print(f"{numbr} - {i}")


def menu():
    buildMenu()

    inpt = int(input())

    if 4 > inpt > 0:
        s.sendall(("<" + cmdArr[inpt - 1] + ":").encode())
        print("Response:" + str(s.recv(1000)))
    elif inpt == 4:
        print("Please select name for file")
        name = input()
        s.sendall(("<" + cmdArr[inpt - 1] + "-" + name + ":").encode())
        print("Please type the filepath of the song")
        addSong(input())
    elif inpt == 5:
        print("Please select a file to remove")
        name = input()
        s.sendall(("<" + cmdArr[inpt - 1] + "-" + name + ":").encode())
        print("Please type the filepath of the song")
        print("Response:" + str(s.recv(1000)))
    elif inpt == 6:
        print("Please select a file to download")
        name = input()
        s.sendall(("<" + cmdArr[inpt - 1] + "-" + name + ":").encode())
        getSong()
    elif inpt == 7:
        print("Please select a file to hash")
        name = input()
        s.sendall(("<" + cmdArr[inpt - 1] + "-" + name + ":").encode())
        print("Response:" + str(s.recv(1000)))
    elif inpt == 8:
        print("Please select a song to slice")
        name = input()
        s.sendall(("<" + cmdArr[inpt - 1] + "-" + name + ":").encode())
        print("Response:" + str(s.recv(1000)))
    elif inpt == 9:
        playSong()
    else:
        print("Not an option, try again")
        menu()


def cli():
    print("Type help if you want the command list")
    print("type input:")

    text = input()

    s.sendall(("<" + text + ":").encode())
    if "addsong" in text:
        print("Please type filepath to song you want to add")
        addSong(input())
    elif "playsong" in text:
        playSong()
    elif "getsong" in text:
        getSong()
    else:
        print("Response:" + str(s.recv(1000)))


def mode():
    print("Input 1 if you wish to use the menu system")
    print("Input 2 if you wish to use the command-line system")
    print("Input 3 if you want to exit the system")
    mode = input()
    if "1" in mode:
        menu()
    elif "2" in mode:
        cli()
    elif "3" in mode:
        global exit
        exit = 1
    else:
        print("Not an option, try again")
        mode()


try:

    while exit == 0:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("connecting to server.....")
        mode()
finally:
    print("closing connection.....")
    s.close()
