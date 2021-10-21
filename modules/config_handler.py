#!/usr/bin/env python3
import json
import os
import re


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)


def clean_up_text(title):
    unauthorized_txt = ',.\/:*?"<>|'
    title = str(title)
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
