# iTunes-RPC
iTunes-Rich Presence that will make your discord status the song playing on iTunes.


# Requirements
Requires a .env file containing your discord application client id and your Supabase url and key to get access to your database storage.
.env file must be in the same file directory as the python files.

# How It Works
Uses PyPresence for RPC client connection. 
Win32Com to connect to Itunes and get information regarding Itunes Music and information.
Supabase for database storage for retrieving album art links.

# General Information
Once Supabase storage policies and correct URL and Keys are inputted into the .env (with correct naming convention as the attributes file) file album art will start working.
Text and song information will work regardless of database information. However, album art will only be downloaded/viewable if the albums are in the users library due to limitations with the Win32Com python library.
Error handling is added to prevent any unforseen crashes and prevent duplicated album art images in the storage database. If duplicated images are found the program will delete the duplicated image and will be closed and must be re-opened to work again. 

