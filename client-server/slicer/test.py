from pydub import AudioSegment
from pydub.utils import make_chunks

import os


file_name = "britney.mp3"




myaudio = AudioSegment.from_file(file_name , "mp3") 
chunk_length_ms = 1000*30 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of 30 seconds

#Export all of the individual chunks as mp3 files

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.mp3".format(i)
    chunk.export(chunk_name, format="mp3")