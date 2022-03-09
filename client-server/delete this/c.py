import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50006         # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("type 1 to run the add song")
print("type 2 to get a song")
print("type 3 for the filesize")
print("type 4 for the ip of user")
print("type 5 for hash")
print("type <search + file name to search")
print("type input:")
text = input()

if "1" in text:
    text = '<addsong-chunk0.mp3>'
elif "2" in text:
    text = '<get-chunk0.mp3>'
elif "3" in text:
    text = "<filesize"
elif "4" in text:
    text = "<ip"
elif "5" in text:
    text = "<hash"

# when we send data to the server, we are using a colon
# at the end of a sentence to mark the end of the current sentence
# later when the input comes back, we will then be breaking the input
# into individual parts using the colon : to separate the lines
s.sendall((text + ":").encode())
if "<hash" in text:
    ans = s.recv(1000)
    print(ans)

if "<addsong" in text:
    print("getting ready to send file....")

    # read in the file chunk
    chunk = open('c0part.mp3', 'rb')
    content = chunk.read()
    s.sendall(content)
    chunk.close()
elif "<get" in text:
    parts = text.split("-")
    print(parts[0])
    print(parts[1])

    f = open('c0part.mp3', 'wb')
    filedata = s.recv(1000)

    while filedata:
        print(filedata)
        f.write(filedata)
        filedata = s.recv(1000)

    f.close()
if "quit" in text:
    quit()
s.close()
