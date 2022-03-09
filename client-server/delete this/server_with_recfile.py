import socket
import sys

tracker = list() # keep to track of songs added and removed


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


def parseCommand(cmd):
    global tracker # point to variable
    cmd = str(cmd)
    print("input" + cmd)
    
    if "[" in cmd:
        print("command found")
        if "[SONGFILENAME" in cmd: #cmd = '[SONGFILENAME-britney.mp3-127.0.0.1-10020]'
            cmd = cmd.replace(']','')
            values = cmd.split('-') # break up based on dash

            commandName = values[0] # get values from the string
            fileName = values[1]
            ipaddress = values[2]
            portnumber = values[3]
            
            newRec = list() # make new list
            newRec.append(fileName) #add data to the list
            newRec.append(ipaddress)
            newRec.append(portnumber)
   

         
            print("file name: " + fileName)
            print("ip address: " + ipaddress)
            
            print(newRec)
            
            
            
            # If nothing is in the tracker, add the song
            if(len(tracker)) == 0:
                tracker.append(newRec)
            else:    
                # see if the filename exists in the tracker    
                if newRec in tracker:
                    print("already have it, skip")               
                else:
                    print("adding song to tracker...")
                    tracker.append(newRec) # add the record to the tracker.
        elif "[SPLIT" in cmd:
            fs = FileSplit(file='samplefile.mp3', splitsize=50000, output_dir='..')
            fs.split()
                    


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        while True:        
            buffer = b''
            # Receive the data in small chunks
            data = connection.recv(4096)
            
            '''
            Here we will say if the command is a "split" command or a "songfilename"
            then run the usual parseCommand function.
            
            If it is not one of these commands, then run the ELSE statement
            which is designed to recv the data from the file being sent over
            and writing it to a file.
            
            After it has the data saved to a file, it goes back to regular
            
            command made. To test this, open the client and run and type "sendfile"
            you will see on the server the file will get transferred.
            
            '''
            if "[SPLIT" in str(data) or "[SONGFILENAME" in str(data):
                parseCommand(data)
            else:
                while data: # if it was not a command, it is a file being sent over.
                    print("looping over data coming in")
         
                    data = connection.recv(4096)
                    
                    buffer += data
                    
                    print("writing to file")
                    with open('../myfile.mp3', 'wb+') as w:
                        w.write(buffer)
                    print("finished writing")
                    break # get out of the while loop
                
        

    finally:
        # Clean up the connection
        connection.close()