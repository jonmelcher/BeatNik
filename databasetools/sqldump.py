'''
An example of how to add to a database.
'''

import sqlite3

# I needed to copy Classes.py to the current direcory. I don't know
# how to import modules from directories other than the current working
# directory. Hence, this code is
'''UNSTABLE'''
from ..bin import Classes


class song_db(object):
    'Initializes and manipulates a database of songs'

    # Fix documentation


    def __init__(self, name, db_name):
        self.name = name
        self.database = db_name
        self.cursor = None
        self.conn = None
        self.connect()

    def connect(self):
        'Connects the database to the self.database database.'
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_table(self, name):
        'Attempts to create an SQL table.'
        try:
            self.cursor.execute('''CREATE TABLE %s
                (artist text, title text, album text, label text, year int, genre text, BPM real)''' % name)
        except sqlite3.OperationalError:
            print 'The table %s already exists' % name

    def drop_table(self, name):
        'Drops name if it exists.'
        self.cursor.executescript('drop table if exists %s;' % name)


    def insert_song(self, song, table):

        self.cursor.execute('''INSERT INTO %s VALUES
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s')'''
            % (table,
               song.artist,
               song.title,
               song.album,
               song.BPM,
               song.genre,
               song.label,
               song.year,
              )
            )

    def delete_song(self, song):
        print "No."

    def fetch_artist(self, artist, table):
        t = (artist, )
        self.cursor.execute('SELECT * FROM my_songs WHERE artist=?', t)
        return self.cursor.fetchone()




    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    db = song_db('BPMdatabase', 'bpmdatabase.db')
    table_name = 'my_songs'
    db.drop_table(table_name)
    db.create_table(table_name)

    my_song_data = ['Radiohead', 'Time of my life', 'The Very Best of Neil Young', 9001, 'Electronic', 'Spam Recording Inc', 2015]

    my_song = Song(my_song_data)


    db.insert_song(my_song, table_name)

    db.fetch_artist(my_song.artist, table_name)

