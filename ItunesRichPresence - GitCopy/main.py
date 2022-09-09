__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "1.0"

from attributes import *

RPC = Presence(clientid, pipe = 0)
RPC.connect()

global track
global artist
global album
global startSong
global endSong
global art

print("RPC has started...")

def getInfo():
    global track
    global artist
    global album
    global art

    #Initial Information
    track = iTunes.CurrentTrack.Name
    artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
    album = iTunes.CurrentTrack.Album
    setTime()
    art = getArt()


def setTime():
    global startSong
    global endSong

    startSong = int(time.time()) - iTunes.PlayerPosition
    endSong = int(time.time()) + (iTunes.CurrentTrack.Duration - iTunes.PlayerPosition)

def getArt():
    with open(os.path.join(thisFolder, albumFile), 'r') as fp:
        lines = fp.readlines()
        for row in lines:
            word = iTunes.CurrentTrack.Album

            if row.find(word) == 0:
                 row.rstrip()
                 artwork = row.split(" - ")[1]
                 link = artwork.strip()
                 break
            else:
                link = "itunes_logo"
    fp.close()
    return link

#If initially Playing
if iTunes.PlayerState == 1:
    getInfo()
    RPC.update(state = artist, details = track, large_text = album, large_image=art, start = startSong, end = endSong)
else:
    track = None

while True:

    if iTunes.PlayerState == 1:

        if track == None:
            getInfo()

        if track != iTunes.CurrentTrack.Name:
            track = iTunes.CurrentTrack.Name

        if album != iTunes.CurrentTrack.Album:
            album = iTunes.CurrentTrack.Album
            artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
            art = getArt()

        setTime()

        RPC.update(state=artist, details=track, large_text=album, 
            large_image=art, start=startSong, end=endSong)
    elif iTunes.PlayerState == 0:
        RPC.clear()
    time.sleep(2)
