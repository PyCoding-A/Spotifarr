#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3
from contextlib import contextmanager


class db:
    def __init__(self):
        self.database_name = 'spotifarr'
        self.db = None
        self.cursor = None

    @contextmanager
    def sql_in(self):
        db_path = os.path.normpath(
            os.path.dirname(os.path.normpath(__file__)).replace('modules', f'config/{self.database_name}.db'))
        try:
            self.db = sqlite3.connect(db_path)
            self.cursor = self.db.cursor()
            yield self.cursor
            self.db.commit()
            self.cursor.close()
            self.db.close()
        except ValueError as e:
            pass

    def test_val(self, table_name, in_col, vals_in_col, equal_to):
        with self.sql_in() as cr:
            cr.execute(f'SELECT {in_col} FROM "{table_name}" WHERE {vals_in_col} = {equal_to}')
            result = cr.fetchone()
        if result is not None:
            return True
        else:
            return False

    def update_val(self, table_name, val_to_be_update, new_val, condition_to_chk, is_equalt_to):
        with self.sql_in() as cr:
            cr.execute(
                f'UPDATE  "{table_name}" SET ({val_to_be_update}) = ({new_val}) WHERE ({condition_to_chk}) = ({is_equalt_to})')

    def insert_val(self, table_name, dic):
        with self.sql_in() as cr:
            cr.execute(f'INSERT INTO "{table_name}" {tuple(dic.keys())} VALUES {tuple(dic.values())}')

    def insert_playlist(self, table_name, dic):
        with self.sql_in() as cr:
            cr.execute(f'INSERT INTO "{table_name}" VALUES (?, ?, ?, ?, ?)', tuple(dic.values()))

    def insert_track(self, table_name, dic):
        with self.sql_in() as cr:
            cr.execute(f'INSERT INTO "{table_name}" {tuple(dic.keys())} VALUES {tuple(dic.values())}')

    def fetch_all_list(self, table_name, what):
        with self.sql_in() as cr:
            cr.execute(f'SELECT {what} FROM "{table_name}"')
            result = cr.fetchall()
        if result is not None:
            return result
        else:
            return []

    def create_playlist_table(self, table_name):
        with self.sql_in() as cr:
            cr.execute(f'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="{table_name}"')
            if cr.fetchone()[0] == 1:
                pass
            else:
                cr.execute(
                    f'CREATE TABLE "{table_name}" (title TEXT NOT NULL, artist TEXT, album TEXT, albumartist TEXT, '
                    f'date TEXT, tracknumber TEXT, location TEXT, url TEXT) ')

    def create_homepage(self):
        with self.sql_in() as cr:
            cr.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='playlists' ''')
            if cr.fetchone()[0] == 1:
                pass
            else:
                cr.execute(
                    'CREATE TABLE "playlists" ("name"	TEXT NOT NULL, "number_of_songs"	INTEGER, "location"	TEXT, '
                    '"downloaded"	INTEGER, "monitored"	INTEGER)')
