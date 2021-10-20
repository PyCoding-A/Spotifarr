#!/usr/bin/env python3
import os
from contextlib import contextmanager
from datetime import datetime


@contextmanager
def file(filename, method):
    file = open(filename, method)
    yield file
    file.close()


log_file = os.path.normpath(
    os.path.dirname(os.path.normpath(__file__)).replace('modules', 'config/log_spotifarr.txt'))
today = str(datetime.now())
with file(log_file, 'w') as f:
    f.write(f'Log of [{today}]\n')


class log:
    def __init__(self, text):
        self.text = text
        self.text = self.text + "\n"

        with file(log_file, 'a') as f:
            f.write(self.text)
