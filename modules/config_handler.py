#!/usr/bin/env python3
import json
import os
import re
from contextlib import contextmanager


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


def check_cred():
    credentials_cfg = os.path.normpath(
        os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/credentials.json'))

    @contextmanager
    def open_file(filename, method):
        f_to_open = open(filename, method)
        yield f_to_open
        f_to_open.close()

    with open_file(credentials_cfg, 'r') as j_file:
        credentials = json.load(j_file, cls=LazyDecoder)

    if credentials['username'] == "":
        print('\nRefer to https://www.spotify.com/us/account/overview/')
        credentials['username'] = input('Please enter your Spotify username: ')
    if credentials['client_id'] == "":
        print('\nRefer to https://developer.spotify.com/dashboard/')
        credentials['client_id'] = input('Please enter your Spotify client_id via Spotify Dashboard: ')
    if credentials['client_secret'] == "":
        print('\nRefer to https://developer.spotify.com/dashboard/')
        credentials['client_secret'] = input('Please enter your Spotify client_secret via Spotify Dashboard: ')
    if credentials['path_music'] == "":
        credentials['path_music'] = input('\nPut the location of where you want to save your music: ')
    if credentials['plex_base_url'] == "":
        credentials['plex_base_url'] = input('\nPlease insert the plex base url eg: http://localhost:32400/: ')
    if credentials['plex_token'] == "":
        print('\nRefer to https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/')
        credentials['plex_token'] = input('Please insert your plex Token: ')

    with open_file(credentials_cfg, 'w') as j_file:
        json.dump(credentials , j_file)
    print("Credentials is up to date")


def clean_up_text(title):
    unauthorized_txt = ',.\/:*?"<>*|'
    title = str((str(title).encode("utf-8")).decode('utf-8', 'ignore'))
    title = title.strip()
    for cr in unauthorized_txt:
        title = title.replace(cr, '')
    return title


def location_folder(playlist, path):
    for (dir, subdirs, files) in os.walk(path):
        if str(playlist) in subdirs:
            return os.path.normpath(os.path.join(dir + os.path.dirname("/" + str(str(playlist)) + "/")))
    else:
        folder_playlist = os.path.normpath(os.path.join(path + os.path.dirname("/" + str(playlist) + "/")))
        os.mkdir(folder_playlist)


def location_file(song, path):
    file = song
    for (dir, subdirs, files) in os.walk(path):
        if file in files:
            return os.path.normpath(os.path.join(dir + "/" + str(file)))
