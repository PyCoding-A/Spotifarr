#!/usr/bin/env python3
from modules.spotify_db import *
from modules.youtube_to_mp3 import *
from modules.plex import *
print('\nUpdating the playlists')
spotify_c().update_playlists()

print('\nUpdating the locations')
build_track_location()

print('\nDownload missing')
download_missing()

print('\nConnecting to plex & updating the playlists')
plex_c()