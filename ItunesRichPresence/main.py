from pypresence import Presence
import time
import win32com.client
import os

client_id = "1017221480909651989"
RPC = Presence(client_id, pipe = 0)
RPC.connect()

iTunes = win32com.client.Dispatch("iTunes.Application")

while True:
    startSong = int(time.time()) - iTunes.PlayerPosition
    endSong = int(time.time()) + (iTunes.CurrentTrack.Duration - iTunes.PlayerPosition)

    with open (r'albums.txt', 'r') as fp:
        lines = fp.readlines()
        for row in lines:
            word = iTunes.CurrentTrack.Album

            if row.find(word) == 0:
                 row.rstrip()
                 artwork =  newLine = row.split(" - ")[1]
    fp.close()

    link = artwork.strip()
    if iTunes.PlayerState == 1:
        name = iTunes.CurrentTrack.Name
        artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
        text = iTunes.CurrentTrack.Album

    RPC.update(state=artist, details=name, large_text=text, 
        large_image=link, start=startSong, end=endSong)

    time.sleep(5)

