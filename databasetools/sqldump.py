'''
An example of how to add to a database.
'''

import sqlite3

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

        self.cursor.execute('''CREATE TABLE %s
                (title text, artist text, album text, label text, year int, genre text, BPM real)''' % name)


    def insert_song(self, song):
        print "I'm too lazy."

    def delete_song(self, song):
        print "No."

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()


if __name__ == '__main__':
    db = song_db('BPMdatabase', 'bpmdatabase.db')
    db.insert_song('hello')


# conn = sqlite3.connect('bpmdatabase.db')


# create_new_table = False
# if create_new_table:

# c.execute('''INSERT INTO songs VALUES
#              ('Fake Plastic Trees', 'Radiohead', 'NULL', 74, 'NULL', 'Capitol Records', 1995)''')

# conn.commit()

# # make sure to close cursors
# c.close()
