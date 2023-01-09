__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "2.0"

from attributes import *
from supabase import create_client

SUPABASE = create_client(SUPABASE_URL, SUPABASE_KEY)
RPC = Presence(CLIENT_ID, pipe = 0)
RPC.connect()

global track, artist, album, startSong, endSong, art

print("RPC has started...")
print("Press CTRL + C to quit RPC..\n")

def getInfo():
    global track, artist, album, art

    #Initial Information
    track = iTunes.CurrentTrack.Name
    artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
    album = iTunes.CurrentTrack.Album
    setTime()
    art = getLink()


def setTime():
    global startSong, endSong

    startSong = int(time.time()) - iTunes.PlayerPosition
    endSong = int(time.time()) + (iTunes.CurrentTrack.Duration - iTunes.PlayerPosition)

def getLink():
    link = SUPABASE.storage().from_("albumimages").get_public_url(iTunes.CurrentTrack.Artist + "/" + album + ".png")

    string = link.split("/")

    albumLoc = len(string) - 1
    artistLoc = len(string) - 2

    string[albumLoc] = string[albumLoc].replace(" ", "%20")

    if "," in string[artistLoc]:
        string[artistLoc] = string[artistLoc][0:string[artistLoc].index(',')]
    elif "&" in string[artistLoc]:
        string[artistLoc] = string[artistLoc][0:string[artistLoc].index(' &')]
  

    if " " in string[artistLoc]:
        string[artistLoc] = string[artistLoc].replace(" ", "%20")

    if ":" in string[albumLoc]:
      string[albumLoc] = string[albumLoc].replace(":", "")
    
    string = "/".join(string)
  
    link = string

    return link


#If initially Playing
if iTunes.PlayerState == 1:
    getInfo()
    print("Playing Song: " + iTunes.CurrentTrack.Name + " by " + iTunes.CurrentTrack.Artist + " on " + iTunes.CurrentTrack.Album)
    RPC.update(state = artist, details = track, large_text = album, large_image=art, start = startSong, end = endSong)
else:
    track = None

while True:

    if iTunes.PlayerState == 1:

        if track == None:
            getInfo()

        if track != iTunes.CurrentTrack.Name:
            print("Playing Song: " + iTunes.CurrentTrack.Name + " by " + iTunes.CurrentTrack.Artist + " on " + iTunes.CurrentTrack.Album)
            track = iTunes.CurrentTrack.Name

        if album != iTunes.CurrentTrack.Album:
            album = iTunes.CurrentTrack.Album
            artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
            art = getLink()

        setTime()

        
        RPC.update(state=artist, details=track, large_text=album, 
            large_image=art, start=startSong, end=endSong)
    elif iTunes.PlayerState == 0:
        RPC.clear()
    time.sleep(2)
