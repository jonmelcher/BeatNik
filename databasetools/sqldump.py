'''
An example of how to add to a database.
'''

import sqlite3
from Classes import Song

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
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def create_table(self, name):
        try:
            self.cursor.execute('''CREATE TABLE %s
                (title text, artist text, album text, label text, year int, genre text, BPM real)''' % name)
        except sqlite3.OperationalError:
            print 'The table %s already exists' % name

    def delete_table(self, name):
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

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    db = song_db('BPMdatabase', 'bpmdatabase.db')
    table_name = 'my_songs'
    db.delete_table(table_name)
    db.create_table(table_name)

    my_song_data = ['Radiohead', 'Time of my life', 'The Very Best of Neil Young', 9001, 'Electronic', 'Spam Recording Inc', 2015]

    for i, d in enumerate(my_song_data):
        if isinstance(d, str):
           my_song_data[i] = d.replace(' ', '')
    my_song = Song(my_song_data)

    # print my_song.artist, my_song.title, my_song.label, my_song.year

    db.insert_song(my_song, table_name)


        # self.artist   = song_data[0]
        # self.title    = song_data[1]
        # self.album    = song_data[2]
        # self.BPM      = song_data[3]
        # self.genre    = song_data[4]
        # self.label    = song_data[5]
        # self.year     = song_data[6]


# conn = sqlite3.connect('bpmdatabase.db')


# create_new_table = False
# if create_new_table:

# c.execute('''INSERT INTO songs VALUES
#              ('Fake Plastic Trees', 'Radiohead', 'NULL', 74, 'NULL', 'Capitol Records', 1995)''')

# conn.commit()

# # make sure to close cursors
# c.close()
