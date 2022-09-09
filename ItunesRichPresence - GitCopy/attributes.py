#Related Imports
import os
import win32com.client
from pypresence import Presence
import time

#Discord Application Client ID
clientid = "clientid"

#Points thisFolder to the location where program is located.
path = "point to the album txt file"
thisFolder = os.path.dirname(path)


#iTunes Program
iTunes = win32com.client.Dispatch("iTunes.Application")


#Album List Text File
albumFile = 'albumsFinal.txt'