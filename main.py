__author__ = "SnowTempest"
__copyright__ = "Copyright (C) 2022 SnowTempest"
__license__ = "NONE"
__version__= "4.0"

from attributes import *
from supabase import create_client

SUPABASE = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    RPC = pypresence.Presence(CLIENT_ID, pipe = 0)
except pypresence.exceptions.DiscordNotFound:
        print("\nDiscord is either not open or not installed on this system. ItunesRPC will safely close.")
        exit()

RPC.connect()

global track, artist, album, startSong, endSong, art, imPath, modAlbum

print("RPC has started...")
print("Press CTRL + C to quit RPC..\n")

def getInfo():
    global track, artist, album, art

    track = setTrack()
    artist = setArtist()
    album = setAlbum()
    setTime()
    art = getLink()
    currentlyPlaying()


#Uploads album art to Supabase and retrieves the uploaded album art as a link.
def getLink():
    global modAlbum

    getArt()
    modAlbum = re.sub('[^0-9a-zA-Z]+', '', album)
    try:
        image = SUPABASE.storage().from_("albumimages").upload(modAlbum + ".png", imPath, {"content-type": "image/png" "lastmodified:"})
    except StorageException:
            print("Album image is duplicated in the database and must be deleted. ItunesRPC will delete this image and close. Please restart to continue.55")
            close()
    link = SUPABASE.storage().from_("albumimages").get_public_url(modAlbum + ".png")

    return link

#Downloads the album art from itunes and stores it into were this is located.
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

def removeImage():
    remove = SUPABASE.storage().from_("albumimages").remove(modAlbum + ".png")

def setArtist():
    return iTunes.CurrentTrack.Artist + " | " + iTunes.CurrentTrack.Album

def setTrack():
    return iTunes.CurrentTrack.Name

def setAlbum():
    return iTunes.CurrentTrack.Album

def setTime():
    global startSong, endSong

    startSong = int(time.time()) - iTunes.PlayerPosition
    endSong = int(time.time()) + (iTunes.CurrentTrack.Duration - iTunes.PlayerPosition)

def currentlyPlaying():
    print("Playing Song: " + iTunes.CurrentTrack.Name + " by " + iTunes.CurrentTrack.Artist + " on " + iTunes.CurrentTrack.Album)

def close():
    removeImage()
    exit()

try:
    initial = 0
    while True:
        if iTunes.PlayerState == 1:
            if initial == 0:
                getInfo()
                initial = initial + 1

            if track != iTunes.CurrentTrack.Name:
                currentlyPlaying()
                track = setTrack()
                artist = setArtist()

            if album != iTunes.CurrentTrack.Album:
                removeImage()
                album = setAlbum()
                artist = setArtist()
                art = getLink()

            setTime()
            RPC.update(state=artist, details=track, large_text=album, 
                large_image=art, start=startSong, end=endSong)
        elif iTunes.PlayerState == 0:
            if initial != 0:
                RPC.clear()
        time.sleep(2)
except KeyboardInterrupt:
        print("\nItunesRPC will close.")
        close()
except pypresence.exceptions.InvalidID:
        print("\nDiscord either closed or crashed. ItunesRPC will safely close.")
        close()
except com_error:
        print("\nItunes has been closed unexpectedly. ItunesRPC will safely close.")
        close()