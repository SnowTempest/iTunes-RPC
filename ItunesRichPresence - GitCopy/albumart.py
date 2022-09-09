from pypresence import Presence
import time
import win32com.client
import os

thisFolder = os.path.dirname(os.path.abspath(__file__))

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


def txtFile():
    print("Method Entered")
    iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
    library = iTunes.LibraryPlaylist
    tracks = library.Tracks
    track_count = tracks.Count

    with open(os.path.join(thisFolder, 'albums.txt'), "w+") as f:
        i = 1
        for track_index in range (i, track_count+1):
            track = tracks.Item(track_index)
            album = track.Album
            f.write(album + " - \n")
        f.flush()

    f.close()

def removeDupes():
    lines_seen = set()

    outFile = open(os.path.join(thisFolder, 'albumsFinal.txt'), "w")
    inFile = open(os.path.join(thisFolder, 'albums.txt'), "r")

    for line in inFile:
        if line not in lines_seen:
            outFile.write(line)
            lines_seen.add(line)
    outFile.close()

def sortFile():
    with open(os.path.join(thisFolder, 'albumsNoDupes.txt'), 'r') as f:
        lines = f.readlines()
        lines.sort()
        with open(os.path.join(thisFolder, 'albumsFinal.txt'), 'w') as f2:
            for line in lines:
                f2.write(line)
    f.close()
    f2.close()

txtFile()
removeDupes()
sortFile()