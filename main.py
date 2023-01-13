__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "3.0"

from attributes import *
from supabase import create_client

SUPABASE = create_client(SUPABASE_URL, SUPABASE_KEY)
RPC = Presence(CLIENT_ID, pipe = 0)
RPC.connect()

global track, artist, album, startSong, endSong, art, imPath, modAlbum

print("RPC has started...")
print("Press CTRL + C to quit RPC..\n")

def getInfo():
    global track, artist, album, art

    track = iTunes.CurrentTrack.Name
    artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
    album = iTunes.CurrentTrack.Album
    setTime()
    art = getLink()
    print("Playing Song: " + track + " by " + iTunes.CurrentTrack.Artist + " on " + album)

def setTime():
    global startSong, endSong

    startSong = int(time.time()) - iTunes.PlayerPosition
    endSong = int(time.time()) + (iTunes.CurrentTrack.Duration - iTunes.PlayerPosition)

def getLink():
    global modAlbum

    getArt()
    modAlbum = re.sub('[^0-9a-zA-Z]+', '', album)
    image = SUPABASE.storage().from_("albumimages").upload(modAlbum + ".png", imPath, {"content-type": "image/png" "lastmodified:"})
    link = SUPABASE.storage().from_("albumimages").get_public_url(modAlbum + ".png")

    return link


def getArt():
    global os
    global imPath
    global counter

    if (iTunes.playerState == 1):

        track = iTunes.CurrentTrack
        artwork = track.Artwork.Item(1)

        if (track.Artwork.Count == 1):
            full_path = os.path.realpath(__file__)
            imPath = os.path.dirname(full_path) + "\\" + "album.png"
            artwork.SaveArtworkToFile(imPath)


try:
    initial = 0
    while True:
        if iTunes.PlayerState == 1:
            if initial == 0:
                getInfo()
                initial = initial + 1

            if track != iTunes.CurrentTrack.Name:
                print("Playing Song: " + iTunes.CurrentTrack.Name + " by " + iTunes.CurrentTrack.Artist + " on " + iTunes.CurrentTrack.Album)
                track = iTunes.CurrentTrack.Name

            if album != iTunes.CurrentTrack.Album:
                remove = SUPABASE.storage().from_("albumimages").remove(modAlbum + ".png")
                album = iTunes.CurrentTrack.Album
                artist = iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album
                art = getLink()

            setTime()
            RPC.update(state=artist, details=track, large_text=album, 
                large_image=art, start=startSong, end=endSong)
        elif iTunes.PlayerState == 0:
            if initial != 0:
                RPC.clear()
        time.sleep(2)
except KeyboardInterrupt:
        print("RPC is closing.")
        remove = SUPABASE.storage().from_("albumimages").remove(modAlbum + ".png")
        exit()