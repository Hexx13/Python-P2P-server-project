
import os

file_list = os.listdir('')
for filename in sorted(file_list):
    print(filename) # print out one file name at a time.
    
    out_filename = 'out.mp3' # specify where the files will go
    
    # opening one file at a time, and adding to onto out.mpg
    with open(out_filename, 'ab') as outfile:
        with open('merge/' + filename, 'rb') as infile:
            outfile.write(infile.read()) # read the contents, add to output
           
            