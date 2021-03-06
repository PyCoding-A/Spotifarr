#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from plexapi.server import PlexServer

from modules.config_handler import *
from modules.logger import *
from modules.sql_querry import *


class plex_c:
    def __init__(self):
        credentials_cfg = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/credentials.json'))
        self.test = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/test.json'))
        self.db = db()

        @contextmanager
        def open_file(filename, method):
            f_to_open = open(filename, method)
            yield f_to_open
            f_to_open.close()

        with open_file(credentials_cfg, 'r') as j_file:
            credentials = json.load(j_file, cls=LazyDecoder)

        plex_base_url = credentials['plex_base_url']
        plex_token = credentials['plex_token']
        plex = PlexServer(plex_base_url, plex_token)
        print("Connected to: " + str(plex.myPlexAccount()).replace('<MyPlexAccount:https://plex.tv/user:', '').replace(
            '>', ''))
        log("Connected to plex")
        plex.library.refresh()

        for section in plex.library.sections():
            music = plex.library.section(section.title)
            if section.type == "artist":
                for mus in music.searchTracks():
                    location = mus.locations[0]
                    playlist_name = os.path.basename(os.path.dirname(location))
                    playlist = [playlist for playlist in plex.playlists() if playlist.title == playlist_name]

                    if not playlist:
                        plex.createPlaylist(playlist_name, items=mus)
                    else:
                        plex.playlist(playlist_name).addItems(mus)
        print(f"Updating plex playlist done")
        log("Updaing plex playlist done")
