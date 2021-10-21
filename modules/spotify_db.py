#!/usr/bin/env python3
import os.path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from modules.config_handler import *
from modules.logger import *
from modules.sql_querry import *


class spotify_c:
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

        auth_manager = SpotifyClientCredentials(client_id=credentials['client_id'],
                                                client_secret=credentials['client_secret'])
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        self.sp_user = credentials['username']

        self.path_music = os.path.normpath(credentials['path_music'])

        if self.path_music:
            try:
                os.mkdir(self.path_music)
            except:
                pass
        log("connected to spotify")

    def get_track(self, name):
        results = self.sp.search(name, limit=1)
        if results:
            if len(results['tracks']['items']) == 0:
                return None
            else:
                return results
        else:
            return None

    def create_tracks(self, tracks, playlist_name):
        log(f"Creating track DB for {playlist_name}")
        i = 0
        for i, item in enumerate(tracks['items']):
            track = item['track']
            title = clean_up_text(track['name'])
            if not self.db.test_val(table_name=f'{playlist_name}', in_col="title", vals_in_col="title",
                                    equal_to=f'"{title}"'):
                track_info = {
                    "title": title.encode("utf-8"),
                    "artist": clean_up_text(track['artists'][0]['name']).encode("utf-8"),
                    "album": clean_up_text(track['album']['name']).encode("utf-8"),
                    "albumartist": clean_up_text(track['artists'][0]['name']).encode("utf-8"),
                    "date": str(track['album']['release_date']),
                    "tracknumber": str(track['track_number']),
                    "url": str(track['album']['images'][0]['url']) if len(track['album'][
                                                                              'images']) > 0 else "https://upload.wikimedia.org/wikipedia/commons/3/3c/No-album-art.png"
                }
                self.db.insert_val(table_name=playlist_name, dic=track_info)
            else:
                pass
        if i > 0:
            log(f'[X] {str(i)} tracks added to {playlist_name}')

    def update_playlists(self):
        self.db.create_homepage()
        playlists = self.sp.user_playlists(self.sp_user)
        log("Adding spotify playlists to the DB")
        print(f"\n Updating database with {str(len(playlists['items']))} playlists: [", end='')
        for playlist in playlists['items']:
            results = self.sp.playlist(playlist['id'], fields="tracks,next")
            tracks = results['tracks']
            playlist_info = {
                "name": clean_up_text(playlist['name']),
                "number_of_songs": playlist['tracks']['total'],
                "location": location_folder(clean_up_text(playlist['name']), self.path_music),
                "downloaded": 0,
                "monitored": 1,
            }
            if not self.db.test_val(table_name="playlists", in_col="name", vals_in_col='"name"',
                                    equal_to=f'"{playlist_info["name"]}"'):
                log(f'> Creating playlist {playlist_info["name"]}')
                self.db.insert_playlist(table_name="playlists", dic=playlist_info)
                self.db.create_playlist_table(table_name=playlist_info["name"])

            elif (not self.db.test_val(table_name="playlists", in_col="*",
                                       vals_in_col="number_of_songs",
                                       equal_to=f'"{playlist_info["number_of_songs"]}"')) or (
                    not self.db.test_val(table_name="playlists", in_col="*",
                                         vals_in_col="location",
                                         equal_to=f'"{playlist_info["location"]}"')):
                log(f'> Updating playlist {playlist_info["name"]}')
                self.db.create_playlist_table(table_name=playlist_info["name"])
                self.db.update_val(table_name="playlists", val_to_be_update='"number_of_songs","location"',
                                   new_val=f'"{playlist_info["number_of_songs"]}","{playlist_info["location"]}"',
                                   condition_to_chk='"name"',
                                   is_equalt_to=f'"{playlist_info["name"]}"')

            self.create_tracks(tracks, playlist_info["name"])
            while tracks['next']:
                tracks = self.sp.next(tracks)
                self.create_tracks(tracks, playlist_info["name"])
            print("U", end='')
        print("]", end='')
        log("Spotify playlists and tracks imported")
