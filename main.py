#!/usr/bin/env python3
from modules.logger import *
# -*- coding: utf-8 -*-
from modules.plex import *
from modules.youtube_to_mp3 import *
from time import sleep

log("Process 0: Check the cred")
check_cred()


log("Process 1: Updating the playlists")
print('\nUpdating the playlists')
spotify_c().update_playlists()
sleep(5)

log("Process 2: Updating the locations")
print('\nUpdating the locations')
build_track_location()
sleep(5)

log("Process 3: Download missing")
print('\nDownload missing')
download_missing()
sleep(5)

log("Process 4: Refrech the locations")
print('\nRefrech the locations')
build_track_location()
sleep(5)

log("Process 4: Connecting to plex & updating the playlists")
print('\nConnecting to plex & updating the playlists')
try:
    plex_c()
except:
    pass
