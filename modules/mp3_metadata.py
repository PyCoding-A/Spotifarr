#!/usr/bin/env python3
import os.path
import urllib
import urllib.request

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

from modules.spotify_db import *


def download_photo(img_url, filename):
    try:
        urllib.request.urlretrieve(img_url, filename)
    except:
        pass


class metadata:
    def __init__(self, music_data, music_path):

        self.music_path = music_path
        self.music_data = music_data

    def metadata_updata(self):
        audio = EasyID3(self.music_path)
        audio['title'] = self.music_data[0]
        audio['artist'] = self.music_data[1]
        audio['album'] = self.music_data[2]
        audio['albumartist'] = self.music_data[3]
        audio['date'] = self.music_data[4]
        audio['tracknumber'] = self.music_data[5]
        audio.save()
        albumartURL = self.music_data[7]
        albumArtFilename = self.music_path.replace('.mp3', '.jpg')
        try:
            download_photo(albumartURL, albumArtFilename)
            audio = ID3(self.music_path)
            with open(albumArtFilename, 'rb') as albumart:
                audio.add(APIC(3, 'image/jpeg', 3, 'Front cover', albumart.read()))
            audio.save()
        except:
            pass
        try:
            os.remove(albumArtFilename)
        except:
            pass

    def force_metadata(self):
        name = self.music_data[1] + "-" + self.music_data[0]
        results = spotify_c().get_track(name)
        if results is not None:
            for track in results['tracks']['items']:

                audio = EasyID3(self.music_path)
                audio['title'] = clean_up_text(track['name'])
                audio['artist'] = clean_up_text(track['artists'][0]['name'])
                audio['album'] = clean_up_text(track['album']['name'])
                audio['albumartist'] = clean_up_text(track['album']['artists'][0]['name'])
                audio['date'] = clean_up_text(track['album']['release_date'])
                audio['tracknumber'] = clean_up_text(track['track_number'])
                audio.save()
                albumartURL = track['album']['images'][0]['url']
                albumArtFilename = self.music_path.replace('.mp3', '.jpg')
                try:
                    download_photo(albumartURL, albumArtFilename)
                    audio = ID3(self.music_path)
                    with open(albumArtFilename, 'rb') as albumart:
                        audio.add(APIC(3, 'image/jpeg', 3, 'Front cover', albumart.read()))
                    audio.save()
                except:
                    pass
                try:
                    os.remove(albumArtFilename)
                except:
                    pass
