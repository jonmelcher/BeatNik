'''
Some tools for interacting with an sqlite database.
'''

import sqlite3


class song_db(object):
    'Initializes and manipulates a database of songs'

    # Fix documentation


    def __init__(self, name, database):
        self.name = name
        self.database = database
        self.cursor = None
        self.conn = None
        self.connect()

    def connect(self):
        'Connects the database to the self.database database.'
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_song_table(self, name):
        'Attempts to create an SQL table.'
        try:
            self.cursor.execute('''CREATE TABLE %s
                (artist text, title text, album text, label text, year int, genre text, BPM real, key text)''' % name)
        except sqlite3.OperationalError:
            print 'The table %s already exists' % name


    def drop_table(self, name):
        'Drops name if it exists.'

        self.cursor.executescript('drop table if exists %s;' % name)


    def insert_song(self, song, table):
        'Inserts song into table.'
        'Refer to music.py for the Song class.'

        self.cursor.execute('''INSERT INTO %s VALUES
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')'''
            % (table,
               song.artist,
               song.title,
               song.album,
               song.BPM,
               song.genre,
               song.label,
               song.year,
               song.key,
              )
            )

    def delete_song(self, song):
        print "No."

    def fetch_artist(self, artist, table):
        'Returns a list of all database entries in table'
        'with the matching artist.'

        t = (artist, )
        self.cursor.execute('SELECT * FROM %s WHERE artist=?' % table, t)
        return self.cursor.fetchall()


    def table_contents(self, table):
        self.cursor.execute('SELECT * FROM %s' % table)
        return self.cursor.fetchall()


    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    pass
