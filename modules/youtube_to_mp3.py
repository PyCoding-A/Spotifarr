#!/usr/bin/env python3

import yt_dlp
from youtubesearchpython import VideosSearch
from ytmusicapi import YTMusic

from modules.mp3_metadata import *
from modules.sql_querry import *


class music:

    def __init__(self, video_title):
        self.video_title = video_title
        option_cfg = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/option.json'))
        credentials_cfg = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/credentials.json'))
        self.path_config = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config'))

        @contextmanager
        def open_file(filename, method):
            f_to_open = open(filename, method)
            yield f_to_open
            f_to_open.close()

        with open_file(option_cfg, 'r') as f:
            self.option = json.load(f)

        with open_file(credentials_cfg, 'r') as f:
            self.credentials = json.load(f)

    def download_in(self, path_to_save):
        # print("[>] Downloading " + self.video_title + " ...")
        self.option['outtmpl'] = path_to_save + "/" + self.video_title + '.%(ext)s'
        try:
            os.remove(self.path_config + "/youtube.com_cookies.txt")
        except:
            pass
        self.option['cookiefile'] = self.path_config + "/youtube.com_cookies.txt"
        ytmusic = YTMusic()
        search_results = ytmusic.search(self.video_title, filter='songs')[0]['videoId']
        video_url = "https://www.youtube.com/watch?v=" + search_results
        if search_results is None or search_results == "":
            # videosSearch = VideosSearch(self.video_title + "duration < 10min", limit=2)
            videosSearch = VideosSearch(self.video_title, limit=1)

            video_url = videosSearch.result()['result'][0]['link']
        print(f"\n[{self.video_title}] : {video_url}")
        try:
            video_info = yt_dlp.YoutubeDL(self.option).extract_info(
                url=video_url, download=False
            )
            with yt_dlp.YoutubeDL(self.option) as ydl:
                sleep(1)
                ydl.download([video_info['webpage_url']])
                log(f"Downloading {self.video_title}")
            return True
        except:
            print(f"I cannot download {self.video_title}")
            return False


def build_track_location():
    log("Building track locations into DB")
    list_playlist = db().fetch_all_list(table_name="playlists", what="*")

    for ps in list_playlist:
        db().create_playlist_table(ps[0])
        list_track = db().fetch_all_list(table_name=f'{ps[0]}', what="*")
        print(f"\n {ps[0]} with {str(len(list_track))}: [", end='')
        s = 0
        for track in list_track:
            name = str(track[1]) + " - " + str(track[0]) + ".mp3"
            location = location_file(name, ps[2])
            if location is not None:
                if track[6] is None or track[6] == "None" or track[6] != location:
                    db().update_val(table_name=ps[0], val_to_be_update='"location"', new_val=f'"{location}"',
                                    condition_to_chk='"title","artist"',
                                    is_equalt_to=f'"{track[0]}","{track[1]}"')
                if os.path.exists(location):
                    s = s + 1
            print("=", end='')
        print("]", end='')
        db().update_val(table_name="playlists", val_to_be_update='"downloaded"',
                        new_val=s,
                        condition_to_chk='"name"',
                        is_equalt_to=f'"{ps[0]}"')

    log(f"[| Location for songs of {ps[0]} were built")


def download_missing():
    log("Download missing")
    list_playlist = db().fetch_all_list(table_name="playlists", what="*")
    for ps in list_playlist:
        if ps[4] == 1:
            list_track = db().fetch_all_list(table_name=f'{ps[0]}', what="*")
            print(f"\n {ps[0]} with {str(len(list_track))}: [", end='')

            for track in list_track:

                if track[6] is None or track[6] == "None" or not os.path.exists(track[6]):
                    if music(track[1] + " - " + track[0]).download_in(ps[2]):
                        music_path = os.path.normpath(ps[2] + "/" + track[1] + " - " + track[0] + ".mp3")
                        db().update_val(table_name=ps[0], val_to_be_update='"location"', new_val=f'"{music_path}"',
                                        condition_to_chk='"title","artist"',
                                        is_equalt_to=f'"{track[0]}","{track[1]}"')
                        try:
                            metadata(track, music_path).metadata_updata()
                        except:
                            pass
                print(".", end='')
            print("]", end='')
    log("Download missing complete")
    build_track_location()


def force_loop_metadata(search):
    list_playlist = db().fetch_all_list(table_name="playlists", what="*")
    for ps in list_playlist:
        list_track = db().fetch_all_list(table_name=f'{ps[0]}', what="*")
        print(f"\n {ps[0]} with {str(len(list_track))}: [", end='')
        for track in list_track:
            if track[6] is not None or track[6] != "None" or os.path.exists(track[6]):
                if search:
                    metadata(track, track[6]).force_metadata()
                if not search:
                    try:
                        metadata(track, track[6]).metadata_updata()
                    except:
                        pass
            print("#", end='')
        print("]", end='')


