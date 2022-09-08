from pypresence import Presence
import time
import win32com.client


def main():

    iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
    library = iTunes.LibraryPlaylist
    tracks = library.Tracks
    track_count = tracks.Count

    i = 1
    for track_index in range(i, track_count+1):
        track = tracks.Item(track_index)
        artwork = track.Artwork.Item(1)
        print(track.Name)

        if track.Artwork.Count == 1:
            artwork.SaveArtworkToFile("D:\College\Coding\Python\ItunesRichPresence\Images" + "\\" + track.Album  + ".png")


def safePrint(label, data):
    print (label) 
    try:
        print (data)
    except UnicodeEncodeError:
        print (repr(data))

if __name__ == '__main__':
    main()
#currentTrack = iTunes.CurrentTrack
#artist = iTunes.CurrentTrack.Artist
#state = iTunes.PlayerState

#print(currentTrack.Name)
#print(currentTrack.Artwork.Count)
#artwork = currentTrack.Artwork.Item(1)
#artwork.SaveArtworkToFile("D:\College\Coding\Python\ItunesRichPresence\Images\Replacement.png")