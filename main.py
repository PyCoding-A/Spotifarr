#!/usr/bin/env python3
from modules.logger import *
from modules.plex import *
from modules.youtube_to_mp3 import *

log("Process 0: Check the cred")
check_cred()

log("Process 1: Updating the playlists")
print('\nUpdating the playlists')
spotify_c().update_playlists()

log("Process 2: Updating the locations")
print('\nUpdating the locations')
build_track_location()

log("Process 3: Download missing")
print('\nDownload missing')
download_missing()

log("Process 4: Connecting to plex & updating the playlists")
print('\nConnecting to plex & updating the playlists')
try:
    plex_c()
except:
    pass
