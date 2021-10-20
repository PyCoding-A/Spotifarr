#!/usr/bin/env python3
from modules.spotify_db import *
from modules.youtube_to_mp3 import *
from modules.plex import *
from modules.logger import *

log("Process 1")
print('\nUpdating the playlists')
spotify_c().update_playlists()

log("Process 2")
print('\nUpdating the locations')
build_track_location()

log("Process 3")
print('\nDownload missing')
download_missing()

log("Process 4")
print('\nConnecting to plex & updating the playlists')
plex_c()