import win32com.client

def main():
    
    iTunes = win32com.client.gencache.EnsureDispatch("iTunes.Application")
    library = iTunes.LibraryPlaylist
    tracks = library.Tracks
    track_count = tracks.Count
    
    for track_index in range(1, track_count+1):
        track = tracks.Item(track_index)
        if track.Artwork.Count != 1:
            safePrint('images', track.Artwork.Count)
            safePrint('name', track.Name)
            safePrint('artist', track.Artist)
            safePrint('album', track.Album)
            print

def safePrint(label, data):
    print (label) 
    try:
        print (data)
    except UnicodeEncodeError:
        print (repr(data))

if __name__ == '__main__':
    main()