import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print("starting client....")
print("making connection to server..")
sock.connect(server_address)


try:

    message=''

    while True:
        # Send data
        print("Please enter a command")
        message = input()
        if "hash" in message:
            print("hashing data...")
        elif "sendfile" in message:
            print("Please enter the file name to send")
            fileName = '../samplefile_1.mp3'  # input()
           
            with open(fileName, mode='rb') as file: # b is important -> binary
                fileContent = file.read()
                print(len(fileContent)) # print out how big the file is
                
                sock.sendall(fileContent)
                
        else:
            message = message.encode()
            sock.sendall(message) # send command to the server
               

finally:
    print('closing socket')
    sock.close()